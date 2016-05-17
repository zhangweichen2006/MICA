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
    def dejavu(self):
	    config = {"database": {"host": "127.0.0.1", "user": "root", "passwd": "", "db": "dejavu"}}
	    # config = {"database": {"host": "10.66.31.157", "user": "root", "passwd": "662813", "db": "dejavu"}}
	    djv = Dejavu(config)
	    song = djv.recognize(FileRecognizer, "record_music/convchou.mp3")
	    print(song)

if __name__ == "__main__":
    g = Recognition()
    g.dejavu()






