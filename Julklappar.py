import random
import itertools
import smtplib, ssl
import argparse
import os
import sys

def checkUnique(list1, list2):
    for p1, p2 in zip(list1, list2):
        if p1 == p2:
            return True
    return False

def sendMail(participants, listToShuffle, secondList):
    port = 465 #SSL Port
    password = input("Enter you mailpassword: ")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("hemligajulafton@gmail.com", password)

        for giver, taker in zip(listToShuffle, secondList):
            msg = 'Subject: {}\n\n{}'.format("Din julklappsperson", "God Jul! Du ska ge en julklapp till " + participants[taker] +". Den ska kosta max 300kr.")
            server.sendmail("hemligajulafton@gmail.com", giver, msg)

parser = argparse.ArgumentParser(description='Send secret santa mail')
parser.add_argument("input", help="Input list, e-mail and name separated by colon sign")
args = parser.parse_args()
pathToFile = args.input

if not os.path.isfile(pathToFile):
    print("The specified file does not exist")
    sys.exit()

participants = {}
with open(args.input, 'r') as file:
    for line in file:
        x = line.split(":")
        participants[x[0]] = x[1].rstrip()

listToShuffle = list(participants.keys())

secondList = listToShuffle[:]
random.shuffle(secondList)

while checkUnique(listToShuffle, secondList):
    random.shuffle(listToShuffle)

sendMail(participants, listToShuffle, secondList)
