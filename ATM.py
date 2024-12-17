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







