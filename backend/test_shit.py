from database import Session
from sqlalchemy import select
from models.user import User
from models.account import Account
from models.workspace import Workspace
from models.workspace_member import WorkspaceMember
from models.transaction import Transaction
import services.workspace_services as ws_serv


session = Session()


def main():
	user = session.get(User, 2)
	for account in user.accounts:
		print(account.name)


	# while True:

	# 	print("\n===== Family Finance =====")
	# 	print("1. Create user")
	# 	print("2. List users")

	# 	print("3. Add an account to a user")
	# 	print("4. List accounts")

	# 	print("5. Create workspace")
	# 	print("6. List workspaces")
		
	# 	print("7. Add a member to a workspace")
	# 	print("8. List members of a workspace")

	# 	print("9. Add transaction")

	# 	print("10. Exit")

	# 	choice = input("Choice: ")

	# 	if choice == "1":
	# 		name = input("Name: ")
	# 		login = input("Login: ")
	# 		password = input("Password: ")
	# 		role = input("Role: ")
	# 		user = User(name=name, password_hash=password,
	# 					login=login, role=role, created_at= "now")
	# 		session.add(user)
	# 		session.commit()
	# 	elif choice == "2":
	# 		for user in session.scalars(select(User)).all():
	# 			print(user.id, user.name)

	# 	elif choice == "3":
	# 		name = input("Name: ")
	# 		acc_type = input("type: ")
	# 		currency = input("currency: ")
	# 		owner_login = input("Owner: ")
	# 		stmt = select(User).where(User.login == owner_login)
	# 		owner = session.scalars(stmt).first()
	# 		account = Account(name=name, acc_type=acc_type,
	# 					currency=currency, owner_id=owner.id, created_at= "now")
	# 		session.add(account)
	# 		session.commit()
	# 	elif choice == "4":
	# 		for acc in session.scalars(select(Account)).all():
	# 			print(acc.name, acc.currency)

	# 	elif choice == "5":
	# 		name = input("Name: ")
	# 		description = input("Description: ")
	# 		workspace = Workspace(name=name, description=description, created_at= "now")
	# 		session.add(workspace)
	# 		session.commit()
	# 	elif choice == "6":
	# 		for workspace in session.scalars(select(Workspace)).all():
	# 			print(workspace.id, workspace.name, workspace.description)

	# 	elif choice == "7":
	# 		user_id = input("User id: ")
	# 		workspace_id = input("Workspace id: ")
	# 		permission = input("Permission: ")
	# 		workspace_member = WorkspaceMember(user_id=user_id, workspace_id=workspace_id, permission= permission)
	# 		session.add(workspace_member)
	# 		session.commit()
	# 	elif choice == "8":
	# 		workspace_id = input("Workspace_id: ")
	# 		for user in ws_serv.get_users(workspace_id, session):
	# 			print(user.name)

	# 	elif choice == "9":
	# 		workspace_id = input("Worksapce_id: ")
	# 		print("Who sent?")
	# 		for user in ws_serv.get_users(workspace_id, session):
	# 			print(user.name)
	# 		source_user_name = input()
	# 		amount = input("Amount: ")
	# 		currency = input("Currency: ")
	# 		description = input("Description: ")
	# 		transaction = Transaction(created_at= "now",
	# 			description = description,
	# 			transact_type = "",	
	# 			workspace_id = workspace_id,
	# 			deleted_by = "",
	# 			deleted_at= "",
	# 			amount = amount,
	# 			currency = currency,
	# 			beneficiary_acc = 1,
	# 			source_acc = 1,
	# 			beneficiary_workspace_member = 1,
	# 			source_workspace_member = 1,
	# 			data_source = "")
	# 		session.add(transaction)
	# 		session.commit()

			
			

	# 	elif choice == "10":
	# 		break

	# 	else:
	# 		print("Invalid choice")


if __name__ == "__main__":
	main()
