# -*- coding: utf-8 -*-
import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="carbon_calories"
)

def calculateRating(productID):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM products where productID = "+ str(productID) + ";")
    products = mycursor.fetchone()

    print(products[1], products[2])

    columnWeights = [0.3, 0.2, 0.1, 0.3, 0.1]
    score = 0

    score1=0
    score2=0
    score3=100
    score4=100
    score5=0

    # Local Calculation
    if products[3] == 1:
        score1 = 100
    else:
        score1 = 0
    
    # Plant Based Calculation
    if products[4] == 1:
        score2 = 100
    elif products[4] == 2:
        score2 = 50
    else:
        score2 = 0
    
    # Packaging Calculation
    packaging = str(products[5]).split()
    j = 0
    while j < len(packaging):
        if 'Plastic' in packaging[j]:
            print("We here bishes")
            score3 = score3 - 30
        if 'Paper' in packaging[j]:
            score3 = score3 - 10
        if 'Styrofoam' in packaging[j]:
            score3 = score3 - 15
        if 'Glass' in packaging[j]:
            score3 = score3 - 20
        if 'Metal' in packaging[j]:
            score3 = score3 - 25
        j = j+1
    
    # Meat Calculation
    if products[6] == 'Red':
        score4 = score4 - 90
    elif products[6] == 'White':
        score4 = score4 - 30
    
    # Seasonal Calculation
    if products[7] == 1:
        score5 = 0
    elif products[7] == 0:
        score5 = 100

    score = ((score1 * columnWeights[0]) + (score2 * columnWeights[1]) + (score3 * columnWeights[2]) + (score4 * columnWeights[3]) + (score5 * columnWeights[4])) / 10
    return score

def this(productID):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM products where productName like '%"+ str(productID) + "%';")
    products = mycursor.fetchall()

    for product in products:
        print(product[1], calculateRating(product[2]))

this('Avo')


mydb.close()

