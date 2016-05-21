import pyaudio
import wave

import pygame, sys, glob
from pygame.locals import *
from pygame import *
from PIL import Image

from os import listdir
from os.path import isfile, join

from instrument.classify import Classify
from MenuSystem import MenuSystem
from MenuSystem.gif import GIFImage

from pydub import AudioSegment

# --------------pathgetter------------------
from sys import path
import os.path
thisrep = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.dirname(thisrep))

from EasyGame import pathgetter

import sndhdr

# Background Setup
BACKGROUND_IMG = 'resource/python4.jpg'
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

FONT = "MenuSystem/Roboto-Regular.ttf"
RESULT_FONT = "MenuSystem/TanglewoodTales.ttf"

# Recording Configs
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
# RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,0,0)
GREEN = (0,200,0)
GRAY = (128,128,128)
BLUE = (25,25,112)
BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)
BRIGHT_GRAY = (160,160,160)
BRIGHT_BLUE = (0,249,255)#(0,102,204)
HALF_DARK_BLUE = (0,76,153)
FONT_BLUE = (51,153,255)
BG_COLOR = (0,0,0)#(27,34,39)#(77,96,110)
ORANGE = (251,177,0)

# Button position
RECORD_X = 500
RECORD_Y = 50
RECORD_WIDTH = 80
RECORD_HEIGHT = 40

STOP_X = 620
STOP_Y = 50
STOP_WIDTH = 80
STOP_HEIGHT = 40

CLF_X = 740
CLF_Y = 50
CLF_WIDTH = 80
CLF_HEIGHT = 40

BACK_X = 50
BACK_Y = 50
BACK_WIDTH = 80
BACK_HEIGHT = 40

# PRED_X = 
# PRED_Y = 
PRED_WIDTH = 600
PRED_HEIGHT = 200

# play, pause and stop
PLAY_X = 310
PLAY_Y = 450
PLAY_WIDTH = 80
PLAY_HEIGHT = 40

PAUSE_X = PLAY_X + 120
PAUSE_Y = PLAY_Y
PAUSE_WIDTH = PLAY_WIDTH
PAUSE_HEIGHT = PLAY_HEIGHT

STP_X = PAUSE_X + 120
STP_Y = PLAY_Y
STP_WIDTH = PLAY_WIDTH
STP_HEIGHT = PLAY_HEIGHT

VALID_X = 155
VALID_Y = 270
SELECT_X = 180
SELECT_Y = 60

RESELECT_X = 450 + SELECT_X
RESELECT_Y = SELECT_Y - 10
RESELECT_WIDTH = 80
RESELECT_HEIGHT = PLAY_HEIGHT

SEARCH_X = 150 + RESELECT_X
SEARCH_Y = RESELECT_Y
SEARCH_WIDTH = RESELECT_WIDTH
SEARCH_HEIGHT = RESELECT_HEIGHT

DBMUSIC_X = SELECT_X - 50
DBMUSIC_Y = 180 + SELECT_Y

# sound wave jif
# WAVES = [Image.open(join(WAVE_PATH, f)) for f in listdir(WAVE_PATH) if isfile(join(WAVE_PATH, f)) and "wave" in f]
# IMG = [pygame.Surface.fromstring(w, (220,60), "P") for w in WAVES]

# print WAVES
# print IMG
# pygame.transform.scale(pygame.image.load(w), (600, 70))

