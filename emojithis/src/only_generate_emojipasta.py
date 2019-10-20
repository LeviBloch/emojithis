import random
import json
import os

dictionaryFile = "dictionary.json"

# load dictionary
if os.path.isfile(dictionaryFile):
    with open(dictionaryFile, 'r') as fp:
        dic = json.load(fp)
else:
    dic = {}
    print("NO DICTIONARY FOUND! CONTINUING WITHOUT DICTIONARY.")

def generateReply(text):
    output = ""
    # split text into words
    textList = text.split(" ")
    # for each word
    for word in textList:
        # add word to output
        output += word + " "
        # if dictionary has word
        if word in dic.keys():
            # add 1-3 emojis after word
            for i in range(random.randint(1,3)):
                output += random.choice(dic[word])
            output += " "

    return output

input = input("Enter original message: ")
print(generateReply(input))
