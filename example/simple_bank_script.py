
# Repeated symbol count for header messages
BORDER_CNT = 25

# Menu options
DEPOSIT_FUNDS = "1"
WITHDRAW_FUNDS = "2"
VIEW_BALANCE = "3"
CLOSE_ACCOUNT = "4"

# Print a "hello" message
print(
	"\n" + ("*" * BORDER_CNT) +
	"\n" + "Welcome to Banco Popular!\n" +
	"\n" + ("*" * BORDER_CNT)
)

# Print the Account Setup header
print(
	"\n" + ("-" * BORDER_CNT) + "\nAccount Setup\n" + ("-" * BORDER_CNT) + "\n"
)

# Set up the account
name = input("Account name: ")
balance = round(float(input("Starting balance: $")), 2)

# Welcome!
print(
	"\nWelcome new account member!\n"
	f"Account {name} created with starting balance: ${balance:.2f}"
)

# Ask the user to make a choice...
choice = input(
	"\nSelect option:\n"
	"(1) Deposit funds\n"
	"(2) Withdraw funds\n"
	"(3) View bank account balance\n"
	"(4) Close account\n"
)

if choice == DEPOSIT_FUNDS:
	# Print the header
	print(
		"\n" + ("-" * BORDER_CNT) +
		"\n" + "Deposit Funds" +
		"\n" + ("-" * BORDER_CNT)
	)

	# Get the amount we're going to deposit
	deposit_amt = round(float(input("Amount to deposit: $")), 2)

	if deposit_amt <= 0:
		# The transaction fails because the deposit amount is invalid (<= 0)
		print("Transaction failed: Invalid deposit amount.")
	else:
		# If the transaction is valid, we go through with it
		balance += deposit_amt

		# Finally, print the 'receipt'
		print(f"Account Name: {name}")
		print(f"Deposit Amount: ${deposit_amt:.02f}")
		print(f"New Balance: ${balance:.02f}")

elif choice == WITHDRAW_FUNDS:
	# Print the header
	print(
		"\n" + ("-" * BORDER_CNT) +
		"\n" + "Withdraw Funds" +
		"\n" + ("-" * BORDER_CNT)
	)

	# Get the amount we're going to withdraw
	withdraw_amt = round(float(input("Amount to withdraw: $")), 2)

	if withdraw_amt <= 0:
		# The transaction fails, because the requested amount is negative (or 0)
		print("Transaction failed: Invalid withdrawal amount.")
	else:
		# Calculate the hypothetical balance if the transaction WERE to be done
		hypothetical_balance = balance - withdraw_amt

		# Calculate the penalty
		if hypothetical_balance >= -100:
			penalty_percent = 0.00
		elif hypothetical_balance > -1000:
			penalty_percent = 0.01
		elif hypothetical_balance > -5000:
			penalty_percent = 0.03
		else:
			penalty_percent = -1
		
		if penalty_percent == -1:
			# The balance WOULD be too low, so the transaction fails
			print(
				"Transaction failed: withdrawal amount exceeds overdraft limit."
			)
		else:
			# Print penalty (if any)
			if penalty_percent != 0:
				print(
					"Withdrawal amount is greater than account balance. "
					f"Overdraft penalty of {int(penalty_percent * 100)}%"
					" applied."
				)
			
			# Do the calculation
			penalty_amt = withdraw_amt * penalty_percent
			balance = hypothetical_balance - penalty_amt
			
			# Print the receipt
			print(f"Account Name: {name}")
			print(f"Withdrawal Amount: ${withdraw_amt:.02f}")
			print(f"Penalties: ${penalty_amt:.02f}")
			print(f"New Balance: ${balance:.02f}")

elif choice == VIEW_BALANCE:
	# Print the header
	print(
		"\n" + ("-" * BORDER_CNT) +
		"\n" + "Account Balance" +
		"\n" + ("-" * BORDER_CNT)
	)

	# Print out the balance
	print(f"Account Name: {name}")
	print(f"Balance: ${balance:.02f}")

elif choice == CLOSE_ACCOUNT:
	# This... isn't done yet.
	print("TODO")

else:
	# If none of the options go through, it's an invald option!
	print("Invalid option")

print("\nThank you for banking with Banco Popular!")

# To make a tester from this file, simply run the following command:
# python ../src/test_generator.py simple_bank_script.py tests.json bank_test && python bank_test test_bank_script.py
