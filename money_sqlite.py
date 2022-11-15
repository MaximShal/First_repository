import sqlite3
from art import tprint
from datetime import *
import time
from prettytable import PrettyTable


conn = sqlite3.connect("Money_control.sqlite3")
dict_month = {
        "01": "january",
        "02": "february",
        "03": "march",
        "04": "april",
        "05": "may",
        "06": "june",
        "07": "july",
        "08": "august",
        "09": "september",
        "10": "october",
        "11": "november",
        "12": "december"}
date_global = datetime.now().strftime("%m")


def create_table():
    conn.execute(f'CREATE TABLE IF NOT EXISTS "{dict_month[date_global]}" '
                 f'(id INT, Purpose TEXT, Kind TEXT, Sum INT, Date TEXT, Time TEXT)')


def add_record():
    print("\nAdding.")
    id = conn.execute(f"SELECT max(id) FROM {dict_month[date_global]} ORDER BY id DESC LIMIT 1").fetchone()[0]
    if id == None:
        id = 1
    else:
        id = id + 1
    purpose = input("Purpose: ")
    sum = input("Sum(UAH): ")
    kind = input("Kind '+' or '-': ")
    date = datetime.now().strftime("%d-%m-%Y")
    time = datetime.now().strftime("%H:%M")
    conn.execute(f'INSERT INTO {dict_month[date_global]} VALUES ({id}, "{purpose}", "{kind}", {sum}, "{date}", "{time}"'
                 f')')
    conn.commit()
    print("Added!".center(20, "_"), "\n")


def view_records():
    def view_cycle(sqlite_list):
        my_table = PrettyTable()
        my_table.field_names = ["id", "Purpose", "Kind", "Sum", "Date", "Time"]
        total_income = 0
        total_expense = 0

        for operation in sqlite_list:
            if operation[2] == "+":
                total_income = total_income + operation[3]
            elif operation[2] == "-":
                total_expense = total_expense + operation[3]
            my_table.add_row(operation)

        total = total_income - total_expense
        my_table.add_row([" ", "Total income", "+", total_income, " ", " "])
        my_table.add_row([" ", "Total expense", "-", total_expense, " ", " "])
        my_table.add_row([" ", "***Total***", " ", total, " ", " "])
        print(my_table)
        print()

    print("\nChoose per 'month' or 'day':")
    choose_view = input(">")
    if choose_view == "month":
        month_view = conn.execute(f'SELECT * FROM {dict_month[date_global]}').fetchall()
        view_cycle(month_view)
    elif choose_view == "day":
        day_view = conn.execute(f'SELECT * FROM {dict_month[date_global]} WHERE '
                                f'date = "{datetime.now().strftime("%d-%m-%Y")}"').fetchall()
        view_cycle(day_view)
    else:
        print("¯\_(ツ)_/¯".center(22, " "), "\nYou taked mistake... Try again")
        view_records()


def help_information():
    help_text = """In this program you can control your finance. This code using sqlite3 database. You can use function:
          'add' - for add your income or expense operation;
          'view' - for see completed operations per moth or day;
          'close' - simple, will closing a code.\n"""
    for i in help_text:
        time.sleep(0.1)
        print(i, end='', flush=True)


def main():
    create_table()
    tprint("MoneyControl", font="thin")

    dict_operations = {
        "add": add_record,
        "view": view_records,
        "help": help_information
    }

    def step_one():
        print("Operations: \n add\n view\n help\n close")
        try:
            dict_operations[input(">")]()
            step_one()
        except KeyError:
            print("See you later... ʕ ᵔᴥᵔ ʔ")
            pass

    step_one()
    conn.close()


if __name__ == "__main__":
    main()
