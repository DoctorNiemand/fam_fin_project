/* =========================================================
   Family Finance
   Workspace context / navigation
   ========================================================= */



async function loadWorkspaceDebts() {

    const workspaceDebts =
        document.getElementById("workspace-debts");

    if (!workspaceDebts) {
        return;
    }

    const workspaceId = getWorkspaceId();

    if (!workspaceId) {
        return;
    }

    try {

        const response = await fetch(
            `${API_BASE_URL}/workspaces/${workspaceId}/debts?user_id=${CURRENT_USER_ID}`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to load workspace debts: ${response.status}`
            );
        }

        const debts = await response.json();

        workspaceDebts.innerHTML = "";

        debts.forEach(debt => {

            const row =
                document.createElement("div");

            row.className = "debt-row";

            const values = [];

            if (debt.usd !== 0) {
                values.push({
                    amount: debt.usd,
                    currency: "USD"
                });
            }

            if (debt.eur !== 0) {
                values.push({
                    amount: debt.eur,
                    currency: "EUR"
                });
            }

            if (debt.rub !== 0) {
                values.push({
                    amount: debt.rub,
                    currency: "RUB"
                });
            }

            const valuesHTML = `
                <span class="debt-value ${debt.eur > 0 ? "positive" : debt.eur < 0 ? "negative" : ""}">
                    ${debt.eur !== 0 ? `${debt.eur > 0 ? "+" : ""}${debt.eur.toFixed(2)} EUR` : ""}
                </span>

                <span class="debt-value ${debt.rub > 0 ? "positive" : debt.rub < 0 ? "negative" : ""}">
                    ${debt.rub !== 0 ? `${debt.rub > 0 ? "+" : ""}${debt.rub.toFixed(2)} RUB` : ""}
                </span>

                <span class="debt-value ${debt.usd > 0 ? "positive" : debt.usd < 0 ? "negative" : ""}">
                    ${debt.usd !== 0 ? `${debt.usd > 0 ? "+" : ""}${debt.usd.toFixed(2)} USD` : ""}
                </span>
            `;

            row.innerHTML = `
                <div class="debt-member">
                    ${debt.name}
                </div>

                <div class="debt-values">
                    ${valuesHTML}
                </div>
            `;

            workspaceDebts.appendChild(row);
        });

    } catch (error) {

        console.error(error);

        workspaceDebts.innerHTML = `
            <div class="debt-row">
                <div class="debt-member">
                    Failed to load debts.
                </div>
            </div>
        `;
    }
}

async function loadWorkspaceTransactions() {
    const container = document.getElementById("workspace-transactions");

    if (!container) {
        return;
    }

    try {
        const context = {
            type: "workspace",
            id: getWorkspaceId()
        };

        const allTransactions = await fetchTransactions(context);

        const recentTransactions = [...allTransactions]
            .sort(
                (a, b) =>
                    new Date(b.created_at) - new Date(a.created_at)
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

function setupTransactionActions() {
    const workspaceId = getWorkspaceId();

    const buttons = document.querySelectorAll(
        ".section-actions .button"
    );

    if (buttons.length < 2) {
        return;
    }

    const newTransactionButton = buttons[0];
    const viewAllButton = buttons[1];

    viewAllButton.addEventListener("click", () => {
        window.location.href =
            `transactions.html?workspace_id=${workspaceId}`;
    });

    newTransactionButton.addEventListener("click", () => {
        window.location.href =
            `transactions.html?workspace_id=${workspaceId}&new_transaction=true`;
    });
}

function setupDeleteWorkspace() {
    const button = document.getElementById("delete-workspace-button");

    if (!button) {
        return;
    }

    button.addEventListener("click", async () => {
        const workspaceId = getWorkspaceId();

        if (!workspaceId) {
            return;
        }

        const confirmed = confirm(
            "Are you sure you want to delete this workspace?"
        );

        if (!confirmed) {
            return;
        }

        try {
            const response = await fetch(
                `${API_BASE_URL}/workspaces/${workspaceId}?user_id=${CURRENT_USER_ID}`,
                {
                    method: "DELETE"
                }
            );

            if (!response.ok) {
                const error = await response.json().catch(() => null);

                throw new Error(
                    error?.detail ||
                    `Failed to delete workspace: ${response.status}`
                );
            }

            // Refresh sidebar workspaces
            userWorkspacesPromise = null;
            await loadUserWorkspaces();

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
        setupTransactionActions();
        setupDeleteWorkspace();

        await loadWorkspaceDebts();
        await loadWorkspaceTransactions();
    }
);