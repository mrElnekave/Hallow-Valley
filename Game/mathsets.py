from constants import *
import objects
import os

def LoadMath():
    file_path = '24sets.txt'
    current_path = os.path.dirname(__file__)
    file_loc = os.path.join(current_path, file_path)
    filetxt = open(file_loc, "r")
    data = filetxt.read()
    filetxt.close()

    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split()

    
    mathQuestions = data
    if difficulty <= 2: 
        objects.problems = mathQuestions[(difficulty*400):((difficulty+1)*400)]
    else: 
        objects.problems = mathQuestions[1200:]