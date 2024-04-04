import mysql.connector
import random

connection = mysql.connector.connect(user = 'root', database = 'example', password ='Cocogoat3663!')


def check(id):
    cursor = connection.cursor()
    testQuery = ("SELECT * FROM Accounts WHERE ID = %s")
    cursor.execute(testQuery, (id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False

def create(name, id):
    cursor = connection.cursor()
    addData = ("INSERT INTO Accounts (Name, ID, Balance) VALUES (%s, %s, 0)")
    cursor.execute(addData, (name, id))
    print("Account created! We're glad to have you.")
    connection.commit()
    cursor.close()

def balance(id):
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

def deposit(amount, id):
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

def withdraw(amount, id):
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

def close(id):
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

def modify(id, name):
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
    7. Exit""")

    choice = input(">")
    try:
        choice = int(choice)
    except:
        print("Make sure your choice is an integer!")
        continue
    if ((choice < 1 or choice > 7)):
        print("Invalid input! Make sure your choice is an integer between 1 and 7.\n")
        continue

    if (choice == 7):
        print("Have a nice day!")
        break
    elif (choice == 4):
        cursor = connection.cursor()
        testQuery = ("SELECT ID FROM Accounts")
        cursor.execute(testQuery)
        IDs = set(cursor.fetchall())
        rang = list(range(1000000, 9999999))
        available_ids = list(set(rang) - set(IDs))
        id = int(random.sample(available_ids, 1)[0])
        name = input("What name should your new account be under?\n>")
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