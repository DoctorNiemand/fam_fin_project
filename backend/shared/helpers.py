def choose_enum(enum_type):
	values = list(enum_type)

	for i, value in enumerate(values, 1):
		print(i, value.name)

	choice = int(input())

	return values[choice - 1]

def choose_user(users, prompt="Choose user"):
	print(prompt)

	for i, u in enumerate(users, 1):
		print(f"{i}. {u.name}")

	while True:
		try:
			choice = int(input("Choice: "))
			if 1 <= choice <= len(users):
				return users[choice - 1]
		except ValueError:
			pass

		print("Invalid choice.")
