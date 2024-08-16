import sys

def get_initial_balance():
    try:
        balance = int(input('How much money do you have?\n'))
    except (ValueError,TypeError):            #Exceptoion 10
        sys.stderr.write(f"Invalid input. Initializing balance to 0.\n")
        balance = 0
    return balance

def has_comma(input_str):
    return ',' in input_str

def process_with_comma(records_list, input_str):
    parts = [part.strip() for part in input_str.split(',')]
    for part in parts:
        process_single_entry(records_list, part)

def process_without_comma(records_list, input_str):
    # Skip empty lines
    if input_str.strip():
        process_single_entry(records_list, input_str)

def process_single_entry(records_list, entry):
    subparts = entry.split()
    if len(subparts) == 2 and subparts[0].isalpha() and (subparts[1].isdigit() or (subparts[1][0] == '-' and subparts[1][1:].isdigit())):
        records_list.append(entry)
    else:
        sys.stderr.write(f"Invalid input format: {entry}")
        sys.stderr.write(f"Please use 'description amount' format.\n")

def add_records(records_list):
    try:
        print('Add expense or income records with description and amount:')
        print("desc1 amt1, desc2 amt2, desc3 amt3, ...")
        records = input('')
        #Check if the user enters multi data that is seperated by a coma
        if has_comma(records):
            process_with_comma(records_list, records)
        else:
        #If no coma, try adding to the records
            process_without_comma(records_list, records)

    except Exception as e:
        sys.stderr.write(f"An error occurred, When trying to Add Records: {e}\n")


def view_records(records_list, balance):
    try:
        # Print the records
        print("Here's your expense and income records:")
        print(f"{'Description':<20} {'Amount'}")
        print("=" * 30)

        total_amount = 0
        for record in records_list:
            desc, amt = record.split()
            amt = int(amt)
            total_amount += amt
            print(f"{desc:<20} {amt}")

        print("=" * 30)
        #print(f"{'Total':<20} {total_amount}")
        print(f"Now you have {balance + total_amount} dollars.")
    except Exception as e:          #Exceptoion 8
        sys.stderr.write(f"An error occurred, When trying to View Records: {e}\n")

def delete_record(records_list, balance):
    try:
        delete_desc = input("Which record do you want to delete?: ")
        found = False
        last_index = -1
        #Check if there is something to delete
        for i, record in enumerate(records_list):
            desc, amt = record.split()
            if desc == delete_desc:
                found = True
                last_index = i
        #If found delete that data
        if found:
            desc, amt = records_list[last_index].split()
            balance -= int(amt)
            del records_list[last_index]
        else:
            print("Invalid description.")
    except Exception as e:     #Exception 7
        sys.stderr.write(f"An error occurred, When trying to Delete Records: {e}\n")

def save_records(records_list, balance):
    try:
        with open('records.txt', 'w') as file:
            for record in records_list:
                # Check if the record is not an empty line
                if record.strip():
                    file.write(record + '\n')
            file.write(f"Balance: {balance}\n")
        print("Records saved to records.txt")
    except Exception as e:      #Exception 6
        sys.stderr.write(f"An error occurred when trying to save records: {e}\n")


def initialize():
    try:
        with open('records.txt', 'r') as file:
            records_lines = file.readlines()

        # Extract records and balance from the file
        records_list = []
        invalid_lines = []
        for line in records_lines[:-1]:
            if has_comma(line):
                process_with_comma(records_list, line)
            else:
                process_without_comma(records_list, line)

        # Check if the last line (balance line) has the correct format
        last_line = records_lines[-1].strip().split(":")
        if len(last_line) == 2 and last_line[0].strip() == 'Balance' and last_line[1].strip().isdigit():
            balance = int(last_line[1].strip())
            print("Welcome Back!")
        else:
            raise ValueError("Invalid balance line format")
        #Find the invalid line that is saved in the text file by the user  
        if invalid_lines:
            sys.stderr.write(f"Invalid input formats in records.txt:\n")
            for line in invalid_lines:
                sys.stderr.write(f"{line.strip()}\n")

    #Exception Handling 
    except FileNotFoundError:
        # If records.txt doesn't exist, prompt for initial balance
        balance = get_initial_balance()
        records_list = []
    except RuntimeError as e: #Exceptoion 1
        sys.stderr.write(f"An error occurred, RuntimeError: {e}\n")
        sys.stderr.write(f"Invalid format in records.txt. Adjusting the contents.\n")
        # If an error occurs, clear the contents of the file
        with open('records.txt', 'w') as file:
            file.write("")
        # Prompt for initial balance
        balance = get_initial_balance()
        records_list = []
    except IndexError as e:   #Exceptoion 2
        sys.stderr.write(f"An error occurred, IndexError: {e}\n")
        sys.stderr.write(f"Invalid format in records.txt. Adjusting the contents.\n")
        # If an error occurs, clear the contents of the file
        with open('records.txt', 'w') as file:
            file.write("")
        # Prompt for initial balance
        balance = get_initial_balance()
        records_list = []
    except ValueError as e:   #Exceptoion 3
        #print("Raised Value error")
        sys.stderr.write(f"An error occurred, ValueError: {e}\n")
        sys.stderr.write(f"Invalid format in records.txt. Adjusting the contents.\n")
        # If an error occurs, clear the contents of the file
        with open('records.txt', 'w') as file:
            file.write("")
        # Prompt for initial balance
        balance = get_initial_balance()
        records_list = []
    except PermissionError as e: #Exceptoion 4
        sys.stderr.write(f"An error occurred, PermissionError: {e}\n")
        sys.stderr.write(f"Invalid format in records.txt. Adjusting the contents.\n")
        # If an error occurs, clear the contents of the file
        with open('records.txt', 'w') as file:
            file.write("")
        # Prompt for initial balance
        balance = get_initial_balance()
        records_list = []
    except Exception as e:    #Exceptoion 5
        sys.stderr.write(f"An unexpected error occurred, Other Exception: {e}\n")
        sys.stderr.write(f"Invalid format in records.txt. Adjusting the contents.\n")
        # If an error occurs, clear the contents of the file
        with open('records.txt', 'w') as file:
            file.write("")
        # Prompt for initial balance
        balance = get_initial_balance()
        records_list = []

    return records_list,balance

def main():
    #First try to inilize
    records_list, balance = initialize()
    while True:
        #Wait for command
        command = input("What do you want to do (add / view / delete / exit)?")
        #Choose command
        if command == "add":
            add_records(records_list)
        elif command == "view":
            view_records(records_list, balance)
        elif command == "delete":
            delete_record(records_list, balance)  
        elif command == "exit":
            save_records(records_list, balance)
            break
        else:
            #Try again
            sys.stderr.write("Invalid command. Please enter add, view, delete, or exit.\n")

if __name__ == "__main__":
    main()