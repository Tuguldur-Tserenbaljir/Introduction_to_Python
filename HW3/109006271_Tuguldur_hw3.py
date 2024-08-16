import sys

class Record:
    """
    Represents a financial record.

    Attributes:
    - category (str): The category of the financial record.
    - description (str): A description of the financial transaction.
    - amount (int): The monetary amount associated with the transaction.

    Properties:
    - category: Getter property for accessing the category attribute.
    - description: Getter property for accessing the description attribute.
    - amount: Getter property for accessing the amount attribute.
    """
    def __init__(self, category, description, amount):
        """
        Initialize a financial record with the specified category, description, and amount.

        Parameters:
        - category (str): The category of the financial record.
        - description (str): A description of the financial transaction.
        - amount (int): The monetary amount associated with the transaction.
        """
        # Initialize attributes
        self._category = category
        self._description = description
        self._amount = amount

    @property
    def category(self):
        """Getter property for the category attribute."""
        return self._category

    @property
    def description(self):
        """Getter property for the description attribute."""
        return self._description

    @property
    def amount(self):
        """Getter property for the amount attribute."""
        return self._amount


class Categories:
    """
    Manages a hierarchical list of categories and provides methods for operations.

    Attributes:
    - _categories (list): The hierarchical list of categories.

    Methods:
    - view: Displays the categories in a hierarchical structure.
    - is_category_valid: Checks if a given category is valid within the hierarchy.
    - find_categories: Finds and returns subcategories of a given category using a generator.
    """
    def __init__(self):
        """
        Initializes a Categories instance with a default hierarchical list.
        """
        self._categories = ['expense',['food', ['meal', 'snack', 'drink'], 'transport', ['bus', 'railway']], 'income', ['salary', 'bonus']]

    def view(self, categories=None, index=0):
        """
        Displays the categories in a hierarchical structure.

        Parameters:
        - categories (list, optional): The list of categories to display.
        - index (int, optional): The indentation level for proper formatting.
        """
        if categories is None:
            categories = self._categories
        for item in categories:
            if isinstance(item, list):
                self.view(item, index + 2)
            else:
                print(' ' * index + str(item))

    def is_category_valid(self, category, categories=None):
        """
        Checks if a given category is valid within the hierarchy.

        Parameters:
        - category (str): The category to check for validity.
        - categories (list, optional): The list of categories to search within.

        Returns:
        - bool: True if the category is valid, False otherwise.
        """
        if categories is None:
            categories = self._categories
        if category in categories:
            # Check if the current item is a list (indicating subcategories)
            # and recursively call the function to search within the subcategories.
            return True
        for item in categories:
            if isinstance(item, list) and self.is_category_valid(category, item):
                return True
        return False


    def find_categories(self, category):
            """
                Finds and returns subcategories of a given category using a generator.

                Parameters:
                - category (str): The category for which to find subcategories.

                Returns:
                - list: A list containing the subcategories of the specified category.
            """
            def find_categories_gen(category, categories, found=False):
                if type(categories) == list:
                    for index, child in enumerate(categories):
                         # Recursively yield subcategories using the generator.
                        yield from find_categories_gen(category, child, found)
                         # When the target category is found, set a flag to True
                        # and yield subcategories in the next level.
                        if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list:
                            flag = True
                            for i in categories[index + 1]:
                                yield from find_categories_gen(category, i, flag)
                else:
                    # If the current category matches the target or the flag is True,
                    # yield the current category.
                    if category == categories or found == True:
                        yield categories

            return [i for i in find_categories_gen(category, self._categories)]



