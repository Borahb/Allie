import pickle
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import numpy as np
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
import speech_recognition as sr
lis = sr.Recognizer()


import discord
import os
import requests
import nest_asyncio
nest_asyncio.apply()







intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res



#def chat():
 #    print("Start talking with the bot (type quit to stop)!")
#       while True:
#         inp = input("You:")
#         if inp.lower() == "quit":
#            break
#         results = chatbot_response(inp)
#         print(results)
        
#chat()

#def voice_input():           
#    with sr.Microphone() as source:
#        print('listening.....')
#        voice = lis.listen(source)
#        command = lis.recognize_google(voice)
#        print(command)

#voice_input()   
      
        
        
client = discord.Client()    

@client.event
async def on_ready():
  print('We have logged in !')
  general_channel = client.get_channel(803876773360041997)
  await general_channel.send('Hello Everyone !')
  
  
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msgc = message.content  
  inp = msgc
  results = chatbot_response(inp)         
  general_channel = client.get_channel(803876773360041997)
  await general_channel.send(results)
         
                          
client.run('ODAzODY1OTg4NzU1NzUwOTQy.YBEAig.ZE7ZAa1Eo6pUBa7f14_MKYEXU5c') 
        
        
        
        