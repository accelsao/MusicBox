import sys

import pytube
import os
from time import sleep
import vlc
import argparse
from random import choice
import keyboard
from PyQt5.QtWidgets import QApplication
from pytube import YouTube

from gui import Player
from playlist import MusicLists


class Music(dict):
  def __init__(self):
    super(Music, self).__init__()

  def addSong(self, label, url):
    if label not in self:
      self[label] = list()

    if url not in self[label]:
      self[label].append(url)

music = Music()
music.addSong('bach', '')
music.addSong('Your Lie in April', 'https://www.youtube.com/watch?v=uLFtmJlzKvE')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tag', type=str, help='set tags for the song', required=True)
    parser.add_argument('-id', '--url_id', type=str, help='youtube url ID')
    args = parser.parse_args()


    m = MusicLists('playlist.p')
    print(m)

    if args.tag not in m:
        print('[tag: {}] is not in the playlist, please add it！'.format(args.tag))

    if args.url_id is not None and args.url_id not in m[args.tag]:
        print('[id: {}] is not in the [tag: {}], please add it！'.format(args.url_id, args.tag))

    if args.url_id is None:
        url = 'https://www.youtube.com/watch?v=' + choice(m[args.tag])
    else:
        url = 'https://www.youtube.com/watch?v=' + args.url_id

    print(url)

    # yt = pytube.YouTube('https://www.youtube.com/watch?v=uLFtmJlzKvE')
    # yt = YouTube('https://www.youtube.com/watch?v=R-bLiEFnyZw')
    yt = YouTube(url)
    url = yt.streams.all()[0].url
    print(url)

    # url = "https://www.youtube.com/watch?v=XtqGr-km0XQ"
    # video = pafy.new(url)
    # best = video.getbest()
    # playurl = best.url
    # print(playurl)
    # v = vlc.Instance()
    # player = v.media_player_new()
    # Media = v.media_new(url)
    # print(Media)
    # # Media.get_mrl()
    # print(Media)
    # player.set_media(Media)
    # player.play()
    app = QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    sys.exit(app.exec_())


    # print(123)
    # while True:
    #     try:
    #         if keyboard.is_pressed('q'):
    #             player.pause()
    #         elif keyboard.is_pressed('s'):
    #             player.stop()
    #     except KeyboardInterrupt:
    #         exit()

    # while not player.is_playing():
    #     sleep(1)
    #
    # while player.is_playing():
    #     pass
