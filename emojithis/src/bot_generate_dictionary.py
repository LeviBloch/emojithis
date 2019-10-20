#!/usr/bin/python
import praw
import emoji
import json
import os

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("emojipasta")

dictionaryFile = 'dictionary.json'
submissionsReadFile = 'submissions_read.json'

def containsEmojis(text):
    for character in text:
        # TODO find a cleaner way to determine if a character is an emoji
        if (emoji.demojize(character) != character) & (emoji.emojize(emoji.demojize(character)) == character):
            return True
    return False

def extractEmojis(text):
    output = []
    for character in text:
        if containsEmojis(character):
            output.append(character)
    return output

# load dictionary where keys are words and values are lists of emojis
if os.path.isfile(dictionaryFile):
    with open(dictionaryFile, 'r') as fp:
        dic = json.load(fp)
else:
    dic = {}

# Load file to check if submissions have already been read by bot
if os.path.isfile(submissionsReadFile):
    with open(submissionsReadFile, 'r') as fp:
        submissionsRead = json.load(fp)
        #submissionsRead = submissionsRead.split(\n)
        #submissionsRead = list(filter(None, submissionsRead))
else:
    submissionsRead = []

# loop through newest submissions
for submission in subreddit.new(limit=1000):
    # make sure submission hasn't been viewed by bot before
    if submission.id in submissionsRead:
        continue

    # check if submission has a body
    text = submission.selftext
    if text == "":
        continue

    #convert text to all lower case
    text = text.lower()

    # split text into list of words
    textList = text.split()

    # loop through words
    for i in range(len(textList) - 1):
        word = textList[i]

        # if the word contains no emojis
        if containsEmojis(word) == False:

            # get emojis in next word
            nextEmojis = extractEmojis(list(textList[i+1]))

            # add word to dic as key, add emoji to list of values
            for e in nextEmojis:
                dic.setdefault(word, []).append(e)

    # mark submission as read
    submissionsRead.append(submission.id)

# save dictionary as json
with open(dictionaryFile, 'w') as fp:
    json.dump(dic, fp)

# save list of submissions that have been read by the bot
with open(submissionsReadFile, 'w') as fp:
    json.dump(submissionsRead, fp)

