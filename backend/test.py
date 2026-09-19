#####################################################
def simplify_one_currency_debts(debtors, creditors):
		debtors_sorted = sorted(
			debtors,
			key=lambda x: x[1],
			reverse=True
		)
		creditors_sorted = sorted(
			creditors,
			key=lambda x: x[1],
			reverse=True
		)
		if not debtors_sorted or not creditors_sorted:
			return []

		simplified = []
		debtor_index = 0
		creditor_index = 0
		debtor, debtor_amount = debtors_sorted[debtor_index]
		creditor, creditor_amount = creditors_sorted[creditor_index]

		while (
			debtor_index < len(debtors_sorted)
			and creditor_index < len(creditors_sorted)
		):
			amount = min(debtor_amount, creditor_amount)

			simplified.append(
				(debtor, creditor, amount)
			)

			debtor_amount -= amount
			creditor_amount -= amount

			if debtor_amount == 0:
				debtor_index += 1

				if debtor_index < len(debtors_sorted):
					debtor, debtor_amount = debtors_sorted[debtor_index]

			if creditor_amount == 0:
				creditor_index += 1

				if creditor_index < len(creditors_sorted):
					creditor, creditor_amount = creditors_sorted[creditor_index]

		return simplified


class Member:
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return self.name


alice = Member("Alice")
bob = Member("Bob")
charlie = Member("Charlie")
ben = Member("ben")
sam = Member("sam")
james = Member("james")
ann = Member("ann")
kyle = Member("kyle") 

debtors = [
	(ben, 10),
	(alice, 100),
	(sam, 31),
	(james, 69)
]

creditors = [
	(bob, 60),
	(charlie, 40),
	(ann, 77),
	(kyle, 33),
]

print(simplify_one_currency_debts(debtors, creditors))
	
#####################################################

#####################################################