class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    """
    Manage a list of 'Record' instances and the initial amount of money.

    Attributes:
    - _records (list): List containing 'Record' instances.
    - _balance (int): The balance amount.
    - _categories_manager (Categories): Instance of the Categories class.
    - _categories (list): The hierarchical list of categories.

    Methods:
    - add: Add records to the list based on user input.
    - view: Display all records and report the current balance.
    - delete: Delete a record based on the provided description.
    - find: Display records based on specified categories and report the total amount.
    - save: Save the current balance and all records to 'records.txt'.
    """
    def __init__(self, categories_manager):
        """
        Initialize a Records instance.

        Parameters:
        - categories_manager (Categories): Instance of the Categories class.
        """
        # Instantiate Categories
        self._records = []
        self._balance = 0
        self._categories_manager = categories_manager
        self._categories = categories_manager._categories 
        # Read from 'records.txt' or prompt for initial amount of money
        try:
            #Try to open the file with method
            with open('records.txt', 'r') as file:
                records_lines = file.readlines()
            print("Welcome back!")
            # Extract records and balance from the file
            self._records = []
            self._initial_money = 0
            invalid_lines = []

            #Get the data of records with their category == part[0], descripton == part[1], amount == part[3]
            for line in records_lines:
                parts = line.strip().split()
                if len(parts) == 3 and parts[0].isalpha() and parts[1].isalpha() \
                        and (parts[2].isdigit() or (parts[2][0] == '-' and parts[2][1:].isdigit())):
                    record = Record(parts[0], parts[1], int(parts[2]))
                    self._records.append(record)
                elif line.startswith('Balance:'):
                #Get balance from the last line of the record.txt file
                    try:
                        self._initial_money = int(line.split(":")[1].strip())
                    except ValueError:
                        sys.stderr.write(f"Invalid balance format in records.txt.\n")
                        self._initial_money = 0
                else:
                    invalid_lines.append(line)
            #Detect and Remove invalid lines from record.txt file
            if invalid_lines:
                sys.stderr.write(f"Invalid input formats in records.txt:\n")
                for line in invalid_lines:
                    sys.stderr.write(f"{line.strip()}\n")
        #Exception handling
        except (FileNotFoundError,RuntimeError,IndexError,ValueError,PermissionError):
            # If records.txt doesn't exist, prompt for initial balance
            self._initial_money = get_initial_balance()
            self._records = []
        except Exception as e:
            sys.stderr.write(f"An unexpected error occurred: {e}\n")
            sys.stderr.write(f"Initializing with default values.\n")
            self._initial_money = 0
            self._records = []

    def add(self, records_input):
        """
        Add records to the list based on user input.

        Parameters:
        - records_input (str): Input string containing records in 'category description amount' format.
        """
        # Convert the input string into a list of Record instances
        #Test if the user enters multi records with their category, desciption, amount
        records_list = records_input.split(',')

        for record_string in records_list:
            record_string = record_string.strip()
            parts = [part.strip() for part in record_string.split()]
            #Check if the entered input of records is valid
            if len(parts) == 3 and parts[0].isalpha() and parts[1].isalpha() \
                    and (parts[2].isdigit() or (parts[2][0] == '-' and parts[2][1:].isdigit())):
                category, description, amount = parts
                new_record = Record(category, description, int(amount))

                # Check if the category is valid
                if self._categories_manager.is_category_valid(category, self._categories):
                    self._records.append(new_record)
                else:
                    sys.stderr.write(f"Invalid category: {category}\n")
            #If the entered input does not match the template, show error message
            else:
                sys.stderr.write(f"Invalid input format: {record_string}\n")
                sys.stderr.write(f"Please use 'category description amount' format.\n")

    def view(self):
        """
        Display all records and report the current balance.
        """
        # Print all the records and report the balance
        total_amount = 0
        print(f"{'Category':<15} {'Description':<20} {'Amount'}")
        print("=" * 55)
        for record in self._records:
            #Filter the data to their respective fields
            category = record.category
            desc = record.description
            amt = record.amount
            total_amount += amt
            print(f"{category:<15} {desc:<20} {amt}")
        print("=" * 55)
        #calculate the balance
        print(f"Now you have {self._initial_money + total_amount} dollars.")

    def delete(self, description):
        """
        Delete a record based on the provided description.

        Parameters:
        - description (str): Description of the record to be deleted.
        """
        try:
            #Reverse the string for the method to delete the last entered duplicate
            found = False
            last_index = -1
            # Check if there is something to delete
            for i, record in enumerate(self._records):
                desc = record.description  # Access the description using attribute
                if desc == description:
                    found = True
                    last_index = i
            # If found, delete that data
            if found:
                category = self._records[last_index].category
                amt = self._records[last_index].amount
                self._balance -= amt
                del self._records[last_index]
                print(f"Record with description '{description}' deleted successfully.")
            #Prompted delete record is not found
            else:
                print("Record not found.")
        #Exception for somewhat reason if the delete function does not work
        except Exception as e:
            sys.stderr.write(f"An error occurred when trying to Delete Records: {e}\n")
    
    def find(self, categories_to_find):
        """
        Display records based on specified categories and report the total amount.

        Parameters:
        - categories_to_find (str): Comma-separated categories to search for.
        """
        # Print the records whose category is in the list passed in
        # and report the total amount of money of the listed records.
        subcategories = self._categories_manager.find_categories(categories_to_find)
        filtered_records = [record for record in self._records if record.category in subcategories or
                            any(subcategory in record.category for subcategory in subcategories)]
        #If the prompted record is not found
        if not filtered_records:
            print(f"No records found for the specified categories.")
            return
        #Print out the found categories
        current_money = 0
        print(f"{'Category':<15} {'Description':<20} {'Amount'}")
        dash = '=' * 40
        print(dash)
        #Print out the amount
        for record in filtered_records:
            print(f"{record.category:<15} {record.description:<20} {record.amount}")
            current_money += int(record.amount)

        print(dash)
        print(f'The total amount above is {current_money} dollars.')

    def save(self):
        """
        Save the current balance and all records to 'records.txt'.
        """
        # Save the balance money and all the records to 'records.txt'.
        try:
            with open('records.txt', 'w') as file:
                for record in self._records:
                    file.write(f"{record.category} {record.description} {record.amount}\n")
                file.write(f"Balance: {self._initial_money}\n")
            print("Records saved to records.txt")
        except Exception as e:
            sys.stderr.write(f"An error occurred when trying to save records: {e}\n")


