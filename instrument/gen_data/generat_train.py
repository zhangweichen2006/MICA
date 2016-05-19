from utils import Generator


''' Absolute path to the raw audios '''
PIANO_PATH_MP3 = '../raw_data/mp3/piano/'
PIANO_PATH_WAV = '../raw_data/wav/piano/'

DHOL_PATH_MP3 = '../raw_data/mp3/dhol/'
DHOL_PATH_WAV = '../raw_data/wav/dhol/'

VIOLIN_PATH_MP3 = '../raw_data/mp3/violin/'
VIOLIN_PATH_WAV = '../raw_data/wav/violin/'

# initilize the generator for converting raw audio into mfcc
train_data = Generator()

''' generating data into the training set '''
# Piano
train_data.process_audio(PIANO_PATH_WAV, PIANO_PATH_MP3, 'piano')

# Dhol
train_data.process_audio(DHOL_PATH_WAV, DHOL_PATH_MP3, 'dhol')

# Violin
train_data.process_audio(VIOLIN_PATH_WAV, VIOLIN_PATH_MP3, 'violin')

''' finallize and output '''
train_data.output('train.csv')