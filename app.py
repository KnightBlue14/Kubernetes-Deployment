from flask import Flask
import csv
import random

app = Flask(__name__)

@app.get("/")
def home():
    return ('You are at the homepage')

@app.get("/thought")
def thought():
    with open('thought_for_the_day.csv', mode ='r') as file:
        csvFile = csv.reader(file)
        line = random.choice(list(csvFile))[0]
        return line