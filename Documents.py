'''
Documents 

Scenario:
  A small service company needs to ellaborate documents certifing service provided.
  Each poisson distributed with lam = 1800secs time a document request arrives.
  Only one secretary ellaborates documents.
  The process comes with the following conditions depending of client context and requirements:

      Conditions is a binary string from 00000 to 11111.
      A 1 is a True in each condition.
      The conditions and its probability are:

      00001 : Previous document found (0.8)
      00010 : Printing required (0.85)
      00100 : PDF format required (0.3)
      01000 : Send by mail (0.85)
      10000 : Upload file to drive (0.25)

The proccess and each activity time are (times are normally distribuited, with a SD = 0.1*time):

  Seek previous document of same client (30)
  if 00001:
    take previous (5)
  else:
    Take last or similar document (60)
  Edit with new data (60)
  Generate QR code (20)
  Copy QR metadata to db file (30)
  Paste QR image in document (60)
  Copy document data to db file (70)
  Check QR code is working (90)
  Save (5)
  if 00010:
    Print (15)
  if 00100:
    Save as PDF (20)
    if 01000:
      Compose email (90)
      Send (5)
    if 10000:
      Upload file to drive (60)
      Generate drive link (30)
      Compose email (180)
      Check drive link is working (60)
      Send (5)
'''

import simpy
import numpy as np
from itertools import count
from random import normalvariate, random, seed
import matplotlib.pyplot as plt

RANDOM_SEED = 190689
CONDITIONS_PROBABILITIES = [0.8, 0.85, 0.3, 0.85, 0.25]
ACTIVITIES_TIMES = [30, 5, 60, 60, 20, 30, 60, 70, 90, 5, 15, 20, 90, 5, 60, 30, 180, 60, 5]
DOCS_TIME_ARRIVING = 1800
SECRETARIES = 3
HOURS_SIMULATED = 10

def documentGenerator(env, res, arriving_rate):
    i=0
    while True:
        yield env.timeout(np.random.poisson(arriving_rate))
        #print("Document arrived at {}".format(env.now))
        env.documentsLeft += 1
        env.arrivedDocs += 1
        conditions = 0
        if(random() < CONDITIONS_PROBABILITIES[0]): conditions = conditions | 1
        if(random() < CONDITIONS_PROBABILITIES[1]): conditions = conditions | 2
        if(random() < CONDITIONS_PROBABILITIES[2]):
            conditions = conditions | 4
            if(random() < CONDITIONS_PROBABILITIES[3]): conditions = conditions | 8
            if(random() < CONDITIONS_PROBABILITIES[4]): conditions = conditions | 16
        env.process(document(env, i, format(conditions, '#07b')[2:], res))
        i += 1
    
#Generates normal distribiuted random time, from mean = time and SD = 0.1*time
def normalRandomTimeGenerator(time):
    new_time = int(normalvariate(time, time*0.1))
    return new_time

def document(env, number, conditions, res):
  with res.request() as scv:
      yield scv
      rt = normalRandomTimeGenerator
      #print("Document {} process started with following conditions: {}".format(number, conditions))
      ini = env.now
      yield env.timeout(rt(ACTIVITIES_TIMES[0])) # Seek previous document of same client
      if(conditions[4] == '1'):
          yield env.timeout(rt(ACTIVITIES_TIMES[1]))  # Take previous
      else:
          yield env.timeout(rt(ACTIVITIES_TIMES[2])) # Take last or similar document
      yield env.timeout(rt(ACTIVITIES_TIMES[3])) # Edit with new data
      yield env.timeout(rt(ACTIVITIES_TIMES[4])) # Generate QR code
      yield env.timeout(rt(ACTIVITIES_TIMES[5])) # Copy QR metadata to db file
      yield env.timeout(rt(ACTIVITIES_TIMES[6])) # Paste QR image in document
      yield env.timeout(rt(ACTIVITIES_TIMES[7])) # Copy document data to db file
      yield env.timeout(rt(ACTIVITIES_TIMES[8])) # Check QR code is working 
      yield env.timeout(rt(ACTIVITIES_TIMES[9])) # Save
      if(conditions[3] == '1'):
          yield env.timeout(rt(ACTIVITIES_TIMES[10])) # Print
      if(conditions[2] == '1'):
          yield env.timeout(rt(ACTIVITIES_TIMES[11])) # Save as PDF
          if(conditions[1] == '1'):
              yield env.timeout(rt(ACTIVITIES_TIMES[12])) # Compose email
              yield env.timeout(rt(ACTIVITIES_TIMES[13]))  # Send
          if(conditions[0] == '1'):
              yield env.timeout(rt(ACTIVITIES_TIMES[14])) # Upload file to drive
              yield env.timeout(rt(ACTIVITIES_TIMES[15])) # Generate drive link
              yield env.timeout(rt(ACTIVITIES_TIMES[16]))# Compose email
              yield env.timeout(rt(ACTIVITIES_TIMES[17])) # Check drive link is working
              yield env.timeout(rt(ACTIVITIES_TIMES[18]))  # Send
      env.documentsLeft -= 1
      processingTime = env.now - ini
      #print("Process time: {}".format(processingTime))
      #print("Process ended at {} hours {} minutes".format(env.now // 3600, (env.now % 3600)//60))
      #print("")

#Simulation begin
#----------------------------------------------------------------

print("Document Generation Simulation")
seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

#docsPerArrivingRate = []
#unfinishedDocsPerArrivingRate = []

for y in range (SECRETARIES, 0, -1): #Behavior with from SECRETARIES to 1
    docsPerArrivingRate = []
    unfinishedDocsPerArrivingRate = []
    for x in range(DOCS_TIME_ARRIVING, 19, -20): #Higher pace of documents requests
        env = simpy.Environment()
        env.documentsLeft = 0
        env.arrivedDocs = 0
        res = simpy.Resource(env, capacity = y)
        env.process(documentGenerator(env, res, x))
        env.run(until=(HOURS_SIMULATED * 3600 + 1))

        docsPerArrivingRate.append(env.arrivedDocs)
        unfinishedDocsPerArrivingRate.append(env.documentsLeft)
        
    print(docsPerArrivingRate)
    print(unfinishedDocsPerArrivingRate)
    plt.plot(range(DOCS_TIME_ARRIVING, 19, -20), unfinishedDocsPerArrivingRate) #plot how many unfinished documents with current parameters

plt.gca().invert_xaxis()
plt.show()