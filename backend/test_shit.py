from database import Session
from models.user import User
from models.account import Account
from sqlalchemy import select


session = Session()


def main():

	while True:

		print("\n===== Family Finance =====")
		print("1. Create user")
		print("2. List users")
		print("3. Add an account to a user")
		print("4. List accounts")
		print("5. Exit")

		choice = input("Choice: ")

		if choice == "1":
			name = input("Name: ")
			login = input("Login: ")
			password = input("Password: ")
			role = input("Role: ")
			user = User(name=name, password_hash=password,
						login=login, role=role, created_at= "now")
			session.add(user)
			session.commit()

		elif choice == "2":
			for user in session.scalars(select(User)).all():
				print(user.id, user.name)

		elif choice == "3":
			name = input("Name: ")
			acc_type = input("type: ")
			currency = input("currency: ")
			owner_login = input("Owner: ")
			stmt = select(User).where(User.login == owner_login)
			owner = session.scalars(stmt).first()
			account = Account(name=name, acc_type=acc_type,
						currency=currency, owner_id=owner.id, created_at= "now")
			session.add(account)
			session.commit()

		elif choice == "4":
			for acc in session.scalars(select(Account)).all():
				print(acc.name, acc.currency)

		elif choice == "5":
			break

		else:
			print("Invalid choice")


if __name__ == "__main__":
	main()
