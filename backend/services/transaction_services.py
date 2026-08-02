from sqlalchemy.orm import Session
from sqlalchemy import select

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember
from models.user import User
from models.transaction import Transaction


# payer_id_id is a workspace member id
# beneficiaries are worksp members too
def shared_payment(session: Session,
    workspace_id: int,
    payer_id: int,
    value: float,
    currency: str,
    description: str,
    recipients_list: list[int],
    shares_list: list[float] | None = None
):
	
	if shares_list is None:
		shares_list = [1 / len(recipients_list)] * len(recipients_list)
	elif (len(shares_list) != len(recipients_list)):
		raise ValueError("Shares and recipients have different lengths.")
	elif abs(sum(shares_list) - 1) > 1e-6:
		raise ValueError("Shares must sum to 1.")

	for recipient, share in zip(recipients_list, shares_list):
		transaction = Transaction(amount = value * share, description=description, 
							currency=currency, transact_type = "shared_payment",
							beneficiary_workspace_member = recipient,
							source_workspace_member = payer_id,
							workspace_id = workspace_id,
							created_at= "now"
							)
		session.add(transaction)
	session.commit()
