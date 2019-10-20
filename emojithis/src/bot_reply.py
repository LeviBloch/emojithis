#!/usr/bin/python
import praw
import re
import random
import json
import os
import time

dictionaryFile = "dictionary.json"
submissionsRepliedToFile = "submissions_replied_to.json"

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("emojipasta")
keyphrase = "!emojithis"

# load list of posts replied to
if os.path.isfile(submissionsRepliedToFile):
    with open(submissionsRepliedToFile, 'r') as fp:
        submissionsRepliedTo = json.load(fp)
else:
    submissionsRepliedTo = []

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


# loop through new comments in subreddit
for comment in subreddit.stream.comments():
    
    # check if comment contains keyphrase
    if re.search(keyphrase, comment.body, re.IGNORECASE):
        
        # check if bot has already replied to submission
        if comment.id in submissionsRepliedTo:
            continue
        
        # get text of parent
        if (comment.is_root):
            parentText = comment.parent().selftext
        else:
            parentText = comment.parent().body
            
        # generate reply using parent
        reply = generateReply(parentText)

        # make sure that there isn't an exception due to posting too often
        canPost = False
        while canPost == False:
            try:
                comment.reply(reply)
                canPost = True
            except (praw.exceptions.APIException):
                time.sleep(60)

        print(reply)
        print("------------------------------------------------------------------------")
        
        # save comment id to list of submissions that have been replied to by the bot
        submissionsRepliedTo.append(comment.id)
        with open(submissionsRepliedToFile, 'w') as fp:
            json.dump(submissionsRepliedTo, fp)



