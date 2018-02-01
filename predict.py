import pandas
import numpy
from tobow import tobow
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

topic_model_path = "classifier/topic/classifier.json"
topic_weights_path = "classifier/topic/weights.h5"
topic_encoder_path = "classifier/topic/encoder.npy"

intent_model_path = "classifier/intent/classifier.json"
intent_weights_path = "classifier/intent/weights.h5"
intent_encoder_path = "classifier/intent/encoder.npy"

def predict(sentence):
    # load class encoder
    topic_encoder = LabelEncoder()
    topic_encoder.classes_ = numpy.load(topic_encoder_path)
    json_file = open(topic_model_path, "r")
    topic_loaded_model_json = json_file.read()
    json_file.close()
    #=============================#
    intent_encoder = LabelEncoder()
    intent_encoder.classes_ = numpy.load(intent_encoder_path)
    json_file = open(intent_model_path, "r")
    intent_loaded_model_json = json_file.read()
    json_file.close()
    
    # load classifier model
    topic_model = model_from_json(topic_loaded_model_json)
    topic_model.load_weights(topic_weights_path)
    topic_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    #=============================#
    intent_model = model_from_json(intent_loaded_model_json)
    intent_model.load_weights(intent_weights_path)
    intent_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    vector = tobow(sentence)
    topic_predict = topic_model.predict(numpy.array([vector[0]]))
    topic_index = numpy.argmax(topic_predict[0])
    intent_predict = intent_model.predict(numpy.array([vector[0]]))
    intent_index = numpy.argmax(intent_predict[0])

    return intent_encoder.classes_[intent_index], topic_encoder.classes_[topic_index]