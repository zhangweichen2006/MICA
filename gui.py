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


# Background Setup
BACKGROUND_IMG = 'resource/python4.jpg'
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

FONT = "MenuSystem/Roboto-Regular.ttf"

# Recording Configs
CHUNK = 2048
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
BRIGHT_BLUE = (0,102,204)
HALF_DARK_BLUE = (0,76,153)
FONT_BLUE = (51,153,255)

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

# sound wave jif
# WAVES = [Image.open(join(WAVE_PATH, f)) for f in listdir(WAVE_PATH) if isfile(join(WAVE_PATH, f)) and "wave" in f]
# IMG = [pygame.Surface.fromstring(w, (220,60), "P") for w in WAVES]

# print WAVES
# print IMG
# pygame.transform.scale(pygame.image.load(w), (600, 70))

class Gui(object):

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def initialise_background(self):
        # background setup
        pygame.display.set_caption('Music Identification and Classification Application (MICA)')
        bg = image.load(BACKGROUND_IMG)

        self.imgwave_x, self.imgwave_y = bg.get_size()[0] / 2 - self.imgwave_x / 2,\
                                         bg.get_size()[1] / 2 - self.imgwave_y / 2

        self.gameDisplay = display.set_mode(bg.get_size())
        self.scrrect = self.gameDisplay.blit(bg,(0,0))
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
        self.bar.set((self.search_menu, self.recognize_menu, self.accuracy_check_menu, self.exit))
        display.update(self.bar)

        self.ms = MenuSystem.MenuSystem()

        # self.exit_button = MenuSystem.Button('EXIT',100,30)
        # self.exit_button.bottomright =  self.scrrect.w-20,self.scrrect.h-20
        # self.exit_button.set()

    def record_screenloop(self):

        smallText = pygame.font.Font(FONT,16)

        # mouse on GREEN show record button
        if RECORD_X+RECORD_WIDTH > self.mouse[0] > RECORD_X and RECORD_Y+RECORD_HEIGHT > self.mouse[1] > RECORD_Y \
            and not self.recording:

            pygame.draw.rect(self.gameDisplay, BRIGHT_RED,(RECORD_X,RECORD_Y,RECORD_WIDTH,RECORD_HEIGHT))
            textRecord, recRect = self.text_objects("Record", smallText, BLACK)
            if self.click[0] == 1 :
                if self.recording == False:
                    self.open_record()
                    self.recording = True  
                self.record_once = True
        else:
            pygame.draw.rect(self.gameDisplay, BRIGHT_RED,(RECORD_X,RECORD_Y,RECORD_WIDTH,RECORD_HEIGHT), 1)
            textRecord, recRect = self.text_objects("Record", smallText, BRIGHT_RED)

        
        
        recRect.center = ( (RECORD_X+(RECORD_WIDTH/2)), (RECORD_Y+(RECORD_HEIGHT/2)) )
        self.gameDisplay.blit(textRecord, recRect)

        # mouse on RED stop record button
        if STOP_X+STOP_WIDTH > self.mouse[0] > STOP_X and STOP_Y+STOP_HEIGHT > self.mouse[1] > STOP_Y \
            and self.recording:

            pygame.draw.rect(self.gameDisplay, BRIGHT_GRAY,(STOP_X,STOP_Y,STOP_WIDTH,STOP_HEIGHT))
            textStop, stopRect = self.text_objects("Stop", smallText, BLACK)
        else:
            pygame.draw.rect(self.gameDisplay, BRIGHT_GRAY,(STOP_X,STOP_Y,STOP_WIDTH,STOP_HEIGHT), 1) 
            textStop, stopRect = self.text_objects("Stop", smallText, BRIGHT_GRAY)

        
        stopRect.center = ((STOP_X+(STOP_WIDTH/2)), (STOP_Y+(STOP_HEIGHT/2)) )
        self.gameDisplay.blit(textStop, stopRect)

        # back button
        if BACK_X+BACK_WIDTH > self.mouse[0] > BACK_X and BACK_Y+BACK_HEIGHT > self.mouse[1] > BACK_Y:
            pygame.draw.rect(self.gameDisplay, WHITE ,(BACK_X,BACK_Y,BACK_WIDTH,BACK_HEIGHT))
            textBack, recBack = self.text_objects("Back", smallText, BLACK)
            if self.click[0] == 1:
                self.recording = False
                self.click_func = False
        else:
            pygame.draw.rect(self.gameDisplay, WHITE,(BACK_X,BACK_Y,BACK_WIDTH,BACK_HEIGHT), 1)
            textBack, recBack = self.text_objects("Back", smallText, WHITE)

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
            if STOP_X+STOP_WIDTH > self.mouse[0] > STOP_X and STOP_Y+STOP_WIDTH > self.mouse[1] > STOP_Y and self.recording and self.click[0] == 1 :
                print("* done recording")

                self.stream.stop_stream()
                self.stream.close()

                self.wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                self.wf.setnchannels(CHANNELS)
                self.wf.setsampwidth(self.p.get_sample_size(FORMAT))
                self.wf.setframerate(RATE)
                self.wf.writeframes(b''.join(self.frames))
                
                self.recording = False
                smallText = pygame.font.Font(FONT,16)
                text_clf, clf_rect = self.text_objects("Classify", smallText, HALF_DARK_BLUE)
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


    # def set_back_button(self):

    #     smallText = pygame.font.Font(FONT,16)

    #     if BACK_X+BACK_WIDTH > self.mouse[0] > BACK_X and BACK_Y+BACK_HEIGHT > self.mouse[1] > BACK_Y:
    #         pygame.draw.rect(self.gameDisplay, WHITE ,(BACK_X,BACK_Y,BACK_WIDTH,BACK_HEIGHT))
    #         textBack, recBack = self.text_objects("Back", smallText, BLACK)
    #         if self.click[0] == 1:
    #             self.recording = False
    #             self.click_func = False
    #     else:
    #         pygame.draw.rect(self.gameDisplay, WHITE,(BACK_X,BACK_Y,BACK_WIDTH,BACK_HEIGHT), 1)
    #         textBack, recBack = self.text_objects("Back", smallText, WHITE)

    #     recBack.center = ((BACK_X+(BACK_WIDTH/2)), (BACK_Y+(BACK_HEIGHT/2)) )
    #     self.gameDisplay.blit(textBack, recBack)


    def set_classify(self):
        smallText = pygame.font.Font(FONT,16)
        if CLF_X+CLF_WIDTH > self.mouse[0] > CLF_X and CLF_Y+CLF_HEIGHT > self.mouse[1] > CLF_Y \
            and not self.recording:
            

            pygame.draw.rect(self.gameDisplay, BRIGHT_BLUE,(CLF_X,CLF_Y,CLF_WIDTH,CLF_HEIGHT))

            if self.click[0] == 1 :
                self.is_classify = True

            if self.is_classify:

                text_clf, clf_rect = self.text_objects("Trying...", smallText, BLACK)
            else:
                text_clf, clf_rect = self.text_objects("Classify", smallText, BLACK)

            clf_rect.center = ((CLF_X+(CLF_WIDTH/2)), (CLF_Y+(CLF_HEIGHT/2)) )
            self.gameDisplay.blit(text_clf, clf_rect)

            display.flip()

            if self.is_classify is True:
                self.is_classify = False
                self.predict = self.clf.predict(WAVE_OUTPUT_FILENAME)
                print self.predict
            # print self.is_classify

        else:
            pygame.draw.rect(self.gameDisplay, BRIGHT_BLUE,(CLF_X,CLF_Y,CLF_WIDTH,CLF_HEIGHT), 1) 
            if self.is_classify:
                text_clf, clf_rect = self.text_objects("Trying...", smallText, BRIGHT_BLUE)
            else:
                text_clf, clf_rect = self.text_objects("Classify", smallText, BRIGHT_BLUE)
        
            clf_rect.center = ((CLF_X+(CLF_WIDTH/2)), (CLF_Y+(CLF_HEIGHT/2)) )
            self.gameDisplay.blit(text_clf, clf_rect)


    def set_functionality_screen(self):

        # Searching functionality:
        if self.B_bar_func == 0:
            if self.S_bar_func is 0:
                print "HELLO WORLD"
                self.click_func = False

            elif self.S_bar_func is 1:
                self.gameDisplay.fill(BLACK)
                self.record_screenloop()
                self.loop_record()
                self.stop_record()
                # self.set_back_button()


            elif self.S_bar_func is 2:
                print "HELLO WORLD"
                self.click_func = False

        # instrument
        elif self.B_bar_func == 1:
            if self.S_bar_func is 0:
                print "HELLO WORLD"
                self.click_func = False

            elif self.S_bar_func is 1:
                self.gameDisplay.fill(BLACK)
                self.record_screenloop()
                self.loop_record()
                self.stop_record()
                # self.set_back_button()
                self.set_classify()

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

        pygame.init()

        self.clf = Classify()
        self.click_func = False
        self.init = False

        self.is_classify = False

        self.imgwave = GIFImage("resource/wave1.gif")
        self.imgwave_x, self.imgwave_y = self.imgwave.image.size
        


    def main_loop(self):

        while True:

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
