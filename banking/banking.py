import random
import string
import datacard

conn = datacard.connect()
conn.execute("DROP TABLE card;")
datacard.create_table(conn)


class Account:
    all_account = {}

    def __init__(self, card, pin):
        self.card = card
        self.pin = pin
        self.balance = 0
        Account.all_account.update({self.card: {'pin': self.pin, 'balance': self.balance}})


card_number = ''
pin_number = ''


def create_number():
    global card_number
    global pin_number
    unique_number = string.digits
    card_number = '400000' + ''.join(random.choice(unique_number) for i in range(9))
    list_number = [num for num in card_number]
    for x in range(len(list_number)):
        list_number[x] = int(list_number[x])
        if x % 2 == 0:
            list_number[x] *= 2
        if list_number[x] > 9:
            list_number[x] -= 9
    if sum(list_number) % 10 != 0:
        checksum = 10 - (sum(list_number) % 10)
    else:
        checksum = 0
    card_number += str(checksum)
    pin_number = ''.join(random.choice(unique_number) for j in range(4))


def luhn_check(receive):
    list_num = [a for a in receive]
    for a in range(len(list_num)):
        list_num[a] = int(list_num[a])
        if a % 2 == 0:
            list_num[a] *= 2
        if list_num[a] > 9:
            list_num[a] -= 9
    if sum(list_num) % 10 == 0:
        return True
    return False


def transfer(acc):
    print("Transfer")
    receive_num = input("Enter card number:\n")
    data_ = datacard.get_all(conn)
    same_acc = False
    acc_exist = False
    if receive_num == acc[1]:
        same_acc = True
    if not same_acc:
        if luhn_check(receive_num):
            for d in data_:
                if receive_num == d[1]:
                    acc_exist = True
                    amount = int(input("Enter how much money you want to transfer:\n"))
                    balance = datacard.get_balance(conn, acc[0])
                    bal = balance[0][3]
                    if amount > bal:
                        print("Not enough money!\n")
                    else:
                        add_money = amount + d[3]
                        minus_money = bal - amount
                        datacard.update_balance(conn, (add_money, d[0]))
                        datacard.update_balance(conn, (minus_money, acc[0]))
                        print("Success!\n")
            if not acc_exist:
                print("Such a card does not exist.\n")
        else:
            print("Probably you made a mistake in the card number. Please try again!\n")
    else:
        print("You can't transfer money to the same account!\n")


MENU_PROMPT = """1. Create an account
2. Log into account
0. Exit
"""
LOG_PROMPT = """1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
"""
control = 1
log_in = False
ids = 0
while control != "0":
    control = input(MENU_PROMPT)
    print()
    if control == "1":
        create_number()
        ids += 1
        account = Account(card_number, pin_number)
        datacard.add_card(conn, card_number, pin_number)
        print("Your card has been created")
        print("Your card number:")
        print(account.card)
        print("Your card pin:")
        print(account.pin)
        data = datacard.get_all(conn)
        print()
    elif control == "2":
        print("Enter your card number:")
        check_number = input()
        print("Enter your pin:")
        check_pin = input()
        print()
        check_acc = False
        data = datacard.get_all(conn)
        for acc in data:
            if acc[1] == check_number:
                check_acc = True
                if check_pin == acc[2]:
                    print("You have successfully logged in!\n")
                    log_in = True
                    while log_in and (control := input(LOG_PROMPT)) != "0":
                        print()
                        if control == "1":
                            balance = datacard.get_balance(conn, acc[0])
                            bal = balance[0][3]
                            print(f"Balance: {bal}\n")
                        elif control == "2":
                            print("Enter income:")
                            income = int(input())
                            balance = datacard.get_balance(conn, acc[0])
                            bal = balance[0][3]
                            income += bal
                            print("Income was added!\n")
                            datacard.update_balance(conn, (income, acc[0]))
                        elif control == "3":
                            transfer(acc)
                        elif control == "4":
                            datacard.delete_card(conn, acc[0])
                            print("The account has been closed!")
                            log_in =False
                        elif control == "5":
                            print("You have successfully logged out!")
                            log_in = False
                        else:
                            print("Invalid input!")
                    print()
                else:
                    check_acc = False
        if not check_acc:
            print("Wrong card number or PIN!\n")
    else:
        print("Invalid input!")
    if control == "0":
        print("Bye!")
