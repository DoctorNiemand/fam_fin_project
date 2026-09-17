/* =========================================================
   Family Finance
   Transaction rendering
   ========================================================= */

function sortTransactions(transactions) {
    return [...transactions].sort((a, b) => {
        let valueA;
        let valueB;

        switch (currentSort.column) {
            case "created_at":
                valueA = new Date(a.created_at);
                valueB = new Date(b.created_at);
                break;

            case "description":
                valueA = a.description ?? "";
                valueB = b.description ?? "";
                break;

            case "workspace":
                valueA = a.workspace_name ?? "";
                valueB = b.workspace_name ?? "";
                break;

            case "type":
                valueA = a.type ?? "";
                valueB = b.type ?? "";
                break;

            case "paid_by":
                valueA = a.paid_by?.name ?? "";
                valueB = b.paid_by?.name ?? "";
                break;

            case "amount":
                valueA = Number(a.amount);
                valueB = Number(b.amount);
                break;

            default:
                return 0;
        }

        let result;

        if (
            typeof valueA === "number" &&
            typeof valueB === "number"
        ) {
            result = valueA - valueB;
        } else if (
            valueA instanceof Date &&
            valueB instanceof Date
        ) {
            result = valueA - valueB;
        } else {
            result = String(valueA).localeCompare(
                String(valueB)
            );
        }

        return currentSort.direction === "asc"
            ? result
            : -result;
    });
}

function setupTransactionSorting() {
    const sortButtons = document.querySelectorAll(".sort-button");

    sortButtons.forEach(button => {
        button.addEventListener("click", () => {
            const column = button.dataset.column;

            if (!column) {
                return;
            }

            if (currentSort.column === column) {
                currentSort.direction =
                    currentSort.direction === "asc"
                        ? "desc"
                        : "asc";
            } else {
                currentSort.column = column;
                currentSort.direction = "asc";
            }

            const transactionTable =
                document.getElementById("transactions-table");

            if (transactionTable) {
                renderTransactions(
                    transactionTable,
                    getVisibleTransactions()
                );
            }
        });
    });
    updateSortIndicators();
}

function updateSortIndicators() {
    const sortButtons = document.querySelectorAll(".sort-button");

    sortButtons.forEach(button => {
        const arrow = button.querySelector("span");

        if (!arrow) {
            return;
        }

        if (button.dataset.column === currentSort.column) {
            arrow.textContent =
                currentSort.direction === "asc"
                    ? "↑"
                    : "↓";
        } else {
            arrow.textContent = "";
        }
    });
}

function toggleTransaction(transactionElement) {
    transactionElement.classList.toggle("expanded");
}

function renderTransactions(transactionTable, transactions) {
    const header = transactionTable.querySelector(
        ".transaction-table-header"
    );

    transactionTable.innerHTML = "";

    if (header) {
        transactionTable.appendChild(header);
    }

    const sortedTransactions = sortTransactions(transactions);

    sortedTransactions.forEach(transaction => {
        transactionTable.appendChild(
            createTransactionElement(transaction)
        );
    });
}

function searchTransactions(transactions, searchTerm) {
    const term = searchTerm.trim().toLowerCase();

    if (!term) {
        return transactions;
    }

    return transactions.filter(transaction => {
        return [
            transaction.description,
            transaction.workspace_name,
            transaction.type,
            transaction.paid_by?.name,
            transaction.paid_to?.name,
            transaction.currency
        ].some(value =>
            String(value ?? "").toLowerCase().includes(term)
        );
    });
}

function getVisibleTransactions() {
    const searchInput =
        document.getElementById("transaction-search");

    if (!searchInput) {
        return transactions;
    }

    return searchTransactions(
        transactions,
        searchInput.value
    );
}

function formatTransactionDate(createdAt) {
    return new Date(createdAt).toLocaleDateString(
        undefined,
        {
            day: "2-digit",
            month: "short"
        }
    );
}

