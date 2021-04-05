# used to create database

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="carbon_calories_account"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE carbon_calories_account")

# mycursor.execute("CREATE TABLE account (id INT AUTO_INCREMENT PRIMARY KEY, userName VARCHAR(255), email VARCHAR(255), password VARCHAR(255), location VARCHAR(255), address VARCHAR(255), imageId INT)")
# mycursor.execute("CREATE TABLE history (id INT AUTO_INCREMENT PRIMARY KEY, account_id INT, item VARCHAR(255), score FLOAT)")
# mycursor.execute("ALTER TABLE history add foreign key (account_id) references account(id)")