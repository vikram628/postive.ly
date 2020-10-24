from datetime import datetime
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

bob = [{"text": "I wanna die", "score": .51, "timestamp": 1572712674.453777},
       {"text": "I wanna die", "score": .3, "timestamp": 1572712674.453777},
       {"text": "I wanna die", "score": .52, "timestamp": 1572712674.453777},
       {"text": "I wanna die", "score": .53, "timestamp": 1572712674.453777}, 
       {"text": "I wanna die", "score": .3, "timestamp": 1572712674.453777}, 
       {"text": "I wanna die", "score": .3, "timestamp": 1572712674.453777}, 
       {"text": "I wanna die", "score": .5, "timestamp": 1572712674.453777}, 
       {"text": "I wanna live", "score": .9, "timestamp": 1572712134.453777},
       {"text": "I wanna live more", "score": .8, "timestamp": 1572710674.453777},
       {"text": "Poop", "score": .3, "timestamp": 1572702674.453777}, 
       {"text": "Poopy!", "score": .9, "timestamp": 1572702974.453777}]

def past24hrs(data):
    timestampnow = datetime.timestamp(datetime.now())
    
    #generate list of past 24 hr messages
    past24hrs = []
    for message in data:
        if(timestampnow - message.get("timestamp") < 86400):
            past24hrs.append(message)
    
    positive = []
    negative = []
    totalScore = 0
    numberPoints = 0
    points = []
    
    #generate moving average and sort past 24 hour messages into positive and negative
    for message in past24hrs:
        totalScore += message.get("score")
        numberPoints += 1
        average = totalScore/numberPoints
        points.append({"timestamp": message.get('timestamp'), "average": average})
        if (message.get("score") < .5):
            negative.append(message)
        if (message.get("score") > .5):
            positive.append(message)
    #find number of positive and negative thoughts
    numberPositive = len(positive)
    numberNegative = len(negative)
    dailyScore = totalScore/numberPoints
    
    # find top ten positive thoughts
    top5Positive = [{"text": "Null", "score": 0, "timestamp": 1572712674.453777},
                    {"text": "Null", "score": 0, "timestamp": 1572712674.453777},
                    {"text": "Null", "score": 0, "timestamp": 1572712134.453777},
                    {"text": "Null", "score": 0, "timestamp": 1572710674.453777},
                    {"text": "Null", "score": 0, "timestamp": 1572702674.453777}]
    
    #print(positive)
    index = 0
    for x in range(len(positive)):
        n = 0
        for y in range(1,5):
            #print(top5Positive[n].get('score'))
            if top5Positive[n].get('score') > top5Positive[y].get('score'):
                n = y
                #print(n)
        if top5Positive[n].get('score') < positive[x].get('score'):
            top5Positive[n] = positive[x]
    
    fivepositivethoughts = []
    
    for message in top5Positive:
        fivepositivethoughts.append(message.get("text"))
    print(fivepositivethoughts)    
        
    f= open("positivethoughts.txt","w+")
    for i in fivepositivethoughts:
        f.write(i + "\n")
    
    f= open("stats.txt","w+")
    f.write(str(numberPositive) + " " + str(numberNegative) + " " + str(round(dailyScore,2)))
    x = []
    y = []
    for i in points:
        x.append(i.get('timestamp'))
        y.append(i.get("average"))
    f.close()
        
    fig = plt.figure(figsize=(10,10))
    fig.patch.set_visible(False)
    plt.plot(x, y, color='skyblue',linewidth=4, alpha=.3 )
    plt.xticks([])
    plt.xlabel("Your Day")
    plt.ylabel("Average Mood Score")
    fig.savefig('past24hrsSMALL.jpg')
    
    fig = plt.figure(figsize=(20,10))
    plt.plot(x, y, color='skyblue',linewidth=4, alpha=.3 )
    plt.xticks([])
    plt.xlabel("Your Day")
    plt.ylabel("Average Mood Score")
    fig.savefig('past24hrsLARGE.jpg')
    
    fig = plt.figure(figsize=(10,10))
    labels = 'Positive Thoughts','Negative Thoughts'
    explode = (.05,0)
    plt.pie([numberPositive,numberNegative], colors = ["lemonchiffon","lightcyan"], explode=explode, labels=labels, autopct='%1.0f%%')
    fig.savefig('thoughtratioSMALL.jpg')

    
    fig = plt.figure(figsize=(20,10))
    labels = 'Positive Thoughts','Negative Thoughts'
    explode = (.05,0)
    plt.pie([numberPositive,numberNegative], colors = ["lemonchiffon","lightcyan"], explode=explode, labels=labels, autopct='%1.0f%%')
    fig.savefig('thoughtratioLARGE.jpg')
    

    fig = plt.figure(figsize=(10,10))
    past30days = [random.randint(0,100)*.01 for i in range(0, 30)]
    plt.hist(past30days,[0,.2,.4,.6,.8,1], rwidth = .8, color = "lemonchiffon")
    plt.xlabel("Mood Score Distribution")
    plt.ylabel("Number of Days")
    fig.savefig('past30daysSMALL.jpg')
    
    fig = plt.figure(figsize=(20,10))
    past30days = [random.randint(0,100)*.01 for i in range(0, 30)]
    plt.hist(past30days,[0,.2,.4,.6,.8,1], rwidth = .8, color = "lemonchiffon")
    plt.xlabel("Mood Score Distribution")
    plt.ylabel("Number of Days")
    fig.savefig('past30daysLARGE.jpg')
    

past24hrs(bob)
        