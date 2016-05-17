from classify import * 


clf = Classify()

pred = clf.predict('../test_data/Kiss_The_Rain.wav')
print 'the prediction is:', pred

pred_prob = clf.predict_prob('../test_data/Kiss_The_Rain.wav')
print 'probability for each class:', pred_prob