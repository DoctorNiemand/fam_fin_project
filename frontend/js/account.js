/* =========================================================
   Family Finance
   Account page
   ========================================================= */

function getAccountId() {
    const params = new URLSearchParams(
        window.location.search
    );

    const accountId =
        Number(params.get("account_id"));

    if (!accountId) {
        return null;
    }

    return accountId;
}


async function loadAccount() {

    const accountId = getAccountId();

    if (!accountId) {
        console.error("No account ID provided.");
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/accounts/${accountId}?user_id=${CURRENT_USER_ID}`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to load account: ${response.status}`
            );
        }

        const account = await response.json();

        document.getElementById(
            "account-name"
        ).textContent =
            account.name.charAt(0).toUpperCase() +
            account.name.slice(1);

        document.getElementById(
            "account-breadcrumb-name"
        ).textContent =
            account.name.charAt(0).toUpperCase() +
            account.name.slice(1);

        document.getElementById(
            "account-type"
        ).textContent = account.acc_type;

        document.getElementById(
            "account-currency"
        ).textContent = account.currency;

        document.getElementById(
            "account-details-type"
        ).textContent = account.acc_type;

        document.getElementById(
            "account-details-currency"
        ).textContent = account.currency;

        const ownerResponse = await fetch(
            `${API_BASE_URL}/users/${account.owner_id}`
        );

        if (ownerResponse.ok) {
            const owner = await ownerResponse.json();

            document.getElementById(
                "account-details-owner"
            ).textContent = owner.name;
        }

        await loadAccountValue(
            accountId,
            account.currency
        );

    } catch (error) {

        console.error(error);

        document.getElementById(
            "account-name"
        ).textContent = "Failed to load account";
    }
}

async function loadAccountValue(
    accountId,
    currency
) {

    try {
        const response = await fetch(
            `${API_BASE_URL}/accounts/${accountId}/value?user_id=${CURRENT_USER_ID}`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to load account value: ${response.status}`
            );
        }

        const data = await response.json();

        const valueElement =
            document.getElementById("account-value");

        const value =
            Number(data.value);

        valueElement.textContent =
            `${value.toFixed(2)} ${currency}`;

        valueElement.classList.remove(
            "positive",
            "negative"
        );

        if (value > 0) {
            valueElement.classList.add("positive");
        } else if (value < 0) {
            valueElement.classList.add("negative");
        }

    } catch (error) {

        console.error(error);

        document.getElementById(
            "account-value"
        ).textContent = "Failed to load";
    }
}

async function loadAccountTransactions() {

    const accountId = getAccountId();

    const container =
        document.getElementById("account-transactions");

    if (!accountId || !container) {
        return;
    }

    try {

        const transactions =
            await fetchTransactions({
                type: "account",
                id: accountId
            });

        container.innerHTML = "";

        if (transactions.length === 0) {
            container.innerHTML =
                "<p>No transactions found.</p>";

            return;
        }

        transactions.forEach(transaction => {
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

function setupAccountTabs() {

    const transactionsTab =
        document.getElementById("account-transactions-tab");

    const detailsTab =
        document.getElementById("account-details-tab");

    const transactionsPanel =
        document.getElementById("account-transactions");

    const detailsPanel =
        document.getElementById("account-details-panel");

    if (
        !transactionsTab ||
        !detailsTab ||
        !transactionsPanel ||
        !detailsPanel
    ) {
        return;
    }

    transactionsTab.addEventListener("click", () => {

        transactionsTab.classList.add("active");
        detailsTab.classList.remove("active");

        transactionsPanel.hidden = false;
        detailsPanel.hidden = true;
    });

    detailsTab.addEventListener("click", () => {

        detailsTab.classList.add("active");
        transactionsTab.classList.remove("active");

        transactionsPanel.hidden = true;
        detailsPanel.hidden = false;
    });
}

function setupDeleteAccount() {
    const button = document.getElementById("delete-account-button");

    if (!button) {
        return;
    }

    button.addEventListener("click", async () => {
        const accountId = getAccountId();

        if (!accountId) {
            return;
        }

        const confirmed = confirm(
            "Are you sure you want to delete this account?"
        );

        if (!confirmed) {
            return;
        }

        try {
            const response = await fetch(
                ``,
                {
                    method: "DELETE"
                }
            );

            if (!response.ok) {
                const error = await response.json().catch(() => null);

                throw new Error(
                    error?.detail ||
                    `Failed to delete account: ${response.status}`
                );
            }

            // Refresh sidebar workspaces
            userAccountPromise = null;
            await loadUserAccounts();

            // Go back to dashboard
            window.location.href = "index.html";

        } catch (error) {
            console.error(error);
            alert(`Failed to delete workspace: ${error.message}`);
        }
    });
}

document.addEventListener(
    "DOMContentLoaded",
    async () => {
        setupAccountTabs();
        await loadAccount();
        await loadAccountTransactions();
    }
);