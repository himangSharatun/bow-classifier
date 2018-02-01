from sklearn.feature_extraction.text import CountVectorizer
from tokenizer import tokenizeSentence as tokenize
import csv
import json

sentences = []

with open('resources/8village/data-only-250.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        sentences.append(tokenize(row[0]))

print sentences[0:5]
 
vectorizer = CountVectorizer()
vectorizer.fit_transform(sentences).todense() 

with open ('vocabulary.json', 'w') as vocabFile:
    json.dump(vectorizer.vocabulary_ , vocabFile)

# print vectorizer.transform(["Mau tanya pak  pupuk apa ya buat memperbesar bunga nya."]).toarray()
# print vectorizer
