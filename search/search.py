import pyaudio
import wave

import pygame, sys
from pygame.locals import *
from pygame import *
import MenuSystem


# import sys
# sys.path.append("dejavu/")
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
# from dejavu.recognize import MicrophoneRecognizer


class Recognition(object):
    def dejavu(self, select_song):
        # config = {"database": {"host": "127.0.0.1", "user": "root", "passwd": "", "db": "dejavu"}}
        config = {"database": {"host": "10.66.31.157", "user": "root", "passwd": "662813", "db": "dejavu"}}
        djv = Dejavu(config)
        # djv.fingerprint_directory("mp3/Piano/", [".mp3"])
        # djv.fingerprint_directory("mp3/Violin/", [".mp3"])
        song = djv.recognize(FileRecognizer, select_song)
        # print(song)
        return song

# if __name__ == "__main__":
#     g = Recognition()
#     g.dejavu("output.wav")