def get_initial_balance():
    """
    Prompt the user for the initial balance and return the entered value.

    The function attempts to convert the user input to an integer.
    If the input is not a valid integer, it defaults to 0 and displays an error message.

    Returns:
    int: The initial balance entered by the user.
    """
    try:
        balance = int(input('How much money do you have?\n'))
    except (ValueError, TypeError):
        sys.stderr.write(f"Invalid input. Initializing balance to 0.\n")
        balance = 0
    return balance


def main():
    """
    The main function for managing expense and income records.

    It starts the Categories and Records managers, then enters a loop
    To process user commands interactively. User can add records, view records, .
    Delete records, view the category, search for a record based on the category, or exit the program.

    Commands:
    - 'add': Add new records to the system.
    - 'view': Display all existing records and the current balance.
    - 'delete': Remove a specific record by its description.
    - 'view_categories': Display the hierarchical structure of available categories.
    - 'find': Find and display records based on specified categories.
    - 'exit': Save the current records and exit the program.

    Returns:
    None
    """
    categories_manager = Categories()
    records_manager = Records(categories_manager) 

    while True:
        command = input("What do you want to do (add / view / delete / find / view_categories / exit)?")
        if command == "add":
            records_input = input("Enter the record(s) (category description amount): ")
            records_manager.add(records_input)
        elif command == "view":
            records_manager.view()
        elif command == "delete":
            delete_desc = input("Which record do you want to delete?: ")
            records_manager.delete(delete_desc)
        elif command == "view_categories":
            categories_manager.view()
        elif command == "find":
            categories_to_find = input("Enter the categories to find: ")
            records_manager.find(categories_to_find)
        elif command == "exit":
            records_manager.save()
            break
        else:
            sys.stderr.write("Invalid command. Please enter add, view, delete, or exit.\n")

if __name__ == "__main__":
    main()
