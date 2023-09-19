B=25
print("\n"+("*"*B)+"\n"+"Welcome to Banco Popular!\n"+"\n"+("*"*B))
print("\n"+("-"*B)+"\nAccount\nSetup\n"+("-"*B)+"\n")
u=input("Account name:")
k=round(float(input("Starting balance:$")), 2)
print(f"\nWelcome new account member!\nAccount {u} created with starting balance:${k:.2f}")
z=input("\nSelect option:\n(1) Deposit funds\n(2) Withdraw funds\n(3) View bank account balance\n(4) Close account\n")
if z=="1":
	print("\n"+("-"*B)+"\n"+"Deposit Funds"+"\n"+("-"*B))
	q=round(float(input("Amount to deposit:$")), 2)
	if q<=0:print("Transaction failed:Invalid deposit amount.")
	else:k+=q;print(f"Account Name:{u}\nDeposit Amount:${q:.02f}\nNew Balance:${k:.02f}")
elif z=="2":
	print("\n"+("-"*B)+"\n"+"Withdraw Funds"+"\n"+("-"*B))
	w=round(float(input("Amount to withdraw:$")), 2)
	if w<=0:print("Transaction failed:Invalid withdrawal amount.")
	else:
		h=k-w
		if h>=-100:p=0.00
		elif h>-1000:p=0.01
		elif h>-5000:p=0.03
		else:p=-1
		if p==-1:print("Transaction failed:withdrawal amount exceeds overdraft limit.")
		else:
			if p!=0:print(f"Withdrawal amount is greater than account balance. Overdraft penalty of {int(p*100)}% applied.")
			t=w*p
			k=h-t
			print(f"Account Name:{u}\nWithdrawal Amount:${w:.02f}\nPenalties:${t:.02f}\nNew Balance:${k:.02f}")
elif z=="3":print(("-"*B),"Account Balance",("-"*B),f"Account Name:{u}\nBalance:${k:.02f}",sep="\n")
elif z=="4":print("TODO")
else:print("Invalid option")
print("\nThank you for banking with Banco Popular!")