class Gui(object):

    def delete_module(self, modname, paranoid=None):
        from sys import modules
        try:
            thismod = modules[modname]
        except KeyError:
            raise ValueError(modname)
        these_symbols = dir(thismod)
        if paranoid:
            try:
                paranoid[:]  # sequence support
            except:
                raise ValueError('must supply a finite list for paranoid')
            else:
                these_symbols = paranoid[:]
        del modules[modname]
        for mod in modules.values():
            try:
                delattr(mod, modname)
            except AttributeError:
                pass
            if paranoid:
                for symbol in these_symbols:
                    if symbol[:2] == '__':  # ignore special symbols
                        continue
                    try:
                        delattr(mod, symbol)
                    except AttributeError:
                        pass

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def initialise_background(self):
        # background setup
        pygame.display.set_caption('Music Identification and Classification Application (MICA)')

        
        # print 'x: {}, y: {}'.format(self.imgwave_x, self.imgwave_y)                                         

        self.gameDisplay = display.set_mode(self.bg.get_size())
        self.scrrect = self.gameDisplay.blit(self.bg,(0,0))
        display.flip()

    def initialise_menu(self):
        
        # initialise menu system
        MenuSystem.init()
        MenuSystem.BGCOLOR = Color(200,200,200,80)
        MenuSystem.FGCOLOR = Color(200,200,200,255)
        MenuSystem.BGHIGHTLIGHT = Color(0,0,0,180)
        MenuSystem.BORDER_HL = Color(200,200,200,180)

        # create menu
        self.search_menu  = MenuSystem.Menu('Search',      ('Search with File','Search with Mic','About Search'))
        self.recognize_menu = MenuSystem.Menu('Instrument',    ('Recognize with File','Recognize with Mic','About Recognize'))
        self.accuracy_check_menu   = MenuSystem.Menu('Similarity',    ('Accuracy Check','About Accuracy Check'))
        self.exit = MenuSystem.Menu('System', ('Exit', 'About us'))
        
        # create bars
        self.bar = MenuSystem.MenuBar()
        self.bar.set((self.recognize_menu,self.search_menu, self.accuracy_check_menu, self.exit))
        display.update(self.bar)

        self.ms = MenuSystem.MenuSystem()

        # self.exit_button = MenuSystem.Button('EXIT',100,30)
        # self.exit_button.bottomright =  self.scrrect.w-20,self.scrrect.h-20
        # self.exit_button.set()

    def record_screenloop(self):

        # mouse on GREEN show record button
        if RECORD_X+RECORD_WIDTH > self.mouse[0] > RECORD_X and RECORD_Y+RECORD_HEIGHT > self.mouse[1] > RECORD_Y \
            and not self.recording:

            pygame.draw.rect(self.gameDisplay, BRIGHT_RED,(RECORD_X,RECORD_Y,RECORD_WIDTH,RECORD_HEIGHT))
            textRecord, recRect = self.text_objects("Record", self.smallText, BLACK)
            if self.click[0] == 1 :
                if self.recording == False:
                    self.open_record()
                    self.recording = True
                    self.is_predicted = False 
                    self.is_recorded = False
                    self.is_music_load = False
                    self.music_found = False
                    self.data_file = False
                    self.music.stop()
                self.record_once = True
        else:
            pygame.draw.rect(self.gameDisplay, BRIGHT_RED,(RECORD_X,RECORD_Y,RECORD_WIDTH,RECORD_HEIGHT), 1)
            textRecord, recRect = self.text_objects("Record", self.smallText, BRIGHT_RED)

        
        
        recRect.center = ( (RECORD_X+(RECORD_WIDTH/2)), (RECORD_Y+(RECORD_HEIGHT/2)) )
        self.gameDisplay.blit(textRecord, recRect)

        # mouse on RED stop record button
        if STOP_X+STOP_WIDTH > self.mouse[0] > STOP_X and STOP_Y+STOP_HEIGHT > self.mouse[1] > STOP_Y \
            and self.recording:

            pygame.draw.rect(self.gameDisplay, BRIGHT_GRAY,(STOP_X,STOP_Y,STOP_WIDTH,STOP_HEIGHT))
            textStop, stopRect = self.text_objects("Stop", self.smallText, BLACK)
        else:
            pygame.draw.rect(self.gameDisplay, BRIGHT_GRAY,(STOP_X,STOP_Y,STOP_WIDTH,STOP_HEIGHT), 1) 
            textStop, stopRect = self.text_objects("Stop", self.smallText, BRIGHT_GRAY)

        
        stopRect.center = ((STOP_X+(STOP_WIDTH/2)), (STOP_Y+(STOP_HEIGHT/2)) )
        self.gameDisplay.blit(textStop, stopRect)

        # back button
        if BACK_X+BACK_WIDTH > self.mouse[0] > BACK_X and BACK_Y+BACK_HEIGHT > self.mouse[1] > BACK_Y:
            pygame.draw.rect(self.gameDisplay, WHITE ,(BACK_X,BACK_Y,BACK_WIDTH,BACK_HEIGHT))
            textBack, recBack = self.text_objects("Back", self.smallText, BLACK)
            if self.click[0] == 1:
                self.recording = False
                self.click_func = False
                self.is_predicted = False
                self.is_recorded = False
                self.is_music_load = False
                self.music.stop()
        else:
            pygame.draw.rect(self.gameDisplay, WHITE,(BACK_X,BACK_Y,BACK_WIDTH,BACK_HEIGHT), 1)
            textBack, recBack = self.text_objects("Back", self.smallText, WHITE)

        recBack.center = ((BACK_X+(BACK_WIDTH/2)), (BACK_Y+(BACK_HEIGHT/2)) )
        self.gameDisplay.blit(textBack, recBack)

        
    def set_recording_variables(self):
        # recording variables setup
        self.recording = False
        self.record_once = False
        self.p = pyaudio.PyAudio()


    def open_record(self):
        # initialise recording
        self.recording = True
        self.stream = self.p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK)
        self.frames = []


    def loop_record(self):
        # start recording
        if self.recording:
            print("* recording")
            self.imgwave.render(self.gameDisplay, (self.imgwave_x,self.imgwave_y))
            data = self.stream.read(CHUNK)
            self.frames.append(data)
        else:
            self.gameDisplay.blit(self.imgwave.frames[0][0], (self.imgwave_x,self.imgwave_y))


    def stop_record(self):
        #stop recording
        for event in pygame.event.get():
            if STOP_X+STOP_WIDTH > self.mouse[0] > STOP_X and STOP_Y+STOP_WIDTH > self.mouse[1] > STOP_Y and self.recording and self.click[0] == 1 \
                and self.recording:
                print("* done recording")

                self.stream.stop_stream()
                self.stream.close()

                self.wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                self.wf.setnchannels(CHANNELS)
                self.wf.setsampwidth(self.p.get_sample_size(FORMAT))
                self.wf.setframerate(RATE)
                self.wf.writeframes(b''.join(self.frames))
                
                self.recording = False
                self.is_recorded = True
                self.smallText = pygame.font.Font(FONT,16)
                text_clf, clf_rect = self.text_objects("Classify", self.smallText, HALF_DARK_BLUE)
                clf_rect.center = ( (CLF_X+(CLF_WIDTH/2)), (CLF_Y+(CLF_HEIGHT/2)) )
                self.gameDisplay.blit(text_clf, clf_rect)
                # break
                self.wf.close()

            if event.type == QUIT:
                if self.record_once:
                    self.p.terminate()
                    # self.wf.close()
                pygame.quit(); 
                sys.exit()

    def play_music_buttons(self, play_music):

        # print(play_music,"   pppp")
        # loading recorded music
        if not self.is_music_load:
            print(play_music)
            # self.music.load(os.path.join('mp3',play_music))
            self.music.load(play_music)
            self.is_music_load = True

        # print(play_music,"   pppp2")
        # play 
        if PLAY_X+PLAY_WIDTH > self.mouse[0] > PLAY_X and PLAY_Y+PLAY_HEIGHT > self.mouse[1] > PLAY_Y:

            pygame.draw.rect(self.gameDisplay, BRIGHT_GREEN,(PLAY_X,PLAY_Y,PLAY_WIDTH,PLAY_HEIGHT))
            text_play, play_rect = self.text_objects("Play", self.smallText, BLACK)

            if self.click[0] == 1:
                if self.music.get_busy():
                    self.music.unpause()
                else:
                    self.music.play(2)

        else:
            pygame.draw.rect(self.gameDisplay, BRIGHT_GREEN,(PLAY_X,PLAY_Y,PLAY_WIDTH,PLAY_HEIGHT), 1) 
            text_play, play_rect = self.text_objects("Play", self.smallText, BRIGHT_GREEN)
        
        play_rect.center = ((PLAY_X+(PLAY_WIDTH/2)), (PLAY_Y+(PLAY_HEIGHT/2)) )
        self.gameDisplay.blit(text_play, play_rect)
        
        # pause
        if PAUSE_X+PAUSE_WIDTH > self.mouse[0] > PAUSE_X and PAUSE_Y+PAUSE_HEIGHT > self.mouse[1] > PAUSE_Y:

            pygame.draw.rect(self.gameDisplay, ORANGE,(PAUSE_X,PAUSE_Y,PAUSE_WIDTH,PAUSE_HEIGHT))
            text_pause, pause_rect = self.text_objects("Pause", self.smallText, BLACK)
            
            if self.click[0] == 1:
                self.music.pause()

        else:
            pygame.draw.rect(self.gameDisplay, ORANGE,(PAUSE_X,PAUSE_Y,PAUSE_WIDTH,PAUSE_HEIGHT), 1) 
            text_pause, pause_rect = self.text_objects("Pause", self.smallText, ORANGE)
        
        pause_rect.center = ((PAUSE_X+(PAUSE_WIDTH/2)), (PAUSE_Y+(PAUSE_HEIGHT/2)) )
        self.gameDisplay.blit(text_pause, pause_rect)
        
        # stop
        if STP_X+STP_WIDTH > self.mouse[0] > STP_X and STP_Y+STP_HEIGHT > self.mouse[1] > STP_Y:

            pygame.draw.rect(self.gameDisplay, BRIGHT_RED,(STP_X,STP_Y,STP_WIDTH,STP_HEIGHT))
            text_stp, stp_rect = self.text_objects("Stop", self.smallText, BLACK)

            if self.click[0] == 1:
                self.music.stop()

        else:
            pygame.draw.rect(self.gameDisplay, BRIGHT_RED,(STP_X,STP_Y,STP_WIDTH,STP_HEIGHT), 1) 
            text_stp, stp_rect = self.text_objects("Stop", self.smallText, BRIGHT_RED)
        stp_rect.center = ((STP_X+(STP_WIDTH/2)), (STP_Y+(STP_HEIGHT/2)) )
        self.gameDisplay.blit(text_stp, stp_rect)

    def set_menu_bar(self):
        self.ev = event.wait()

        if self.ms:
            display.update(self.ms.update(self.ev))
            if self.ms.choice:
                self.B_ms_func, self.S_ms_func = self.ms.choice_index[0], self.ms.choice_index[1]
                print("menu")
                print(self.B_ms_func, self.S_ms_func)
                self.click_func = True
        else:
            display.update(self.bar.update(self.ev))
            if self.bar.choice:
                self.B_bar_func, self.S_bar_func = self.bar.choice_index[0], self.bar.choice_index[1]
                print("bar")
                print(self.B_bar_func, self.S_bar_func)
                self.click_func = True


    def set_back_button(self):

        if BACK_X+BACK_WIDTH > self.mouse[0] > BACK_X and BACK_Y+BACK_HEIGHT > self.mouse[1] > BACK_Y:
            pygame.draw.rect(self.gameDisplay, WHITE ,(BACK_X,BACK_Y,BACK_WIDTH,BACK_HEIGHT))
            textBack, recBack = self.text_objects("Back", self.smallText, BLACK)
            if self.click[0] == 1:
                # self.recording = False
                self.click_func = False
                self.isValid = False
                self.music_found = False
                self.recording = False
                self.is_predicted = False
                self.is_recorded = False
                if self.is_music_load:
                    self.music.stop()
                self.is_music_load = False

                #--------new var-------
                # self.music_in_database = False
                # self.music_found = False
                # self.need_reselect = False
                self.is_file_selected = False


        else:
            pygame.draw.rect(self.gameDisplay, WHITE,(BACK_X,BACK_Y,BACK_WIDTH,BACK_HEIGHT), 1)
            textBack, recBack = self.text_objects("Back", self.smallText, WHITE)

        recBack.center = ((BACK_X+(BACK_WIDTH/2)), (BACK_Y+(BACK_HEIGHT/2)) )
        self.gameDisplay.blit(textBack, recBack)


    def set_classify(self):
        predText = pygame.font.Font(RESULT_FONT,48)

        # file select output
        if self.is_file_selected:
            self.play_music_buttons(self.data_source)

        # control buttons (mic output)
        if self.is_recorded:
            self.play_music_buttons(WAVE_OUTPUT_FILENAME)

        # Classification process
        if CLF_X+CLF_WIDTH > self.mouse[0] > CLF_X and CLF_Y+CLF_HEIGHT > self.mouse[1] > CLF_Y \
            and not self.recording:
            
            pygame.draw.rect(self.gameDisplay, BRIGHT_BLUE,(CLF_X,CLF_Y,CLF_WIDTH,CLF_HEIGHT))

            if self.click[0] == 1 :
                if not self.is_predicted:
                    self.is_classify = True

            if self.is_classify:

                text_clf, clf_rect = self.text_objects("Trying...", self.smallText, BG_COLOR)
            else:
                text_clf, clf_rect = self.text_objects("Classify", self.smallText, BG_COLOR)

            clf_rect.center = ((CLF_X+(CLF_WIDTH/2)), (CLF_Y+(CLF_HEIGHT/2)) )
            self.gameDisplay.blit(text_clf, clf_rect)

            # if is_predicted:

            if not self.is_predicted:
                display.flip()

            if self.is_classify is True:
                self.is_classify = False

                self.predict = self.clf.predict(WAVE_OUTPUT_FILENAME)
                self.is_predicted = True
                print self.predict
            # print self.is_classify

        else:
            pygame.draw.rect(self.gameDisplay, BRIGHT_BLUE,(CLF_X,CLF_Y,CLF_WIDTH,CLF_HEIGHT), 1) 
            if self.is_classify:
                text_clf, clf_rect = self.text_objects("Trying...", self.smallText, BRIGHT_BLUE)
            else:
                text_clf, clf_rect = self.text_objects("Classify", self.smallText, BRIGHT_BLUE)
        
            clf_rect.center = ((CLF_X+(CLF_WIDTH/2)), (CLF_Y+(CLF_HEIGHT/2)) )
            self.gameDisplay.blit(text_clf, clf_rect)

        if self.is_predicted:
            text_clf, pred_rect = self.text_objects("Instrument: {}".format(self.predict.upper()), predText, ORANGE)
            pred_rect.center = ((self.imgwave_x - (PRED_WIDTH - self.imgwave_w) / 2+(PRED_WIDTH/2)), 
                            (self.imgwave_y + 200+(PRED_HEIGHT/2)) )
            self.gameDisplay.blit(text_clf, pred_rect)
            # pygame.draw.rect(self.gameDisplay, ORANGE,(self.imgwave_x - (PRED_WIDTH - self.imgwave_w) / 2, \
                                            # self.imgwave_y + 300, PRED_WIDTH, PRED_HEIGHT), 1)
        
    def validate_music_with_file(self,func_type):
        medText = pygame.font.Font(FONT,20)
        largeText = pygame.font.Font(FONT,36)
        if not self.isValid:
            textValidMusic= largeText.render("Please Select A File With Valid Music Type.", 1, WHITE)
            self.gameDisplay.blit(textValidMusic,(VALID_X,VALID_Y))
        else:
            # print(self.data_source)
            selectMusic= medText.render("You Selected: {}".format(self.data_source.strip().split("/")[-1]), 1, WHITE)

            self.gameDisplay.blit(selectMusic,(SELECT_X,SELECT_Y))

        if func_type == 0:
            self.is_file_selected = True

    def show_file_dialog(self):
        if (self.data_file == False):
            self.data_source = pathgetter()
            # print(self.data_source)
            if os.path.isfile(self.data_source) and (sndhdr.what(self.data_source) is not None):
                self.isValid = True
            else:
                self.isValid = False
            self.data_file = True
        # else:
        #     self.data_str = self.data_source
        # display.flip()

    def reselect(self):
        if RESELECT_X+RESELECT_WIDTH > self.mouse[0] > RESELECT_X and RESELECT_Y+RESELECT_HEIGHT > self.mouse[1] > RESELECT_Y:

            pygame.draw.rect(self.gameDisplay, BRIGHT_GRAY,(RESELECT_X,RESELECT_Y,RESELECT_WIDTH,RESELECT_HEIGHT))
            text_reselect, reselect_rect = self.text_objects("Reselect", self.smallText, BLACK)

            if self.click[0] == 1:
                self.gameDisplay.fill(BLACK)
                self.data_file = False
                self.need_reselect = True
        else:
            pygame.draw.rect(self.gameDisplay, BRIGHT_GRAY,(RESELECT_X,RESELECT_Y,RESELECT_WIDTH,RESELECT_HEIGHT), 1) 
            text_reselect, reselect_rect = self.text_objects("Reselect", self.smallText, WHITE)
        
        reselect_rect.center = ((RESELECT_X+(RESELECT_WIDTH/2)), (RESELECT_Y+(RESELECT_HEIGHT/2)) )
        self.gameDisplay.blit(text_reselect, reselect_rect)

        # display.flip()

        if self.need_reselect:

            self.need_reselect = False
            self.music_found = False
            self.data_file = False

            #--------new var-------
            self.is_file_selected = False

            # display.flip()

    def search_similar_music(self,func_type):
        # display.flip()

        if SEARCH_X+SEARCH_WIDTH > self.mouse[0] > SEARCH_X and SEARCH_Y+SEARCH_HEIGHT > self.mouse[1] > SEARCH_Y:

            pygame.draw.rect(self.gameDisplay, BRIGHT_GREEN,(SEARCH_X,SEARCH_Y,SEARCH_WIDTH,SEARCH_HEIGHT))
            text_search, search_rect = self.text_objects("Search", self.smallText, BLACK)

            if self.click[0] == 1:
                if func_type == 0:
                    msc = self.data_source.strip().split("/")[-1]
                    print(msc)
                if func_type == 1:
                    msc = WAVE_OUTPUT_FILENAME

                from search.search import Recognition
                # from dejavu import Dejavu
                # from dejavu.recognize import FileRecognizer

                # config = {"database": {"host": "127.0.0.1", "user": "root", "passwd": "", "db": "dejavu"}}
                # config = {"database": {"host": "10.66.31.157", "user": "root", "passwd": "662813", "db": "dejavu"}}
                
                # djv = Dejavu(config)

                # djv.fingerprint_directory("mp3", [".mp3"], 3)

                # self.dbMusic = djv.recognize(FileRecognizer, msc)
                g = Recognition()
                self.dbMusic = g.dejavu(msc)

                if self.dbMusic != "":
                    self.music_found = True

                for k in [x for x in sys.modules.keys() if x.startswith('search.')]:
                    del sys.modules[k]
                del sys.modules['search']
                # del dejavu
                
        else:
            pygame.draw.rect(self.gameDisplay, BRIGHT_GREEN,(SEARCH_X,SEARCH_Y,SEARCH_WIDTH,SEARCH_HEIGHT), 1) 
            text_search, search_rect = self.text_objects("Search", self.smallText, BRIGHT_GREEN)
        
        search_rect.center = ((SEARCH_X+(SEARCH_WIDTH/2)), (SEARCH_Y+(SEARCH_HEIGHT/2)) )
        self.gameDisplay.blit(text_search, search_rect)

        if self.music_found:
            textDatabaseMusic= self.smallText.render("The Relevant Music Found in Database:", 1, WHITE)
            self.dbMusicName = self.dbMusic['song_name']
            textDBMusicResult = self.smallText.render("{}".format(self.dbMusicName), 1, WHITE)
            print(self.dbMusicName)
            self.gameDisplay.blit(textDatabaseMusic,(DBMUSIC_X,DBMUSIC_Y))
            self.gameDisplay.blit(textDBMusicResult,(DBMUSIC_X,DBMUSIC_Y+30))

            # print ("wav/{}.wav".format(self.dbMusicName))

            self.play_music_buttons(os.path.join('wav',"{}.wav".format(self.dbMusicName)))

        # del(sys.modules[mod] for mod in sys.modules.keys() if mod.startswith('Recognition'))

    def search_event_handle(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); 
                sys.exit()

    def set_functionality_screen(self):
        
        # instrument
        largeText = pygame.font.Font(FONT,36)
        if self.B_bar_func == 0:
            if self.S_bar_func is 0:
                self.gameDisplay.fill(BLACK)
                # print "HELLO WORLD2"
                self.show_file_dialog()
                self.validate_music_with_file(0)
                self.set_back_button()
                if self.isValid:
                    # self.reselect()
                    self.set_classify()
                    display.flip()

            elif self.S_bar_func is 1:
                self.gameDisplay.fill(BG_COLOR)
                self.record_screenloop()
                self.loop_record()
                self.stop_record()
                # self.set_back_button()
                self.set_classify()

            elif self.S_bar_func is 2:
                print "HELLO WORLD"
                self.click_func = False

        # Searching functionality:
        elif self.B_bar_func == 1:
            #search with file
            if self.S_bar_func is 0:
                self.gameDisplay.fill(BLACK)
                # print "HELLO WORLD2"
                self.show_file_dialog()
                self.validate_music_with_file(1)
                self.set_back_button()
                if self.isValid:
                    self.search_similar_music(0)
                    # self.reselect()
                    display.flip()

            #search with mic
            elif self.S_bar_func is 1:
                self.gameDisplay.fill(BLACK)
                self.record_screenloop()
                self.loop_record()
                self.stop_record()
                # print(self.music_found)
                self.search_similar_music(1)
                display.flip()
                    # self.reselect()
                
                # self.set_back_button()

            #about
            elif self.S_bar_func is 2:
                print "HELLO WORLD"
                self.click_func = False

        # Similarity
        elif self.B_bar_func == 2:
            if self.S_bar_func is 0:
                print "HELLO WORLD"
                self.click_func = False
            elif self.S_bar_func is 1:
                print "HELLO WORLD"
                self.click_func = False

        # System
        elif self.B_bar_func == 3:
            if self.S_bar_func == 0:
                sys.exit(0)
            elif self.S_bar_func is 1:
                print "HELLO WORLD"
                self.click_func = False

        # # Recognizing Functionality:
        # if self.B_bar_func == 1:
        #     if self.S_bar_func == 0:

        # # Checking Functionality:
        # if self.B_bar_func == 2:
        #     if self.S_bar_func == 0:

    def __init__(self):

        # basic settups
        pygame.init()

        self.clf = Classify()
        self.click_func = False
        self.init = False

        self.is_classify = False
        self.is_predicted = False
        self.pred_play = False
        self.is_recorded = False
        self.is_music_load = False
        self.is_paused = False

        self.data_file = False
        self.isValid = False

        #--------new var-------
        self.music_in_database = False
        self.music_found = False
        self.need_reselect = False
        self.is_file_selected = False

        self.smallText = pygame.font.Font(FONT,16)

        self.imgwave = GIFImage("resource/wave1.gif")
        self.imgwave_w, self.imgwave_h = self.imgwave.image.size

        self.music = mixer.music

        # setting bacground
        self.bg = image.load(BACKGROUND_IMG)
        self.bg_w, self.bg_h = self.bg.get_size()

        self.imgwave_x, self.imgwave_y = self.bg.get_size()[0] / 2 - self.imgwave_w / 2,\
                                         self.bg.get_size()[1] / 2 - self.imgwave_h / 2 - 60
        print self.imgwave_y

    def main_loop(self):

        while True:

            self.search_event_handle()

            self.mouse = pygame.mouse.get_pos()
            self.click = pygame.mouse.get_pressed()

            if self.click_func == False:
                if self.init == False:
                    # background setup
                    self.initialise_background()
                    # initialise menu system
                    self.initialise_menu()
                    # recording variables setup
                    self.set_recording_variables()
                    self.init = True
                # set menu bar
                self.set_menu_bar()
                self.data_file = False
                # exit the app
                # if self.exit_button.update(self.ev):
                #     if self.exit_button.clicked: break
                display.flip()
            else:
                self.set_functionality_screen()
                self.init = False

            display.update()

                
if __name__ == "__main__":
    g = Gui()
    g.main_loop()
