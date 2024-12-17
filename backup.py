"""ADMIN SIDE CODE """

import mysql.connector as myconn
import time
from colorama import Fore
from datetime import datetime
#====================================================================================================================================================================================

database = myconn.connect(host = "localhost",user = "root", password = "@Server00703", database ="bank" )
db_cursor = database.cursor(buffered=True)
db_search_username = "select exists ( select username from admins where username = %s);"
divider = Fore.RED + "================================================================================"
header = ["ID","Name","Phone No.","DOB","Address","Account Type","ATM PIN","Net UserName","Net Password","Balance"]
header_transaction = ["Date","Sender ID", "Sender Name", "Receiver ID", "Receiver Name", "Amount"]
header_status = ["ID Card Number", "Current Status"]
header_loan =["ID","Amount","DUE DATE","Status"]
header_loan_pending=["ID","Amount"]
def next_screen(num):
    for i in range(num):
        print()

def push(text):
    length = len(text)
    side = int((80 - length)/2)
    string = ""
    for i in range(side):
        string = string+" "
    string = string + text
    for i in range(side):
        string=string + " "
    print(Fore.GREEN + string)

def display_table(data, headers):
    try:

        col_widths = [max(len(str(row[i])) for row in data + [headers]) for i in range(len(headers))]
        header_row = " | ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers)))
        print(header_row)
        print("-" * len(header_row))
        for row in data:
            print(" | ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(row))))
    except:
        push(Fore.RED +"NO DATA Found")

def login(username,password):
    db_cursor.execute(f'select exists (select username from admins where username = "{username}");')
    if db_cursor.fetchone()[0] == 1:
        db_cursor.execute(f'select password from admins where username = "{username}";')
        if password == db_cursor.fetchone()[0]:
            return 1
        else:
            return 0
    else:
        return 0

def user_esxit(id):
    db_cursor.execute(f'select exists (select ID from users where ID = "{id}");')
    if db_cursor.fetchone()[0] == 1:
            return 1
    else:
        return 0

def user_exist_phone(pn):
    db_cursor.execute(f'select exists (select phone from users where phone = "{pn}");')
    if db_cursor.fetchone()[0] == 1:
        return 1
    else:
        return 0

def display_user(id_card):
    db_cursor.execute(f'select * from users where ID = "{id_card}"')
    result = db_cursor.fetchall()
    display_table(result, header)

def update_info(to_set,new_val,id):
    db_cursor.execute(f'UPDATE users SET {to_set} = "{new_val}" WHERE ID = "{id}"')
    database.commit()
    push("Successful")

def register_new_user():
    net_username ="NULL"
    net_password ="NULL"
    print(divider)
    push("Welcome to Omer's Bank (Registration)")
    print(divider)
    print()
    print()
    name = input("Enter Full Name:  ")
    while True:
        id_card = input("Enter CNIC ID Card:  ")
        if user_esxit(id_card) == 0:
            break
        else:
            push("User With Same ID Number Already Exist")
    while True:
        phone = input("Enter Phone No.:  ")
        if user_exist_phone(phone) == 0:
            break
        else:
            push("User Exist With Same Phone Number")
    dob = input("Enter DOB(DD/MM/YYYY):  ")
    address = input("Enter Address:  ")
    print()
    while True:
        account_type=""
        acc_type = int(input("[1] Saving Account\n[2] Current Account\n[3] Business Account\n---->  "))
        if acc_type > 3:
            push("Invalid Section")
        else:
            if acc_type ==1:
                account_type = "Saving Account"
            elif acc_type ==2:
                account_type = "Current Account"
            elif acc_type == 3:
                account_type = "Business Account"

            break

    while True:
        balance = input("Enter Inertial Balance:  ")
        if balance.isnumeric():
            break
        else:
            push("Enter Only Numbers")
    while True:
        atm_pin = input("Enter 4 Digit ATM Pin:  ")
        if atm_pin.isnumeric() and len(atm_pin)==4:
            break
        else:
            push("Please Enter Only 4 'DIGITS' ")
    while True:
        print()
        net_banking = input("[YES] Net Banking\n[NO] Net Banking\n---->  ")
        if net_banking.upper() == "YES" or net_banking.upper() == "NO":
            break
        else:
            push("Invalid Selection")
    if net_banking.upper() == "YES":
        net_username = input("Enter Username for NetBanking:  ")
        net_password = input("Enter Password fot NetBanking:  ")
    print(divider)
    print(divider)
    print()
    push("Saving User's Information into BANK Database")
    time.sleep(3)
    db_cursor.execute(f'INSERT INTO users VALUES ("{id_card}","{name}","{phone}","{dob}","{address}","{account_type}","{atm_pin}","{net_username}","{net_password}","{balance}");')
    database.commit()
    db_cursor.execute(f'INSERT INTO status VALUES ("{id_card}","BLOCK");')
    database.commit()
    push("SUCCESSFUL")
    input("Press Any Thing To Exit ----> ")
    next_screen(20)

def user_info():
    print(divider)
    push("Welcome to Omer's Bank (User's Information)")
    print(divider)
    print()
    print()
    while True:
        res = input("[1] ID card\n[2] Phone No.\n---->  ")
        if res == "1" or res == "2":
            break
        else:
            push("Invalid Selection")
    if res == "1":
        id_card = input("Enter ID Number:  ")
        push("Searching DataBase Using ID Card Number")
        time.sleep(3)
        if user_esxit(id_card) == 1:
            db_cursor.execute(f'select * from users where ID = "{id_card}"')
            result = db_cursor.fetchall()
            display_table(result,header)
        else:
            push("User Does Not Exist In Bank's Database")
    else:
        phone = input("Enter Phone No.:  ")
        push("Searching DataBase Using Phone Number ")
        time.sleep(3)
        if user_exist_phone(phone) ==1:
            db_cursor.execute(f'select * from users where phone = "{phone}"')
            result = db_cursor.fetchall()
            display_table(result, header)
        else:
            push("User Does Not Exist With This Phone# In Bank's Database")
    input("Press Any Thing To Exit ----> ")
    next_screen(20)

def edit_user():
    print(divider)
    push("Welcome to Omer's Bank (Edit INFO)")
    print(divider)
    print()
    print()
    while True:
        id_card = input("Enter ID Card Number of The User: ")
        push("Searcing In DataBase")
        time.sleep(2)
        if user_esxit(id_card)==1:
            break
        else:
            push("User With This ID Card Does Not Exist")
    print("\n\n\n")
    display_user(id_card)
    print("\n\n\n")
    time.sleep(1)
    while True:
        while True:
            res = input("[1] Name\n[2] Phone No.\n[3] DOB\n[4] Address\n[5] Account Type\n[6] ATM Pin\n[7] Net Banking UserName\n[8] Net Banking Password\n[9] To Exit\n---->  ")
            if res == "1" or res == "2" or res == "3" or res == "4" or res == "5" or res == "6" or res == "7" or res == "8" or res == "9":
                break
            else:
                push("Invalid Selection")
        if res == "1":
            val = input("Enter New Name:  ")
            update_info("name",val,id_card)

        elif res == "2":
            val = input("Enter New Phone No.:  ")
            update_info("phone",val,id_card)
        elif res == "3":
            val = input("Enter New DOB:  ")
            update_info("dob",val,id_card)
        elif res =="4":
            val = input("Enter New Address:  ")
            update_info("address",val,id_card)
        elif res=="5":
            val = input("Enter New Account Type: \n[1] Saving Account\n[2] Current Account\n[3] Business Account\n---->   ")
            if val == "1":
                update_info("account_type","Saving Account",id_card)
            elif val == "2":
                update_info("account_type", "Current Account", id_card)
            elif val == "3":
                update_info("account_type", "Business Account", id_card)
            else:
                push("Invalid Selection")
        elif res == "6":
            val = input("Enter New ATM Pin:  ")
            update_info("ATM_pin", val, id_card)
        elif res == "7":
            val = input("Enter New UserName:  ")
            update_info("net_username", val, id_card)
        elif res == "8":
            val = input("Enter New Password:  ")
            update_info("net_password", val, id_card)
        elif res == "9":
            break
        print("\n\n\n")
        display_user(id_card)
        print("\n\n\n")
        if input("Enter '00' Stop Editing More\n---->  ") == "00":
            break
    input("Press Any Thing To Exit ----> ")
    next_screen(20)

def delete_user():
    print(divider)
    push("Welcome to Omer's Bank (Delete User)")
    print(divider)
    print()
    print()
    while True:
        res = input("[1] ID card\n[2] Phone No.\n---->  ")
        if res == "1" or res == "2":
            break
        else:
            push("Invalid Selection")
    if res == "1":
        id_card = input("Enter ID Number:  ")
        push("Searching DataBase Using ID Card Number ")
        time.sleep(3)
        if user_esxit(id_card) == 1:
            db_cursor.execute(f'select * from users where ID = "{id_card}"')
            result = db_cursor.fetchall()
            push("\nFound One Record Below")
            print("\n\n")
            display_table(result,header)
            print("\n\n\n\n")
            response = input("Do you want to Delete this User? [YES] / [NO]").upper()
            if response == "YES":
                push("Deleting All Info of This User Form The DataBase")
                time.sleep(2)
                db_cursor.execute(f'DELETE FROM users WHERE ID = "{id_card}"')
                database.commit()
                push("Deleted Successfully ")
            elif response == "NO":
                pass
            else:
                push("Invalid Selection")
        else:
            push("User Does Not Exist In Bank's Database")
    else:
        phone = input("Enter Phone No.:  ")
        push("Searching DataBase Using Phone Number ")
        time.sleep(3)
        print("\n\n\n")
        if user_exist_phone(phone) ==1:
            db_cursor.execute(f'select * from users where phone = "{phone}"')
            result = db_cursor.fetchall()
            display_table(result, header)
            print("\n\n\n")
            response = input("Do you want to Delete this User? [YES] / [NO]").upper()
            if response == "YES":
                push("Deleting All Info of This User Form The DataBase")
                time.sleep(2)
                db_cursor.execute(f'DELETE FROM users WHERE phone = "{phone}"')
                database.commit()
                push("Deleted Successfully ")
            elif response == "NO":
                pass
            else:
                push("Invalid Selection")

        else:
            push("User Does Not Exist With This Phone# In Bank's Database")
    input("Press Any Thing To Exit ----> ")
    next_screen(20)

def display_all_users():
    print(divider)
    push("Welcome to Omer's Bank (All User)")
    print(divider)
    print()
    print()
    print()
    db_cursor.execute("SELECT * FROM users;")
    result = db_cursor.fetchall()
    push(f'{len(result)} record found')
    print("\n\n\n")
    display_table(result,header)
    input("Press Any Thing To Exit ----> ")
    next_screen(20)

def all_transactions():
    print(divider)
    push("Welcome to Omer's Bank (All Transactions)")
    print(divider)
    print()
    print()
    print()
    db_cursor.execute(f'SELECT * FROM transactions;')
    result = db_cursor.fetchall()
    push("SEARCHING")
    time.sleep(2)
    print("\n\n\n")
    display_table(result,header_transaction)
    print("\n\n\n")
    input("Press Any Thing To Exit ----> ")

def status():
    while True:

        print(divider)
        push("Welcome to Omer's Bank (User Status")
        print(divider)
        print()
        print()
        res =input("[1] Display All Status\n[2] Display Specific User Status (Also for edit)\n---->  ")
        if res == "1":
            db_cursor.execute(f'SELECT * FROM status;')
            result = db_cursor.fetchall()
            display_table(result,header_status)
            print("\n\n")
        elif res == "2":
            push("Please wait")
            time.sleep(1)
            next_screen(30)
            print(divider)
            print("                  Welcome to Omer's Bank (User Status)                    ")
            print(divider)
            print()
            print()
            while True:
                id_card = input("Enter ID Card Number: ")
                if user_esxit(id_card) == 1:
                    break
            db_cursor.execute(f'SELECT * FROM status WHERE ID = "{id_card}";')
            result = db_cursor.fetchall()
            display_table(result, header_status)
            print("\n\n")

            res = input("[1] ACTIVATE\n[2] Block\n[0] To Exit\n----> ")
            print()
            if res == "1":
                print("Activating")
                time.sleep(1.5)
                db_cursor.execute(f'UPDATE status SET Active = "ACTIVE" WHERE ID = "{id_card}"')
                database.commit()
                print()
                push("Successfully Activated")
            elif res == "2":
                print("Blocking")
                time.sleep(1.5)
                db_cursor.execute(f'UPDATE status SET Active = "BLOCK" WHERE ID = "{id_card}"')
                database.commit()
                print()
                push("Successfully Blocked")


        else:
            push("Invalid Selection")
        print()
        res = input("[1] To Continue with Status\n[0] To Exit\n---> ")
        if res == "0":
            break
        elif res == "1":
            next_screen(25)
        else:
            push("Invalid Selection")
    input("Press Any Key To Go Back---> ")

def ret_phone(id):
    db_cursor.execute(f'SELECT phone FROM users WHERE ID = "{id}"')
    result = db_cursor.fetchone()[0]
    return result
def change_balance(phone,amount):
    db_cursor.execute(f'SELECT balance FROM users WHERE phone = "{phone}"')
    balance = int(db_cursor.fetchone()[0])
    balance = balance + int(amount)
    db_cursor.execute(f'UPDATE users SET balance = "{str(balance)}" WHERE phone = "{phone}"')
    database.commit()

def get_date_time():
    now = datetime.now()
    date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_time_string

def pending_loan_req():
    db_cursor.execute(f'SELECT * FROM pending_loan_requests;')
    result = db_cursor.fetchall()
    return result
def loan_req_approval(id):
    db_cursor.execute(f'SELECT * FROM pending_loan_requests WHERE ID = "{id}";')
    result = db_cursor.fetchall()
    amount = result[0][1]
    change_balance(ret_phone(id),amount)
    due_date = input("Enter Due Date For The Loan:  ")
    state = "DUE"
    db_cursor.execute(f'INSERT INTO loans VALUES ("{id}","{amount}","{due_date}","{state}")')
    database.commit()
    db_cursor.execute(f'DELETE FROM pending_loan_requests WHERE ID = "{id}"')
    database.commit()
    push(f'ID: {id} Loan Request Has Been Approved')
    input("Press Any Key To Exit --->")
def fetch_loan(i):
    if i == 2:
        push("Fetching All Ongoing Loans")
        time.sleep(1)
        db_cursor.execute(f'SELECT * FROM loans WHERE status = "DUE";')
        result = db_cursor.fetchall()
        print("\n\n")
        display_table(result,header_loan)
        print("\n\n")
    elif i == 3:
        push("Fetching All Loans")
        time.sleep(1)
        db_cursor.execute(f'SELECT * FROM loans;')
        result = db_cursor.fetchall()
        print("\n\n")
        display_table(result, header_loan)
        print("\n\n")
    input("Press Any Key To EXIT ---->  ")
def change_status(id):
    db_cursor.execute(f'SELECT * FROM loans WHERE ID = "{id}"')
    result = db_cursor.fetchall()
    print("\n\n")
    push("Current Status")
    print()
    display_table(result,header_loan)
    task = input("Change Status: \n[1] PAID\n[2] DUE\n----> ")
    if task == "1":
        db_cursor.execute(f'UPDATE loans SET status = "PAID" WHERE ID = "{id}"')
        database.commit()
        print()
        push("Status Changed")
    elif task == "2":
        db_cursor.execute(f'UPDATE loans SET status = "DUE" WHERE ID = "{id}"')
        database.commit()
        print()
        push("Status Changed")

        input("Press Any Key To Exit --->")
def loan_manager():
    while True:
        next_screen(30)
        print(divider)
        push("Welcome to Omer's Bank (Loan Manager)")
        print(divider)
        print("\n\n")
        res = input("[1] Loan Requests\n[2] On Going Loans\n[3] All Time Loans\n[4] Change Loan Status\n[5] EXIT\n---->  ")
        if res == "1":
            push("Fetching Information")
            time.sleep(1.5)
            print("\n\n\n")
            display_table(pending_loan_req(),header_loan_pending)
            print("\n\n")
            if input("Continue to Approval Dashboard [YES] / [NO]").upper() == "YES":
                while True:
                    val = input("Enter ID Card Number To Approve loan: ")
                    db_cursor.execute(f'select exists (select ID from pending_loan_requests where ID = "{val}");')
                    if db_cursor.fetchone()[0] == 1:
                        break
                    else:
                        push("No Loan Exist With This ID Card")
                loan_req_approval(val)
                if input("Do You Want To Approve Another Request? [YES] / [NO] ").upper() == "NO":
                    break

            else:
                break
        elif res == "2":
            fetch_loan(2)
        elif res == "3":
            fetch_loan(3)
        elif res == "4":
            next_screen(30)
            push("Please Wait")
            time.sleep(1.5)
            print(divider)
            push("CHANGE LOAN STATUS")
            print(divider)
            print("\n\n")
            while True:
                id_card = input("Enter ID CARD Number: ")
                if user_esxit(id_card) == 1:
                    break
                else:
                    push("No User Found With This ID CARD Number")
            change_status(id_card)
        elif res == "5":
            break
        else:
            push("Invalid Selection ")
    input("Press Any Key To Exit --->")






""" Main Program """
#====================================================================================================================================================================================

while True:
    print(divider)
    push("Welcome to Omer's Bank (Admin Login)")
    print(divider)
    print()
    print()

    while True:
        username = input(Fore.BLUE +"Enter Username: ")
        password = input(Fore.BLUE +"Enter Password: ")
        if login(username,password)==1:
            push(Fore.GREEN +"----Welcome to Omer's Bank----")
        else:
            push(Fore.RED +"! Incorrect Username or Password !")
            continue
        time.sleep(2)
        next_screen(60)
        while True:
            print(divider)
            push("Welcome to Omer's Bank (Admin Panel)")
            print(divider)
            print()
            print()
            print(Fore.GREEN +"[1] Register New User ") #done
            print(Fore.GREEN +"[2] Fetch User's Information ") #done
            print(Fore.GREEN +"[3] Edit User's Information ") #done
            print(Fore.GREEN +"[4] Remove User for Database ") #done
            print(Fore.GREEN +"[5] Display All Users ") #done
            print(Fore.GREEN +"[6] View All Transactions") #done
            print(Fore.GREEN +"[7] Loan Management")
            print(Fore.GREEN +"[8] Active/Block User")
            print(Fore.GREEN +"[9] Log Out")
            res = input(Fore.BLUE +"----> ")
            if res == "1":
                next_screen(25)
                register_new_user()

            elif res == "2":
                next_screen(25)
                user_info()
            elif res == "3":
                next_screen(25)
                edit_user()
            elif res == "4":
                next_screen(25)
                delete_user()
            elif res == "5":
                next_screen(20)
                display_all_users()
            elif res == "6":
                next_screen(25)
                all_transactions()
            elif res == "7":
                next_screen(25)
                loan_manager()
            elif res == "8":
                next_screen(25)
                status()
            elif res =="9":
                break
            else:
                push(Fore.RED +"Invalid ' SELECTION ' ")


""" ADMIN SIDE CODE END """

""" NET BANKING CODE """
import mysql.connector as myconn
import time
from datetime import datetime
from colorama import Fore

#====================================================================================================================================================================================

database = myconn.connect(host = "localhost",user = "root", password = "@Server00703", database ="bank" )
db_cursor = database.cursor(buffered=True)
divider = Fore.RED + "================================================================================" # 80
header_transaction = ["Date","Receiver Account Number", "Receiver Name", "$ Amount"]



#======================================================================================================================================================================================
def push(text):
    length = len(text)
    side = int((80 - length)/2)
    string = ""
    for i in range(side):
        string = string+" "
    string = string + text
    for i in range(side):
        string=string + " "
    print(Fore.GREEN +string)
def heading(text):
    print(divider)
    push(f' Omer"s Bank - NET BANKING ({text}) ')
    print(divider)
def print_space(num):
    for i in range(num):
        print()
def get_date_time():
    now = datetime.now()
    date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_time_string
def login(username,password):
    db_cursor.execute(f'select exists (select net_username from users where net_username = "{username}");')
    if db_cursor.fetchone()[0] == 1:
        db_cursor.execute(f'select net_password from users where net_username = "{username}";')
        if password == db_cursor.fetchone()[0]:
            return 1
        else:
            return 0
    else:
        return 0
def add_tras(date,sender_ph,rec_ph,amount):
    db_cursor.execute(f'INSERT INTO transactions VALUES ("{date}","{sender_ph}","{ret_name_phone(sender_ph)}","{rec_ph}","{ret_name_phone(rec_ph)}","{amount}");')
    database.commit()
def next_screen(num):
    for i in range(num):
        print()
def display_table(data, headers):
    try:

        col_widths = [max(len(str(row[i])) for row in data + [headers]) for i in range(len(headers))]
        header_row = " | ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers)))
        print(header_row)
        print("-" * len(header_row))
        for row in data:
            print(" | ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(row))))
    except:
        push("NO DATA Found")
def ret_phone(username_):
    db_cursor.execute(f'SELECT phone FROM users WHERE net_username = "{username_}"')
    result = db_cursor.fetchone()[0]
    return result
def ret_balance(username_):
    db_cursor.execute(f'SELECT balance FROM users WHERE net_username = "{username_}"')
    result = db_cursor.fetchone()[0]
    return result
def ret_id(username_):
    db_cursor.execute(f'SELECT ID FROM users WHERE net_username = "{username_}"')
    result = db_cursor.fetchone()[0]
    return result
def ret_name_id(id):
    db_cursor.execute(f'SELECT name FROM users WHERE ID = "{id}"')
    result = db_cursor.fetchone()[0]
    return result
def ret_name(username_):
    db_cursor.execute(f'SELECT name FROM users WHERE net_username = "{username_}"')
    result = db_cursor.fetchone()[0]
    return result
def ret_name_phone(phone_):
    db_cursor.execute(f'SELECT name FROM users WHERE phone = "{phone_}"')
    result = db_cursor.fetchone()[0]
    return result
def change_balance(phone,amount):
    db_cursor.execute(f'SELECT balance FROM users WHERE phone = "{phone}"')
    balance = int(db_cursor.fetchone()[0])
    balance = balance + int(amount)
    db_cursor.execute(f'UPDATE users SET balance = "{str(balance)}" WHERE phone = "{phone}"')
    database.commit()
def p2p(sender_ph,rec_ph,amount,date):
    send_amount = str(-1 *int(amount))
    change_balance(sender_ph, send_amount)
    change_balance(rec_ph,amount)
    database.commit()
    add_tras(date,sender_ph,rec_ph,amount)
    push("--Transaction Successful--")
def phone_exist(ph):
    db_cursor.execute(f'select exists (select phone from users where phone = "{ph}");')
    return db_cursor.fetchone()[0]
def tras_funds(username_):
    heading("Transfer Funds")
    print_space(2)
    while True:

        rec_ph = input("Enter Account Number of The Receiver:  ")
        if phone_exist(rec_ph) == 1:
            break
        else:
            push("Receiver Does Not Exist")

    while True:
        amount = input("Enter Amount to Transfer:  ")
        if int(amount) <= int(ret_balance(username_)):
            break
        else:
            push("Amount is Greater Than The Available Balance")
    while True:
        print(divider)
        push(f'Account Title: {ret_name_phone(rec_ph)}')
        push(f'[YES] / [NO] Do You Want To Confirm This Transaction? ')
        print(divider)
        res = input("---->  ")
        if res.upper() == "YES":
            p2p(ret_phone(username_), rec_ph, amount, get_date_time())
            break
        elif res.upper() == "NO":
            push("--- Transaction Cancelled ---")
            break
        else:
            push("INVALID SELECTION")

    input("Press Any Key To Exit --->  ")
def change_atm_pin(username_):
    heading("ATM - PIN")
    print_space(2)
    while True:
        new_atm_pin = input(Fore.BLUE+"Enter New 4 DIGIT ATM - PIN:  ")
        if len(new_atm_pin) == 4 and new_atm_pin.isnumeric():
            break
        else:
            push("ATM PIN Should Only Consist of 4 DIGITS")
    db_cursor.execute(f'UPDATE users SET ATM_pin = "{new_atm_pin}" WHERE net_username = "{username_}" ')
    push("ATM PIN CHANGED")
def user_transaction_history(username_):
    db_cursor.execute(f'SELECT date,getter_id,getter_name,amount FROM transactions WHERE sender_id = "{ret_phone(username_)}"')
    result = db_cursor.fetchall()
    print_space(2)
    display_table(result,header_transaction)
    input(Fore.BLUE +"Press Any Key To Exit ---->  ")
def check_status(id):
    db_cursor.execute(f'SELECT Active FROM status WHERE ID = "{id}";')
    if db_cursor.fetchone()[0] == "ACTIVE":
        return 1
    else:
        return 0
def block_my_account(id):
    heading("Block My Account")
    print_space(2)
    push("Blocking")
    time.sleep(1.5)
    db_cursor.execute(f'UPDATE status SET Active = "BLOCK" WHERE ID = "{id}"')
    database.commit()
    print()
    push("Successfully Blocked")
    print_space(2)
    print(Fore.BLUE+"Press Any Key To Exit --->  ")

def loan_manager(id):
    heading("Loan Manager")
    print_space(2)
    print(divider)
    db_cursor.execute(f'SELECT amount FROM pending_loan_requests WHERE ID = "{id}";')
    try:
        lon = db_cursor.fetchone()[0]
    except:
        lon = "0"


    push(f'Your Pending Loan Requests: ${lon}')
    push("-----------------------------------------------------")
    try:

        db_cursor.execute(f'SELECT amount FROM loans WHERE ID = "{id}" AND status = "DUE";')
        money = db_cursor.fetchone()[0]
        db_cursor.execute(f'SELECT due_date FROM loans WHERE ID = "{id}" AND status = "DUE";')
        dat = db_cursor.fetchone()[0]
        push(f'Your outstanding loan balance is ${money}, due for repayment by {dat}.')
    except:
        push("No Outstanding Loan")
    print(divider)
    print("\n\n\n")
    res = input(Fore.RED+"[1] Pay Loan\n[2] Apply For Loan\n[0] Exit\n----> ")
    if res == "1":
        print()
        next_screen(30)
        heading("RE PAYMENT")
        print("\n\n")
        pay_loan = input("Enter Amount You Want To Pay Back: ")
        db_cursor.execute(f'SELECT amount FROM loans WHERE ID = "{id}"')
        now_loan = int(db_cursor.fetchone()[0])
        now_loan = str(now_loan - int(pay_loan))
        db_cursor.execute(f'UPDATE loans SET amount = {now_loan} WHERE ID = "{id}"')
        database.commit()
        push("Paying Back Your Loan")
        time.sleep(1.5)
        push("Payment Successful")
        print()
        input(Fore.BLUE+"Press Any Key to Exit ----> ")
    elif res == "2":
        next_screen(30)
        heading("Apply For Loan")
        print("\n\n")
        amt = input(Fore.BLUE+"Enter Amount You Want To Apply For: ")
        db_cursor.execute(f'SELECT amount FROM loans WHERE ID = "{id}" AND status = "DUE";')
        try:
            result = db_cursor.fetchone()[0]
        except:
            result = "0"
        db_cursor.execute(f'select exists (select ID from pending_loan_requests WHERE ID = "{id}");')
        any_pending_req = db_cursor.fetchone()[0]
        if result == "0" and any_pending_req == 0:
            db_cursor.execute(f'INSERT INTO pending_loan_requests VALUES ("{id}","{amt}")')
            database.commit()
            push("Generating Your Request")
            time.sleep(1.5)
            push("Your Request Has Been Submitted Successfully")
        else:
            print()
            push("You Can Not Apply For New Loan Before Paying Back Current Outstanding Loans")
        print("\n\n")
        input(Fore.BLUE+"Press Any Key To Exit ----> ")


def customer_support(id):
    heading("Customer Support")
    print_space(1)
    push(Fore.BLUE+"-------------------------------------------")
    push("Send Us Your Queries Here")
    push("We Will Contact")
    push("Back On Call")
    push(Fore.BLUE+"-------------------------------------------")
    push("\n\n")
    message = input(Fore.BLUE+"Enter Your Message: ")
    db_cursor.execute(f'INSERT INTO customer_support VALUES ("{get_date_time()}","{id}","{ret_name_id(id)}","{message}");')
    print_space(2)
    push("Your Messages is Processing")
    time.sleep(1.7)
    push("Your Message Has Been Submitted Successfully")
    print()
    print()
    input(Fore.BLUE+"Press Any Key To Exit ---->")






""" MAIN CODE """
#======================================================================================================================================================================================


while True:
    heading(" - ")
    print_space(2)
    res = input("[1] Log In\n[0] Exit\n--> ")
    if res == "1":
        while True:
            next_screen(40)
            heading(" LOG IN ")
            print_space(2)
            username = input(Fore.BLUE+"Enter UserName:  ")
            password = input(Fore.BLUE+"Enter Password:  ")
            if login(username, password) == 1:
                print("\n\n")
                push(f'----Welcome | {ret_name(username)} | to Omers Bank----')
                if check_status(ret_id(username)) == 0:
                    print("\n\n")
                    print(Fore.BLUE+divider)
                    push(Fore.RED+"Your Account Has been Blocked")
                    push(Fore.RED+"Please Contact Bank")
                    print(Fore.BLUE+divider)
                    print("\n\n\n")
                    input(Fore.BLUE+"Press Any Key To Exit --->  ")
                    continue

            else:
                push(Fore.RED+"! Incorrect Username or Password !")
                continue
            time.sleep(2)
            while True:

                next_screen(60)
                heading(" HOME ")
                print_space(1)
                print(divider)
                push(f'Balance : ${ret_balance(username)}')
                print(divider)
                print_space(3)


                print("[1] Transfer Funds") #done
                print("[2] Change ATM Pin") # done
                print("[3] Transaction History") # done
                print("[4] Loan Management") # done
                print("[5] Customer Support") # Done
                print("[6] Block Account") #done
                print("[7] Log Out") #done
                res = input("----> ")
                if res == "1":
                    next_screen(25)
                    tras_funds(username)

                elif res == "2":
                    next_screen(25)
                    change_atm_pin(username)
                elif res == "3":
                    next_screen(25)
                    user_transaction_history(username)

                elif res == "4":
                    next_screen(20)
                    loan_manager(ret_id(username))
                elif res == "5":
                    next_screen(25)
                    customer_support(ret_id(username))
                elif res == "6":
                    next_screen(25)
                    block_my_account(ret_id(username))
                    break
                elif res == "7":
                    next_screen(30)
                    break
                else:
                    push(Fore.RED+"Invalid ' SELECTION ' ")

    else:
        break

"""NET BANKING CODE END"""

""" ATM CODE """
import mysql.connector as myconn
import time
from colorama import Fore
from datetime import datetime
#====================================================================================================================================================================================

database = myconn.connect(host = "localhost",user = "root", password = "@Server00703", database ="bank" )
db_cursor = database.cursor(buffered=True)
db_search_username = "select exists ( select username from admins where username = %s);"
divider = Fore.RED + "================================================================================"




#====================================================================================================================================================================================


def next_screen(num):
    for i in range(num):
        print()
def push(text):
    length = len(text)
    side = int((80 - length)/2)
    string = ""
    for i in range(side):
        string = string+" "
    string = string + text
    for i in range(side):
        string=string + " "
    print(Fore.GREEN + string)
def display_table(data, headers):
    try:

        col_widths = [max(len(str(row[i])) for row in data + [headers]) for i in range(len(headers))]
        header_row = " | ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers)))
        print(header_row)
        print("-" * len(header_row))
        for row in data:
            print(" | ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(row))))
    except:
        push(Fore.RED +"NO DATA Found")
def login(username,password):
    db_cursor.execute(f'select exists (select username from admins where username = "{username}");')
    if db_cursor.fetchone()[0] == 1:
        db_cursor.execute(f'select password from admins where username = "{username}";')
        if password == db_cursor.fetchone()[0]:
            return 1
        else:
            return 0
    else:
        return 0
def user_esxit(id):
    db_cursor.execute(f'select exists (select ID from users where ID = "{id}");')
    if db_cursor.fetchone()[0] == 1:
            return 1
    else:
        return 0
def heading(text):
    print(divider)
    push(f' Omer"s Bank - ATM ({text}) ')
    print(divider)
def print_space(num):
    for i in range(num):
        print()
def get_date_time():
    now = datetime.now()
    date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_time_string
def ret_id(phone_):
    db_cursor.execute(f'SELECT ID FROM users WHERE phone = "{phone_}"')
    result = db_cursor.fetchone()[0]
    return result
def ret_pin(phone_):
    db_cursor.execute(f'SELECT ATM_pin FROM users WHERE phone = "{phone_}"')
    result = db_cursor.fetchone()[0]
    return result
def ret_name_phone(phone_):
    db_cursor.execute(f'SELECT name FROM users WHERE phone = "{phone_}"')
    result = db_cursor.fetchone()[0]
    return result
def change_balance(phone,amount):
    db_cursor.execute(f'SELECT balance FROM users WHERE phone = "{phone}"')
    balance = int(db_cursor.fetchone()[0])
    balance = balance + int(amount)
    db_cursor.execute(f'UPDATE users SET balance = "{str(balance)}" WHERE phone = "{phone}"')
    database.commit()
def ret_balance(phone_):
    db_cursor.execute(f'SELECT balance FROM users WHERE phone = "{phone_}"')
    result = db_cursor.fetchone()[0]
    return result
def add_tras(date,sender_ph,rec_ph,amount):
    db_cursor.execute(f'select exists (select name from users where phone = "{sender_ph}");')
    if db_cursor.fetchone()[0] == 1:
        name = ret_name_phone(sender_ph)
    else:
        name = ret_name_phone(rec_ph)
    db_cursor.execute(f'INSERT INTO transactions VALUES ("{date}","{sender_ph}","{name}","{rec_ph}","{name}","{amount}");')
    database.commit()


def withdraw_cash(phone_):
    while True:
        heading("Withdraw Cash")
        print_space(2)
        push("Enter the amount to withdraw:")
        print()
        push("[1] $20                       [2] $50")
        push("[3] $100                      [4] $150")
        push("[5] $250                      [6] $500")
        push("[7] $1000                     [8] Other Amount")
        push("[9] Go Back")
        print_space(2)
        res = input("-----> ")
        if res == "1":
            if int(ret_balance(phone_)) < 20:
                print_space(2)
                push("Insufficient Balance")
                print_space(2)
                time.sleep(2)
                new_res = input("Would you like another transaction?\n[YES] / [NO]")
                if new_res.upper() == "YES":
                    continue
                else:
                    break
            else:
                print_space(2)
                push("------------------------------------------")
                push(f'Withdrawing  $20')
                push("------------------------------------------")
                print_space(2)
                change_balance(phone_,"-20")
                add_tras(get_date_time(),"ATM",phone_,"-20")
                time.sleep(1.5)
                print("\n\n")
                push("Withdraw Success, please collect your cash.")
                time.sleep(1.5)
                break

        elif res == "2":
            if int(ret_balance(phone_)) < 50:
                print_space(2)
                push("Insufficient Balance")
                print_space(2)
                time.sleep(2)
                new_res = input("Would you like another transaction?\n[YES] / [NO]")
                if new_res.upper() == "YES":
                    continue
                else:
                    break
            else:
                print_space(2)
                push("------------------------------------------")
                push(f'Withdrawing  $50')
                push("------------------------------------------")
                print_space(2)
                change_balance(phone_,"-50")
                add_tras(get_date_time(), "ATM", phone_, "-50")
                time.sleep(1.5)
                print("\n\n")
                push("Withdraw Success, please collect your cash.")
                time.sleep(1.5)
                break
        elif res == "3":
            if int(ret_balance(phone_)) < 100:
                print_space(2)
                push("Insufficient Balance")
                print_space(2)
                time.sleep(2)
                new_res = input("Would you like another transaction?\n[YES] / [NO]")
                if new_res.upper() == "YES":
                    continue
                else:
                    break
            else:
                print_space(2)
                push("------------------------------------------")
                push(f'Withdrawing  $100')
                push("------------------------------------------")
                print_space(2)
                change_balance(phone_,"-100")
                add_tras(get_date_time(), "ATM", phone_, "-100")
                time.sleep(1.5)
                print("\n\n")
                push("Withdraw Success, please collect your cash.")
                time.sleep(1.5)
                break
        elif res == "4":
            if int(ret_balance(phone_)) < 150:
                print_space(2)
                push("Insufficient Balance")
                print_space(2)
                time.sleep(2)
                new_res = input("Would you like another transaction?\n[YES] / [NO]")
                if new_res.upper() == "YES":
                    continue
                else:
                    break
            else:
                print_space(2)
                push("------------------------------------------")
                push(f'Withdrawing  $150')
                push("------------------------------------------")
                print_space(2)
                change_balance(phone_,"-150")
                add_tras(get_date_time(), "ATM", phone_, "-150")
                time.sleep(1.5)
                print("\n\n")
                push("Withdraw Success, please collect your cash.")
                time.sleep(1.5)
                break
        elif res == "5":
            if int(ret_balance(phone_)) < 250:
                print_space(2)
                push("Insufficient Balance")
                print_space(2)
                time.sleep(2)
                new_res = input("Would you like another transaction?\n[YES] / [NO]")
                if new_res.upper() == "YES":
                    continue
                else:
                    break
            else:
                print_space(2)
                push("------------------------------------------")
                push(f'Withdrawing  $250')
                push("------------------------------------------")
                print_space(2)
                change_balance(phone_,"-250")
                add_tras(get_date_time(), "ATM", phone_, "-250")
                time.sleep(1.5)
                print("\n\n")
                push("Withdraw Success, please collect your cash.")
                time.sleep(1.5)
                break
        elif res == "6":
            if int(ret_balance(phone_)) < 500:
                print_space(2)
                push("Insufficient Balance")
                print_space(2)
                time.sleep(2)
                new_res = input("Would you like another transaction?\n[YES] / [NO]")
                if new_res.upper() == "YES":
                    continue
                else:
                    break
            else:
                print_space(2)
                push("------------------------------------------")
                push(f'Withdrawing  $500')
                push("------------------------------------------")
                print_space(2)
                change_balance(phone_,"-500")
                add_tras(get_date_time(), "ATM", phone_, "-500")
                time.sleep(1.5)
                print("\n\n")
                push("Withdraw Success, please collect your cash.")
                time.sleep(1.5)
                break
        elif res == "7":
            if int(ret_balance(phone_)) < 1000:
                print_space(2)
                push("Insufficient Balance")
                print_space(2)
                time.sleep(2)
                new_res = input("Would you like another transaction?\n[YES] / [NO]")
                if new_res.upper() == "YES":
                    continue
                else:
                    break
            else:
                print_space(2)
                push("------------------------------------------")
                push(f'Withdrawing  $1000')
                push("------------------------------------------")
                print_space(2)
                change_balance(phone_,"-1000")
                add_tras(get_date_time(), "ATM", phone_, "-1000")
                time.sleep(1.5)
                print("\n\n")
                push("Withdraw Success, please collect your cash.")
                time.sleep(1.5)
                break
        elif res == "8":
            print_space(2)
            push("------------------------------------------")
            push(f'Custom Amount')
            push("------------------------------------------")
            print_space(1)

            money = input("Enter Amount to withdraw: ")
            if int(ret_balance(phone_)) < int(money):
                print_space(2)
                push("Insufficient Balance")
                print_space(2)
                time.sleep(2)
                new_res = input("Would you like another transaction?\n[YES] / [NO]")
                if new_res.upper() == "YES":
                    continue
                else:
                    break
            else:
                print_space(2)
                push("------------------------------------------")
                push(f'Withdrawing  ${money}')
                push("------------------------------------------")
                print_space(2)
                money = "-"+money
                change_balance(phone_, money)
                add_tras(get_date_time(), "ATM", phone_, f"{money}")
                time.sleep(1.5)
                print("\n\n")
                push("Withdraw Success, please collect your cash.")
                time.sleep(1.5)
                break
        elif res == "9":
            break
        else:
            print()
            push("Invalid Selection")
def deposit_cash(phone_):
    heading(" Deposit Cash ")
    print_space(2)
    push("----------------------------------------------")
    push("Insert cash into the deposit slot.")
    push("[NO] TO Go Back")
    push("----------------------------------------------")
    print_space(2)
    while True:
        amount = input("----> ")
        if amount.isnumeric() == False and amount.upper() != "NO":
            push("Enter Digits Only")
        elif amount.upper() == "NO":
            break
        else:
            change_balance(phone_,amount)
            add_tras(get_date_time(), phone_, "ATM", f"{amount}")
            print_space(2)
            push(f'Amount deposited: ${amount}')
            time.sleep(2)
            print_space(1)
            break

def check_status(id):
    db_cursor.execute(f'SELECT Active FROM status WHERE ID = "{id}";')
    if db_cursor.fetchone()[0] == "ACTIVE":
        return 1
    else:
        return 0
def change_atm_pin(phone_):
    heading("ATM - PIN")
    print_space(2)
    while True:
        new_atm_pin = input(Fore.BLUE+"Enter New 4 DIGIT ATM - PIN:  ")
        if len(new_atm_pin) == 4 and new_atm_pin.isnumeric():
            break
        else:
            push("ATM PIN Should Only Consist of 4 DIGITS")
    db_cursor.execute(f'UPDATE users SET ATM_pin = "{new_atm_pin}" WHERE phone = "{phone_}" ')
    push("ATM PIN CHANGED")


""" MAIN CODE """
#====================================================================================================================================================================================

while True:
    while True:
        res = ""
        heading(" Welcome ")
        print_space(2)
        while True:
             phone = input("Enter Your Account# :  ")
             if phone.isnumeric() and user_esxit(ret_id(phone)) == 1:
                 break
             else:
                 push("No User Exist")
        pin = input("Enter Your 4 DIGIT ATM Pin:  \n[Press 'Cancel' to go back]\n---->  ")
        if ret_pin(phone) == pin:
            if check_status(ret_id(phone)) == 1:
                print("\n\n")
                push("------------------------")
                push(f'Welcome {ret_name_phone(phone)}')
                push("------------------------")
                time.sleep(1.5)
            else:
                print_space(2)
                push("-------------------------------------")
                push("Your Account is Blocked")
                push("-------------------------------------")
                break





        elif pin.upper() =="CANCLE":
            break
        else:
            push("Invalid Pin")
            time.sleep(2)
            break

        while True:
            if res.upper() == "NO":
                break
            next_screen(30)
            heading(f'{ret_name_phone(phone)}')
            print_space(2)
            push("------------------------------------------")
            push(f'M A I N   M E N U')
            push("------------------------------------------")
            print_space(2)
            res = input("[1] View Balance\n[2] Withdraw Cash\n[3] Deposit Cash\n[4] Change Pin\n[5] Exit\n----> ")
            if res == "1":
                next_screen(35)
                push("Your Balance")
                print_space(1)
                print(divider)
                push(f'Balance : ${ret_balance(phone)}')
                print(divider)
                print_space(2)
                while True:
                    sres = input("Would you like another transaction?\n[YES] / [NO]")
                    if sres.upper() == "YES" or sres.upper() == "NO":
                        break
                    else:
                        push("Invalid Selection")
                        time.sleep(1)

            elif res == "2":
                next_screen(35)
                withdraw_cash(phone)
            elif res=="3":
                next_screen(35)
                deposit_cash(phone)
            elif res == "4":
                next_screen(35)
                change_atm_pin()
            elif res == "5":
                next_screen(35)
                push("Thankyou For Using Our ATM")
                time.sleep(2)
                break
            else:
                push("Invalid Selection")
                input("Press Enter ----> ")

