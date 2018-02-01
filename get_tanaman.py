import json
from tokenizer import tokenize
dictionary = json.load(open('list_tanaman.csv')) # plant
def get_tanaman(sentence):
    tokenizedSentence = tokenize(sentence)
    list = []
    tanaman = ""
    for i in xrange(len(tokenizedSentence)):
        if tokenizedSentence[i] in dictionary['plant']:
            tanaman = tokenizedSentence[i]
            if i+1 < len(tokenizedSentence) and (tanaman in dictionary) and (tokenizedSentence[i+1] in dictionary[tanaman]):
                tanaman += " " + tokenizedSentence[i+1]
                i += 1
            if tanaman not in list:
                list.append(tanaman)
    return list

print get_tanaman("Supaya Durian Pohonnya pendek tapi berbuahnya lebat gimana ya? kalo bawang merah gimana apa lagi apel")
