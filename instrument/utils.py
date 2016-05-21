import numpy as np
from pydub import AudioSegment
import decimal
import math
import pandas as pd
from collections import defaultdict

from os import listdir
from os.path import isfile, join
import sys

from scipy.io import loadmat
from scipy.fftpack import dct
import scipy.io.wavfile as wav


''' Processing raw data and generate the training data in terms of mfcc '''
class Generator:

    def __init__(self):
        self.trainings = defaultdict(list)


    def process_audio(self, wavpath, mp3path, typenm):
        print 'Processing {}...'.format(typenm)
        if mp3path is not None and listdir(wavpath) == []:
            print 'Convert to wav...'
            audios_mp3 = [join(mp3path, f) for f in listdir(mp3path) \
                        if isfile(join(mp3path, f))]

            for audio in audios_mp3:
                if '.mp3' in audio:
                    # print audio
                    mp3_to_wav(audio, typenm)

        audios = [join(wavpath, f) for f in listdir(wavpath) \
                    if isfile(join(wavpath, f)) and '.wav' in f]

        for i, audio in enumerate(audios):

            sys.stdout.write('\rProgress: {}/{}'.format(i, len(audios) - 1))
            sys.stdout.flush()
            sample_rate, signal = wav.read(audio)
            signal = trim(signal)
            coefs = mfcc(signal, samplerate=sample_rate, winlen=0.025, winstep=0.01,
                ncoef=13, nfilter=26, nfft=2048, lof=0, hif=None, preem=0.97, lift=22)

            features = np.mean(coefs, axis=0)
            for i, fe in enumerate(features):
                self.trainings[i].append(fe)
            self.trainings['class'].append(typenm)
        print
        print 'Processing {}...DONE'.format(typenm)


    def output(self, filenm):
        result_training = pd.DataFrame(self.trainings)
        result_training.to_csv(filenm)


''' compute mfcc of a signal '''
def mfcc(signal, samplerate=16000, winlen=0.025, winstep=0.01,
    ncoef=13, nfilter=26, nfft=512, lof=0, hif=None, preem=0.97,
    lift=20):
    
    features, energy = generate_filter_bank_and_energy(signal, samplerate, winlen,
                                                        winstep, nfilter, nfft, lof,
                                                        hif, preem)
    # print features
    features = np.log(features)
    features = dct(features, type=2, axis=1, norm='ortho')[:,:ncoef]
    features = lifter(features, lift)
    
    # replace first coefficient with log of frame energy
    features[:, 0] = np.log(energy)

    return features


''' compute the filter bank and energy '''
def generate_filter_bank_and_energy(signal, samplerate=16000, winlen=0.25,
    winstep=0.01, nfilter=26, nfft=512, lof=0, hif=None, preem=0.97):
    # print 'generating...'
    high_freq = samplerate/2
    signal = pre_emphasis(signal, preem)
    frame_size = winlen * samplerate
    frame_gap = winstep * samplerate
    frames = frame_signal(signal, frame_size, frame_gap)

    # generate power spectrum
    power_spec = power_spectrum(frames, nfft)

    # compute energy in frames
    energy = np.sum(power_spec, 1)
    energy = np.where(energy == 0, np.finfo(float).eps, energy) # make sure no 0s

    filter_bank = filter_banks(nfilter, nfft, samplerate, lof, high_freq)
    features = np.dot(power_spec, filter_bank.T)
    features = np.where(features <= 0, np.finfo(float).eps, features) # make sure no 0s

    return features, energy


''' generate mel filter bank '''
def filter_banks(nfilter=26, nfft=512, samplerate=16000, lof=0, hif=None):
    high_freq = samplerate / 2

    # compute lower and higher freqencies and even spaced
    low_mel = f2mel(lof)
    high_mel = f2mel(high_freq)
    mel_linsp = np.linspace(low_mel, high_mel, nfilter+2)

    # from freq to fft bin
    fft_bin = np.floor((nfft + 1) * mel2f(mel_linsp) / samplerate)
    filter_bank = np.zeros([nfilter, nfft / 2 + 1])

    for i in xrange(0, nfilter):
        for j in xrange(int(fft_bin[i]), int(fft_bin[i + 1])):
            filter_bank[i, j] = (i - fft_bin[i]) / (fft_bin[i + 1] - fft_bin[i])

        for j in xrange(int(fft_bin[i + 1]), int(fft_bin[i + 2])):
            filter_bank[i, j] = (fft_bin[i + 2] - i) / (fft_bin[i + 2] - fft_bin[i + 1])

    return filter_bank


''' Lifter of the magnitude of the high frequency DCT coefficients '''
def lifter(features, n=22):
    nframe, ncoef = np.shape(features)
    sp = np.arange(ncoef)
    lift = 1 + (n / 22) * np.sin(np.pi * sp / n)

    return lift * features


''' strip the audio in case it is too big'''
def trim(signal):
    return signal[:30000,:]


''' Pre-emphasis on the signal'''
def pre_emphasis(signal, coef=0.97):
    return np.append(signal[0], signal[1:]-coef*signal[:-1])


'''Coversion between freq and mel freq'''
def f2mel(f):
    return 1127.01048 * np.log(f / 700 + 1)


def mel2f(m):
    return (np.exp(m / 1127.01048) - 1) * 700


''' Frame the signal according to the window size and gap'''
def frame_signal(signal, framesize, framegap):
    signal_len = len(signal)
    frame_len = int(roundup(framesize))
    frame_step = int(roundup(framegap))

    if signal_len <= frame_len:
        num_frame = 1
    else:
        num_frame = 1 + int(math.ceil((1.0 * signal_len - framesize / framegap)))

    tmp_len = int((num_frame - 1) * framegap + framesize)
    tmp_signal = np.concatenate((signal, np.zeros((tmp_len - signal_len),)))
    
    # find the frames
    a = np.tile(np.arange(0, frame_len), (num_frame, 1))
    b = np.tile(np.arange(0, num_frame * framegap, framegap), (frame_len, 1)).T
    # print signal_len
    # print num_frame
    # print tmp_signal.shape
    indices = a + b
    indices = np.array(indices, dtype=np.int32)
    frames = tmp_signal[indices-1]

    return frames * np.tile(np.ones(frame_len,), (num_frame, 1))


''' generate power spectrum for frames '''
def power_spectrum(frames, nfft):
    spec = spectrum(frames, nfft)
    return 1.0 / nfft * np.square(spec)


''' generate power magnitude spectrum for frames '''
def spectrum(frames, nfft):
    spec = np.fft.rfft(frames, nfft)
    return np.absolute(spec)


''' coversion between wav and mp3 '''
def mp3_to_wav(filenm, typenm):
    name = filenm.split(".mp3")

    output = "../raw_data/wav/{}/".format(typenm)
    fname = name[0].split("/")[-1]
    output_path = "{}{}.wav".format(output, fname)

    sound = AudioSegment.from_mp3(filenm)
    sound.export(output_path, format="wav")


def roundup(number):
    return int(decimal.Decimal(number).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP))
