/* =========================================================
   Family Finance
   Transaction page controller
   ========================================================= */

function getTransactionContext() {
    const params = new URLSearchParams(window.location.search);

    if (params.has("workspace_id")) {
        return {
            type: "workspace",
            id: Number(params.get("workspace_id"))
        };
    }

    if (params.has("account_id")) {
        return {
            type: "account",
            id: Number(params.get("account_id"))
        };
    }

    return {
        type: "user",
        id: null
    };
}

async function initializeTransactionPage() {
    const transactionTable =
        document.getElementById("transactions-table");

    const searchInput =
        document.getElementById("transaction-search");

    const params = new URLSearchParams(window.location.search);
    const openNewTransaction = params.get("new_transaction") === "true";

    if (!transactionTable) {
        return;
    }

    const deletedCheckbox =
        document.querySelector(".deleted-toggle input");

    const context = getTransactionContext();

    async function loadTransactions() {
        try {
            transactions = await fetchTransactions(
                context,
                deletedCheckbox?.checked ?? false
            );

            renderTransactions(
                transactionTable,
                transactions
            );
        } catch (error) {
            console.error(error);
            showTransactionError(transactionTable);
        }
    }

    if (deletedCheckbox) {
        deletedCheckbox.addEventListener(
            "change",
            loadTransactions
        );
    }

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const filteredTransactions = searchTransactions(
                transactions,
                searchInput.value
            );

            renderTransactions(
                transactionTable,
                filteredTransactions
            );
        });
    }

    await loadTransactions();
    setupTransactionSorting(
        document.getElementById("transactions-table")
    );

    if (openNewTransaction) {
        const newTransactionButton =
            document.getElementById("new-transaction-button");

        if (newTransactionButton) {
            newTransactionButton.click();
        }
    }
}

/* =========================================================
   Transaction page initialization
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    initializeTransactionPage
);
