#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2019/10/23 15:27
# @Author  : Alex Kwan
# @Email   : gjy-alex@hotmail.com
# @File    : main.py
# @edited  : aleksejqa 12.08.2021


import m3u8
import utils.tools
import utils.db
import time
import os

class Iptv(object):
    playlist_file = 'playlists/'
    m3u8_file_path = 'output/'
    delay_threshold = 3000 # тайм аут на канал

    def __init__(self):
        self.T = utils.tools.Tools()

        self.now = int(time.time() * 1000)

    def getPlaylist(self):

        playList=[]
        path = os.listdir(self.playlist_file)
        for p in path:
            if os.path.isfile(self.playlist_file + p):
                if p[-4:]=='.m3u':
                    try:
                        m3u8_obj = m3u8.load(self.playlist_file + p)
                        total = len(m3u8_obj.segments)
                        for i in range(0, total):
                            tmp_title = m3u8_obj.segments[i].title
                            tmp_url = m3u8_obj.segments[i].uri
                            data={'title': tmp_title,'url': tmp_url,}
                            playList.append(data)
                    except Exception as e:
                        print(e)
        return playList

    def checkPlayList(self,playList):
        good_i=0
        bad_i=0
        output_file=self.m3u8_file_path+ str(time.time()*1000) +'.m3u'
        with open (output_file,'a', encoding="utf-8") as f:
            f.write("#EXTM3U\n")
        total=len(playList)
        if (total<=0): return False
        for i in range(0,total):
            tmp_title = playList[i]['title']
            tmp_url =playList[i]['url']
            print('Проверка [ %s / %s ](%s/%s):%s' % (i, total,good_i,bad_i, tmp_title))

            netstat = self.T.chkPlayable(tmp_url)
            #print(netstat)
            if netstat > 0 and netstat < self.delay_threshold:
                data = {
                    'title': tmp_title,
                    'url': tmp_url,
                    'delay': netstat,
                    'updatetime': self.now,
                }
                good_i+=1
                
                with open (output_file,'a', encoding="utf-8") as f:
                    f.write("#EXTINF:-1, %s\n" % (tmp_title))
                    f.write("%s\n" % (tmp_url))
            else:
                bad_i+=1
                pass

   


if __name__ == '__main__':
    iptv=Iptv()
    print('начало......')
    iptv.checkPlayList(iptv.getPlaylist())

    print('конец.....')
