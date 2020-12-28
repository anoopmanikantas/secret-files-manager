import sqlite3
import os
from cryptography.fernet import Fernet


def createAccount():
    x = open('pass.key', 'rb').read()
    passw = input("Enter a password to create an account").encode()
    key = Fernet(key=x)
    open('login.txt', 'wb').write(key.encrypt(passw))


def login():
    while True:
        passw = bytes(input('enter your password to login: '), encoding='utf-8')
        x = open('pass.key', 'rb').read()
        key = Fernet(key=x)
        b = open('login.txt', 'rb').read()
        if passw == key.decrypt(b):
            print("Welcome!".center(20, '-'))
            break


def convertData(file):
    with open(file, "rb") as f:
        binData = f.read()
    return binData


def storeFile(LOC):
    if os.path.exists(LOC):
        f = convertData(LOC)
        print()
        cur.execute(f'insert into secret (fname,files) values(?,?)', (os.path.basename(LOC), f))
        db.commit()
        print(f"File->{os.path.basename(LOC)} has been uploaded successfully!")


def writeFile(data, fileName):
    with open(fileName, 'wb') as f:
        f.write(data)


def dataRetrieval(file):
    cur.execute(f"select * from secret where fname='{file}'")
    for i in cur.fetchall():
        file = i[0]
        data = i[1]
        writeFile(data, file)


if __name__ == '__main__':
    if os.path.exists("login.txt"):
        login()
    else:
        key = Fernet.generate_key()
        open('pass.key', 'wb').write(key)
        createAccount()

    while True:
        db = sqlite3.connect("secret_files.db")
        cur = db.cursor()
        print("".center(20, '-'))
        x = input("1. Store file\n2. Open file\n3. Display the files stored\n4. Exit application\nEnter your choice: ")
        print("".center(20, '-'))

        if x == '1':
            path = input("Enter the path of the file\nExample: C:/users/{username}/new_text.txt\n ")
            storeFile(LOC=path)

        elif x == '2':
            name = input("Enter the name of the file with extension to retrieve: ")
            dataRetrieval(name)

        elif x == '3':
            cur.execute("select * from secret")
            print("Name(s) of the file(s) stored in database ", end='\n')
            for i, v in enumerate(cur.fetchall()):
                print(f'file[{i}]: {v[0]}')

        else:
            print("Thank you!")
            break
