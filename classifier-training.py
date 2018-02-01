import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from tobow import tobow

numpy.random.seed(7)

model_path = "classifier/topic/classifier.json"
weights_path = "classifier/topic/weights.h5"
encoder_path = "classifier/topic/encoder.npy"

test_data_path = "resources/intent/data-test.csv"
test_label_path = "resources/intent/label-test.csv"

X_dataframe = pandas.read_csv("resources/intent/data-training.csv", header=None)
X = X_dataframe.values
Y_dataframe = pandas.read_csv("resources/intent/label-training.csv", header=None)
Y = Y_dataframe.values

dummy_x = []
for text in X:
	dummy_x.append(numpy.array(tobow(text[0])[0]))

bow = numpy.array(dummy_x)

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
numpy.save(encoder_path,encoder.classes_)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

# define baseline model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(5000, input_shape=(len(bow[0]),), activation='relu'))
	model.add(Dropout(0.2))
	model.add(Dense(4, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

model = baseline_model()

#training process
model.fit(bow, dummy_y, epochs=30)

#Save to Json
model_json = model.to_json()
with open(model_path, "w") as json_file:
    json_file.write(model_json)
model.save_weights(weights_path)
print "Model has been saved"

from evaluate import evaluate

evaluate(model_path, weights_path, test_data_path, test_label_path, encoder_path)