from .Init import Config

import vlc

class audioPlayer():
    def __init__(self):

        self.mediaPlayer = vlc.MediaPlayer()
        self.level = -1
        self.path = Config().get_config("AudioPath")
        self.playList = Config().get_config("PlayList")

    def start_Audio(self):
        import time

        if self.level == -1:
            return

        self.mediaPlayer.stop()
        path = self.path + self.playList[self.level]
        
        print("Start Audio : ", path)
        self.mediaPlayer.set_media(vlc.Media(path))
        self.mediaPlayer.play()
        time.sleep(0.1)
        self.mediaPlayer.pause()
        time.sleep(1.5)
        self.mediaPlayer.play()

    def stop_Audio(self):
        if self.mediaPlayer.is_playing:
            self.mediaPlayer.stop()

    def set_Level(self, level):
        self.level = level

    def set_PlayList(self, index):
        self.playList = Config().get_config("EffectList").get(index)