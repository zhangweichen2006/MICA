from classify import * 


clf = Classify()

pred = clf.predict('../test_data/output.wav')
print 'the prediction is:', pred

pred_prob = clf.predict_prob('../test_data/output.wav')
print 'probability for each class:', pred_prob