function formatTransactionDateTime(createdAt) {
    return new Date(createdAt).toLocaleString(
        undefined,
        {
            day: "2-digit",
            month: "short",
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}

function formatAmount(amount, currency) {
    return `${Number(amount).toFixed(2)} ${currency}`;
}

function getAmountClass(transaction) {
    const currentUserId = CURRENT_USER_ID;

    if (transaction.paid_by.user_id === currentUserId) {
        return "negative";
    }

    if (transaction.paid_to.user_id === currentUserId) {
        return "positive";
    }

    return "";
}

function showTransactionError(transactionTable) {
    transactionTable.innerHTML = `
        <div class="transaction-error">
            Failed to load transactions.
        </div>
    `;
}

function createTransactionElement(transaction) {
    const element = document.createElement("div");

    element.className = "transaction";

    if (transaction.deleted) {
        element.classList.add("deleted-transaction");
    }

    element.addEventListener("click", event => {
        if (event.target.closest("input, select, textarea, button")) {
            return;
        }

        toggleTransaction(element);
    });

    element.innerHTML = `
        <div class="transaction-date">
            ${formatTransactionDate(transaction.created_at)}
        </div>

        <div class="transaction-main">
            <div class="transaction-description">
                ${transaction.description ?? "—"}
            </div>

            <div class="transaction-meta">
                ${formatTransactionDateTime(transaction.created_at)}
            </div>
        </div>

        <div class="transaction-workspace">
            ${transaction.workspace_name}
        </div>

        <div class="transaction-type">
            ${transaction.type}
        </div>

        <div class="transaction-paid-by">
            ${transaction.paid_by.name}
        </div>

        <div class="transaction-amount ${getAmountClass(transaction)}">
            ${formatAmount(
        transaction.amount,
        transaction.currency
    )}
        </div>

        <div class="transaction-expand">
            ›
        </div>

        <div class="transaction-details">

            <div class="transaction-detail">
                <span>Type</span>
                <span>${transaction.type}</span>
            </div>

            <div class="transaction-detail">
                <span>Workspace</span>
                <span>${transaction.workspace_name}</span>
            </div>

            <div class="transaction-detail">
                <span>Paid by</span>
                <span>${transaction.paid_by.name}</span>
            </div>

            <div class="transaction-detail">
                <span>Paid to</span>
                <span>${transaction.paid_to.name}</span>
            </div>

            ${transaction.source_account
            ? `
                        <div class="transaction-detail">
                            <span>Source account</span>
                            <span>${transaction.source_account.name}</span>
                        </div>
                    `
            : ""
        }

            ${transaction.beneficiary_account
            ? `
                        <div class="transaction-detail">
                            <span>Beneficiary account</span>
                            <span>${transaction.beneficiary_account.name}</span>
                        </div>
                    `
            : ""
        }

            <div class="transaction-detail">
                <span>Amount</span>
                <span>${formatAmount(
            transaction.amount,
            transaction.currency
        )}</span>
            </div>

            <div class="transaction-actions">
                ${transaction.deleted
            ? `
                            <button
                                class="button secondary"
                                type="button"
                                data-action="restore"
                            >
                                Restore
                            </button>
                        `
            : `
                            <button
                                class="button secondary"
                                type="button"
                                data-action="edit"
                            >
                                Edit
                            </button>

                            <button
                                class="button secondary"
                                type="button"
                                data-action="delete"
                            >
                                Delete
                            </button>
                        `
        }
            </div>

        </div>
    `;

    element.addEventListener("click", async event => {
        const button = event.target.closest("[data-action]");

        if (!button) {
            return;
        }

        event.stopPropagation();

        const action = button.dataset.action;

        /*
         * Delete
         */
        if (action === "delete") {
            try {
                await deleteTransaction(transaction.id);
                await initializeTransactionPage();
            } catch (error) {
                console.error(error);
                alert(error.message || "Failed to delete transaction.");
            }
        }

        /*
         * Restore
         */
        if (action === "restore") {
            try {
                await restoreTransaction(transaction.id);
                await initializeTransactionPage();
            } catch (error) {
                console.error(error);
                alert(error.message || "Failed to restore transaction.");
            }
        }

        /*
         * Edit
         */
        if (action === "edit") {
            const details =
                element.querySelector(".transaction-details");

            details.innerHTML = `
                <div class="transaction-detail">
                    <span>Type</span>
                    <span>${transaction.type}</span>
                </div>

                <div class="transaction-detail">
                    <span>Workspace</span>
                    <span>${transaction.workspace_name}</span>
                </div>

                <div class="transaction-detail">
                    <span>Paid by</span>
                    <span>${transaction.paid_by.name}</span>
                </div>

                <div class="transaction-detail">
                    <span>Paid to</span>
                    <span>${transaction.paid_to.name}</span>
                </div>

                <div class="transaction-detail">
                    <span>Source account</span>

                    <select
                        data-edit="source-account"
                    >
                        <option value="">
                            No account
                        </option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <span>Beneficiary account</span>

                    <select
                        data-edit="beneficiary-account"
                    >
                        <option value="">
                            No account
                        </option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <span>Amount</span>

                    <input
                        type="number"
                        step="0.01"
                        value="${transaction.amount}"
                        data-edit="amount"
                    >
                </div>

                <div class="transaction-detail">
                    <span>Currency</span>

                    <select data-edit="currency">
                        <option
                            value="EUR"
                            ${transaction.currency === "EUR"
                    ? "selected"
                    : ""
                }
                        >
                            EUR
                        </option>

                        <option
                            value="USD"
                            ${transaction.currency === "USD"
                    ? "selected"
                    : ""
                }
                        >
                            USD
                        </option>

                        <option
                            value="RUB"
                            ${transaction.currency === "RUB"
                    ? "selected"
                    : ""
                }
                        >
                            RUB
                        </option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <span>Description</span>

                    <input
                        type="text"
                        value="${transaction.description ?? ""}"
                        data-edit="description"
                    >
                </div>

                <div class="transaction-actions">
                    <button
                        class="button primary"
                        type="button"
                        data-action="save"
                    >
                        Save
                    </button>

                    <button
                        class="button secondary"
                        type="button"
                        data-action="cancel-edit"
                    >
                        Cancel
                    </button>
                </div>
            `;

            element.classList.add("editing");

            /*
             * Load source account options
             */
            if (transaction.paid_by?.user_id) {
                const sourceAccountSelect =
                    details.querySelector(
                        '[data-edit="source-account"]'
                    );

                if (sourceAccountSelect) {
                    try {
                        const response = await fetch(
                            `${API_BASE_URL}/accounts/user/${transaction.paid_by.user_id}`
                        );

                        if (!response.ok) {
                            throw new Error(
                                `Failed to load source accounts: ${response.status}`
                            );
                        }

                        const accounts =
                            await response.json();

                        accounts.forEach(account => {
                            sourceAccountSelect.innerHTML += `
                                <option
                                    value="${account.id}"
                                    ${transaction.source_account?.id ===
                                    account.id
                                    ? "selected"
                                    : ""
                                }
                                >
                                    ${account.name} (${account.currency})
                                </option>
                            `;
                        });

                    } catch (error) {
                        console.error(error);
                    }
                }
            }

            /*
             * Load beneficiary account options
             */
            if (transaction.paid_to?.user_id) {
                const beneficiaryAccountSelect =
                    details.querySelector(
                        '[data-edit="beneficiary-account"]'
                    );

                if (beneficiaryAccountSelect) {
                    try {
                        const response = await fetch(
                            `${API_BASE_URL}/accounts/user/${transaction.paid_to.user_id}`
                        );

                        if (!response.ok) {
                            throw new Error(
                                `Failed to load beneficiary accounts: ${response.status}`
                            );
                        }

                        const accounts =
                            await response.json();

                        accounts.forEach(account => {
                            beneficiaryAccountSelect.innerHTML += `
                                <option
                                    value="${account.id}"
                                    ${transaction.beneficiary_account?.id ===
                                    account.id
                                    ? "selected"
                                    : ""
                                }
                                >
                                    ${account.name} (${account.currency})
                                </option>
                            `;
                        });

                    } catch (error) {
                        console.error(error);
                    }
                }
            }
        }

        /*
         * Cancel edit
         */
        if (action === "cancel-edit") {
            element.classList.remove("editing");

            const refreshedElement =
                createTransactionElement(transaction);

            element.replaceWith(refreshedElement);

            return;
        }

        /*
         * Save edit
         */
        if (action === "save") {
            const amount =
                element.querySelector(
                    '[data-edit="amount"]'
                ).value;

            const currency =
                element.querySelector(
                    '[data-edit="currency"]'
                ).value;

            const description =
                element.querySelector(
                    '[data-edit="description"]'
                ).value;

            const sourceAccount =
                element.querySelector(
                    '[data-edit="source-account"]'
                ).value;

            const beneficiaryAccount =
                element.querySelector(
                    '[data-edit="beneficiary-account"]'
                ).value;

            try {
                await updateTransaction(
                    transaction.id,
                    {
                        amount: Number(amount),
                        currency: currency,
                        description: description || null,
                        source_acc_id: sourceAccount
                            ? Number(sourceAccount)
                            : null,
                        beneficiary_acc_id: beneficiaryAccount
                            ? Number(beneficiaryAccount)
                            : null
                    }
                );

                const context = getTransactionContext();

                const refreshedTransactions =
                    await fetchTransactions(context);

                const updatedTransaction =
                    refreshedTransactions.find(
                        item => item.id === transaction.id
                    );

                if (updatedTransaction) {
                    const refreshedElement =
                        createTransactionElement(
                            updatedTransaction
                        );

                    element.replaceWith(refreshedElement);
                }

            } catch (error) {
                console.error(error);

                alert(
                    error.message ||
                    "Failed to update transaction."
                );
            }
        }
    });

    return element;
}