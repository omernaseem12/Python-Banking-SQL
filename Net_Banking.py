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

