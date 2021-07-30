# CFB Bot!

import codecs
import re
from datetime import datetime
import pandas as pd

# Functions to read and write files into arrays.
def get_array(input_string):
    with open("textfiles/"+input_string+".txt","r") as f:
        input_array = f.readlines()
    input_array = [x.strip("\n") for x in input_array]
    return(input_array)

def write_out(input_string,input_array):
    with open("textfiles/"+input_string+".txt","w") as f:
        for i in input_array:
            f.write(i+"\n")
    return

# Big mess of a function to actually respond to commands
def call_bot(body, author, contributors):
    reply=""

    if (body.count("WHOA!")):
        return "he has trouble with the snap!"

    if (body.count("!post")):
        return "posted!"

    # CFB belt "location" for a given date
    if(body.count("!belt")):
        indices = [i for i, x in enumerate(body) if x == "!belt"]
        for i in indices:
            date = body[i+1]
            reply += getBelt(date)

    return reply

def getBelt(date):
    try:
        date = datetime.strptime(date, '%Y/%m/%d')
    except:
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except:
            return "Your date formatting is incorrect. Please use YYYY-MM-DD or YYYY/MM/DD format."

    if date >= datetime.strptime("1/1/1940", '%m/%d/%Y'):
        df = pd.read_csv('D1Games_1869-2019.csv')
        df['Fulldate'] = [datetime.strptime(x, '%Y-%m-%d') for x in df['Fulldate']]
        df = df.sort_values('Fulldate')
        df = df[(df['Fulldate'] >= datetime.strptime('1940/01/01', '%Y/%m/%d'))]

        print(date)
        beltWearer = "USC"
        for ind, row in df.iterrows():
            # early exit condition
            if row['Fulldate'] > date:
                return beltWearer

            elif row['Team'] == beltWearer and row['Result'] == 'L':
                beltWearer = row['Opponent']
        return beltWearer

    else:
        return "Please enter a date after 1940/01/01"
