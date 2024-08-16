#Get input
balance = input('How much money do you have?\n')
income_record = input('Add an expense or income record with description and amount:\n')
#Get int
income_record = income_record.split()
income_record_price = int(income_record[1])
#Calculate balance
balance = int(balance)
balance += income_record_price
print(f"Now you have {balance} dollars.")