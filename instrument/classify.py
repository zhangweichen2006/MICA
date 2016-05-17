import numpy as np
import pandas as pd
import scipy.io.wavfile as wav
import sys

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC, SVC
# sys.path.append('../../raw_data/')

from utils import mfcc, trim


''' class to be called in the GUI '''
class Classify:
    
    def __init__(self):
        print 'Initializing...'
        data_pd = pd.read_csv('train.csv', delimiter=',')
        data = data_pd.values
        # print data
        X = data[:,1:data.shape[1]-1]
        y = data[:,data.shape[1]-1]
        print X.shape
        # print y

        self.clf = RandomForestClassifier(n_estimators=100)
        # self.clf = SVC(kernel='linear', C=1.0, probability=True)
        self.clf.fit(X, y)

        # print 'loading training data...DONE'


    # predict the audio file with '.wav' format
    def predict(self, X):
        # if '.wav' in filenm:
        print 'Predicting...'
        sample_rate, signal = wav.read(X)
        signal = trim(signal)
        coefs = mfcc(signal, samplerate=sample_rate, winlen=0.025, winstep=0.01,
            ncoef=13, nfilter=26, nfft=2048, lof=0, hif=None, preem=0.97, lift=22)
        test = np.mean(coefs, axis=0)
        test = test.reshape(1, -1)

        return self.clf.predict(test)[0]

    def predict_prob(self, X):
        sample_rate, signal = wav.read(X)
        signal = trim(signal)
        coefs = mfcc(signal, samplerate=sample_rate, winlen=0.025, winstep=0.01,
            ncoef=13, nfilter=26, nfft=2048, lof=0, hif=None, preem=0.97, lift=22)
        test = np.mean(coefs, axis=0)
        test = test.reshape(1, -1)

        return self.clf.predict_proba(test)[0]

