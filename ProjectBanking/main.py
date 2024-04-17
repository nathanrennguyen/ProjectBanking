import mysql.connector
import random
import os



connection = mysql.connector.connect(user = 'root', database = 'example', password ='Cocogoat3663!')

def check(id): #checks whether the ID submitted is found in the database
    cursor = connection.cursor()
    testQuery = ("SELECT * FROM Accounts WHERE ID = %s")
    cursor.execute(testQuery, (id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False

def create(name, id): #creates a new account with all parameters and a starting balance of 0
    passw = input("What password would you like?\n>")
    cursor = connection.cursor()
    try:
        addData = ("INSERT INTO Accounts (Name, ID, Password, Balance) VALUES (%s, %s, %s, 0)")
        cursor.execute(addData, (name, id, passw))
        print("Account created! We're glad to have you.")
        connection.commit()
    except:
        pass
    cursor.close()
    os.system('cls||clear')

def balance(id): #outputs balance of the account
    os.system('cls||clear')
    checker = check(id)
    if (not checker):
        print("Sorry, invalid ID! Please enter a valid ID!1")
        return
    cursor = connection.cursor()
    testQuery = ("SELECT Balance FROM Accounts WHERE ID = %s")
    cursor.execute(testQuery, (id,))
    balance = cursor.fetchone()[0]
    print(f"Balance: {balance}")
    cursor.close()

def deposit(amount, id): #deposits money into account
    os.system('cls||clear')
    checker = check(id)
    if (not checker):
        print("Sorry, invalid ID! Please enter a valid ID!2")
        return
    cursor = connection.cursor()
    testQuery = ("SELECT Balance FROM Accounts WHERE ID = %s")
    cursor.execute(testQuery, (id,))
    curbalance = cursor.fetchone()[0]
    cursor.close()
    cursor = connection.cursor()
    newbalance = amount + curbalance
    testQuery = ("UPDATE Accounts SET balance = %s WHERE ID = %s")
    cursor.execute(testQuery, (newbalance, id))
    print("Money deposited!")
    connection.commit()
    cursor.close()

def withdraw(amount, id): #withdraws money from account
    os.system('cls||clear')
    checker = check(id)
    if (not checker):
        print("Sorry, invalid ID! Please enter a valid ID!3")
        return False
    cursor = connection.cursor()
    testQuery = ("SELECT Balance FROM Accounts WHERE ID = %s")
    cursor.execute(testQuery, (id,))
    curbalance = cursor.fetchone()[0]
    cursor.close()
    cursor = connection.cursor()
    newbalance = curbalance - amount
    if (newbalance < 0):
        print("Sorry, you don't have that much money. Try to withdraw a lesser amount of money.")
        return
    testQuery = ("UPDATE Accounts SET balance = %s WHERE ID = %s")
    print("Money withdrawn!\n")
    cursor.execute(testQuery, (newbalance, id))
    connection.commit()
    cursor.close()
    return

def close(id): #closes accounts
    os.system('cls||clear')
    checker = check(id)
    if (not checker):
        print("Sorry, invalid ID! Please enter a valid ID!4")
        return
    cursor = connection.cursor()
    testQuery = ("DELETE FROM Accounts WHERE ID = %s")
    cursor.execute(testQuery, (id,))
    print("Account closed. We hope to see you again.")
    connection.commit()
    cursor.close()

def modify(id, name): #modifies names of accounts
    os.system('cls||clear')
    checker = check(id)
    if (not checker):
        print("Sorry, invalid ID! Please enter a valid ID!5")
        return
    cursor = connection.cursor()
    testQuery = ("UPDATE Accounts SET Name = %s WHERE ID = %s")
    cursor.execute(testQuery, (name, id))
    connection.commit()
    cursor.close()


print("Welcome!")
while (True):
    print("""\nOptions:
    1. Check Balance
    2. Deposit
    3. Withdraw
    4. Create a new account
    5. Close Account
    6. Change name under account
    7: Recover ID
    8. Exit""")

    choice = input(">")
    try:
        choice = int(choice)
    except:
        print("Make sure your choice is an integer!")
        continue
    if ((choice < 1 or choice > 8)):
        print("Invalid input! Make sure your choice is an integer between 1 and 7.\n")
        continue

    if (choice == 8):
        print("Have a nice day!")
        break
    elif (choice == 7):
        cursor = connection.cursor()
        name = input("What's your name?\n>")
        passw = input("What's your password?\n>")
        testQuery = ("SELECT ID FROM Accounts WHERE Name=%s AND Password=%s")
        cursor.execute(testQuery, (name, passw))
        result = cursor.fetchone()[0]
        cursor.close()
        if result:
            il = result
            print(f"Your ID is {il}")
        else:
            print("No ID found with that username and password.")
    elif (choice == 4):
        cursor = connection.cursor()
        testQuery = ("SELECT ID FROM Accounts")
        cursor.execute(testQuery)
        IDs = set(cursor.fetchall())
        rang = list(range(1000000, 9999999))
        available_ids = list(set(rang) - set(IDs))
        id = int(random.sample(available_ids, 1)[0])
        name = input("What name should your new account be under?\n>")
        testQuery = ("SELECT Name FROM Accounts")
        cursor.execute(testQuery)
        names = [row[0] for row in cursor.fetchall()]
        if (name in names):
            print("This name is taken! Choose a new name!")
            continue
        create(name, id)
        cursor.close()
    else:
        id = input("What is your Account ID?\n>")
        if (not id.isdigit()):
            print("Invalid input! Make sure your id is an integer and valid.\n")
            continue
        id = int(id)
        if (id < 1000000 or id > 9999999):
            print("Enter an ID in the valid range (1000000–9999999)")
            continue
        cursor = connection.cursor()
        testQuery = ("SELECT ID FROM Accounts")
        cursor.execute(testQuery)
        IDs = [int(row[0]) for row in cursor.fetchall()]
        if (not id in IDs):
            print("Provide a valid ID!\n")
            continue
        
        if (choice == 1):
            balance(id)
        elif (choice == 2):
            amount = input("How much money would you like to deposit?\n>")
            try:
                amount = int(amount)
            except:
                print("Invalid input! Next time, enter an integer for your amount!")
                continue
            if ((amount <= 0)):
                print("Invalid input! Make sure your amount is an integer and greater than zero.\n")
                continue
            deposit(amount, id)
        elif (choice == 3):
            amount = input("How much money would you like to withdraw?\n>")
            try:
                amount = int(amount)
            except:
                print("Invalid input! Next time, enter an integer for your amount!")
                continue
            if ((amount <= 0)):
                print("Invalid input! Make sure your amount is an integer and greater than zero.\n")
                continue
            withdraw(amount, id)
        elif (choice == 5):
            close(id)
        elif (choice == 6):
            name = input("What would you like to change your account name to?\n>")
            modify(id, name)


connection.close()