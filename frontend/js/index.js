/* =========================================================
   Family Finance
   Dashboard
   ========================================================= */

async function loadUserPosition() {
	const position = document.getElementById("user-position");

	if (!position) {
		return;
	}

	try {
		const response = await fetch(
			`${API_BASE_URL}/users/${CURRENT_USER_ID}/debts`
		);

		if (!response.ok) {
			throw new Error(
				`Failed to load user position: ${response.status}`
			);
		}

		const debts = await response.json();

		const balances = {
			EUR: debts.eur ?? 0,
			RUB: debts.rub ?? 0,
			USD: debts.usd ?? 0
		};

		position.querySelectorAll(".balance-card").forEach(card => {
			const currency =
				card.querySelector(".balance-currency").textContent.trim();

			const valueElement =
				card.querySelector(".balance-value");

			const value = balances[currency] ?? 0;

			valueElement.textContent =
				`${value >= 0 ? "+" : ""}${value.toFixed(2)} ${currency}`;

			valueElement.classList.remove("positive", "negative");

			if (value > 0) {
				valueElement.classList.add("positive");
			} else if (value < 0) {
				valueElement.classList.add("negative");
			}
		});

	} catch (error) {
		console.error(error);

		position.querySelectorAll(".balance-value").forEach(element => {
			element.textContent = "Failed to load";
		});
	}
}

async function loadRecentTransactions() {
	const container =
		document.getElementById("user-transactions");

	if (!container) {
		return;
	}

	try {
		const context = {
			type: "user",
			id: null
		};

		const allTransactions =
			await fetchTransactions(context);

		const recentTransactions =
			[...allTransactions]
				.sort(
					(a, b) =>
						new Date(b.created_at) -
						new Date(a.created_at)
				)
				.slice(0, 5);

		container.innerHTML = "";

		recentTransactions.forEach(transaction => {
			container.appendChild(
				createTransactionElement(transaction)
			);
		});

	} catch (error) {
		console.error(error);

		container.innerHTML = `
            <div class="transaction-error">
                Failed to load transactions.
            </div>
        `;
	}
}

function setupDashboardActions() {
	const newTransactionButton =
		document.getElementById("new-transaction-button");

	const viewAllButton =
		document.getElementById("view-all-transactions-button");

	if (newTransactionButton) {
		newTransactionButton.addEventListener("click", () => {
			window.location.href =
				"transactions.html?new_transaction=true";
		});
	}

	if (viewAllButton) {
		viewAllButton.addEventListener("click", () => {
			window.location.href =
				"transactions.html";
		});
	}
}


document.addEventListener(
	"DOMContentLoaded",
	async () => {
		setupDashboardActions();

		await loadUserPosition();
		await loadRecentTransactions();
	}
);