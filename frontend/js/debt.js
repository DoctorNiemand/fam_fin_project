/* =========================================================
   Family Finance
   Debts page
   ========================================================= */


async function loadUserPosition() {

    const container =
        document.getElementById("user-position");

    if (!container) {
        return;
    }

    try {

        const response = await fetch(
            `${API_BASE_URL}/users/${CURRENT_USER_ID}/debts`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to load user debt: ${response.status}`
            );
        }

        const debt = await response.json();

        const values = {
            EUR: debt.eur,
            RUB: debt.rub,
            USD: debt.usd
        };

        container
            .querySelectorAll(".balance-card")
            .forEach(card => {

                const currency =
                    card.querySelector(".balance-currency")
                        .textContent
                        .trim();

                const valueElement =
                    card.querySelector(".balance-value");

                const value =
                    Number(values[currency] ?? 0);

                valueElement.textContent =
                    `${value > 0 ? "+" : ""}${value.toFixed(2)}`;

                valueElement.classList.remove(
                    "positive",
                    "negative"
                );

                if (value > 0) {
                    valueElement.classList.add("positive");
                } else if (value < 0) {
                    valueElement.classList.add("negative");
                }
            });

    } catch (error) {

        console.error(error);

        container
            .querySelectorAll(".balance-value")
            .forEach(element => {
                element.textContent = "Failed to load";
            });
    }
}


async function loadWorkspaceDebts() {

    const container =
        document.getElementById("workspace-debts");

    if (!container) {
        return;
    }

    const workspaceId =
        getWorkspaceId();

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

        const debts =
            await response.json();

        container.innerHTML = "";

        const rows = debts.filter(debt =>
            debt.eur !== 0 ||
            debt.rub !== 0 ||
            debt.usd !== 0
        );

        rows.forEach(debt => {

            const row =
                document.createElement("div");

            row.className = "debt-row";

            const values = [];

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

            if (debt.usd !== 0) {
                values.push({
                    amount: debt.usd,
                    currency: "USD"
                });
            }

            row.innerHTML = `
                <div class="debt-member">
                    ${debt.name}
                </div>

                <div class="debt-values">
                    ${values.map(value => `
                        <span class="debt-value ${value.amount > 0
                    ? "positive"
                    : value.amount < 0
                        ? "negative"
                        : ""
                }">
                            ${value.amount > 0 ? "+" : ""}
                            ${value.amount.toFixed(2)}
                            ${value.currency}
                        </span>
                    `).join("")}
                </div>
            `;

            container.appendChild(row);
        });

        if (rows.length === 0) {
            container.innerHTML =
                "<p>No outstanding debts.</p>";
        }

    } catch (error) {

        console.error(error);

        container.innerHTML = `
            <div class="debt-row">
                <div class="debt-member">
                    Failed to load debts.
                </div>
            </div>
        `;
    }
}


async function loadGlobalDebts() {

    const container =
        document.getElementById("global-debts");

    if (!container) {
        return;
    }

    try {

        const workspaceResponse = await fetch(
            `${API_BASE_URL}/users/${CURRENT_USER_ID}/workspaces`
        );

        if (!workspaceResponse.ok) {
            throw new Error(
                `Failed to load workspaces: ${workspaceResponse.status}`
            );
        }

        const workspaces =
            await workspaceResponse.json();

        const personResponse = await fetch(
            `${API_BASE_URL}/users/${CURRENT_USER_ID}/cumulative_pair_debts`
        );

        if (!personResponse.ok) {
            throw new Error(
                `Failed to load cumulative debts: ${personResponse.status}`
            );
        }

        const personDebts = await personResponse.json();
        const personalContainer =
            document.getElementById("personal-debts");

        personalContainer.innerHTML = "";

        const personalRows = personDebts.filter(debt =>
            debt.eur !== 0 ||
            debt.rub !== 0 ||
            debt.usd !== 0
        );
        personalRows.forEach(debt => {
            const row = document.createElement("div");

            row.className = "debt-row";

            const values = [];

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

            if (debt.usd !== 0) {
                values.push({
                    amount: debt.usd,
                    currency: "USD"
                });
            }

            row.innerHTML = `
                <div class="debt-member">
                    ${debt.name}
                </div>

                <div class="debt-values">
                    ${values.map(value => `
                        <span class="debt-value ${value.amount > 0
                    ? "positive"
                    : value.amount < 0
                        ? "negative"
                        : ""
                }">
                            ${value.amount > 0 ? "+" : ""}
                            ${value.amount.toFixed(2)}
                            ${value.currency}
                        </span>
                    `).join("")}
                </div>
            `;

            personalContainer.appendChild(row);
        }); if (personalRows.length === 0) {
            personalContainer.innerHTML =
                "<p>No outstanding debts.</p>";
        }

        container.innerHTML = "";

        for (const workspace of workspaces) {

            const response = await fetch(
                `${API_BASE_URL}/users/${CURRENT_USER_ID}/workspace_pair_debts?workspace_id=${workspace.id}`
            );

            if (!response.ok) {
                throw new Error(
                    `Failed to load debts for workspace ${workspace.id}: ${response.status}`
                );
            }

            const debts =
                await response.json();

            const rows = debts.filter(debt =>
                debt.user_id !== CURRENT_USER_ID &&
                (
                    debt.eur !== 0 ||
                    debt.rub !== 0 ||
                    debt.usd !== 0
                )
            );

            if (rows.length === 0) {
                continue;
            }

            const workspaceSection =
                document.createElement("div");

            workspaceSection.className =
                "debt-workspace";

            workspaceSection.innerHTML = `
                <h3>${workspace.name}</h3>
                <div class="debts-list"></div>
            `;

            const debtsList =
                workspaceSection.querySelector(".debts-list");

            rows.forEach(debt => {

                const row =
                    document.createElement("div");

                row.className = "debt-row";

                const values = [];

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

                if (debt.usd !== 0) {
                    values.push({
                        amount: debt.usd,
                        currency: "USD"
                    });
                }

                row.innerHTML = `
                    <div class="debt-member">
                        ${debt.name}
                    </div>

                    <div class="debt-values">
                        ${values.map(value => `
                            <span class="debt-value ${value.amount > 0
                        ? "positive"
                        : value.amount < 0
                            ? "negative"
                            : ""
                    }">
                                ${value.amount > 0 ? "+" : ""}
                                ${value.amount.toFixed(2)}
                                ${value.currency}
                            </span>
                        `).join("")}

                        <button
                            class="compensate-workspace-debt-button"
                            type="button"
                        >
                            Compensate
                        </button>
                    </div>
                `;
                const compensateButton = row.querySelector(
                    ".compensate-workspace-debt-button"
                );

                compensateButton.addEventListener("click", async () => {
                    const currencies = [];

                    if (debt.eur !== 0) currencies.push(["EUR", debt.eur]);
                    if (debt.usd !== 0) currencies.push(["USD", debt.usd]);
                    if (debt.rub !== 0) currencies.push(["RUB", debt.rub]);

                    if (currencies.length === 0) {
                        return;
                    }

                    if (currencies.length > 1) {
                        alert("This debt contains multiple currencies. Compensation currently supports one currency at a time.");
                        return;
                    }

                    const [currency, amount] = currencies[0];

                    if (!confirm(`Compensate ${Math.abs(amount)} ${currency} with ${debt.name}?`)) {
                        return;
                    }

                    try {
                        const response = await fetch(
                            `${API_BASE_URL}/transactions/compensate` +
                            `?workspace_id=${workspace.id}` +
                            `&user_id=${CURRENT_USER_ID}` +
                            `&other_member_id=${debt.workspace_member_id}` +
                            `&amount=${amount}` +
                            `&currency=${currency}`,
                            {
                                method: "POST"
                            }
                        );

                        if (!response.ok) {
                            throw new Error(await response.text());
                        }

                        await loadGlobalDebts();
                    } catch (error) {
                        console.error("Failed to compensate debt:", error);
                        alert("Failed to compensate debt.");
                    }
                });

                debtsList.appendChild(row);
            });

            container.appendChild(workspaceSection);
        }

        if (!container.children.length) {
            container.innerHTML =
                "<p>No outstanding debts.</p>";
        }

    } catch (error) {

        console.error(error);

        container.innerHTML = `
            <div class="debt-row">
                <div class="debt-member">
                    Failed to load debts.
                </div>
            </div>
        `;
    }
}


async function setupPage() {

    const workspaceId = getWorkspaceId();

    const globalDebtsSection =
        document.querySelector(".global-debts-section");

    const workspaceDebtsSection =
        document.querySelector(".workspace-debts-section");

    const simplifiedDebtsSection =
        document
            .getElementById("simplified-debts")
            ?.closest(".dashboard-section");


    if (workspaceId) {

        // Workspace-specific debts page

        if (globalDebtsSection) {
            globalDebtsSection.style.display = "none";
        }

        if (workspaceDebtsSection) {
            workspaceDebtsSection.hidden = false;
        }

        if (simplifiedDebtsSection) {
            simplifiedDebtsSection.style.display = "block";
        }

        const pageTitle =
            document.querySelector(".page-header h1");

        if (pageTitle) {

            try {
                const response = await fetch(
                    `${API_BASE_URL}/workspaces/${workspaceId}?user_id=${CURRENT_USER_ID}`
                );

                if (response.ok) {

                    const workspace =
                        await response.json();

                    pageTitle.textContent =
                        `Debts`;
                }

            } catch (error) {

                console.error(
                    "Failed to load workspace name:",
                    error
                );
            }
        }

        const positionSection =
            document
                .getElementById("user-position")
                ?.closest(".dashboard-section");

        if (positionSection) {
            positionSection.style.display = "none";
        }

        await loadWorkspaceDebts();

    } else {

        // Global debts page

        if (globalDebtsSection) {
            globalDebtsSection.style.display = "block";
        }

        if (workspaceDebtsSection) {
            workspaceDebtsSection.hidden = true;
        }

        if (simplifiedDebtsSection) {
            simplifiedDebtsSection.style.display = "none";
        }

        await loadUserPosition();
        await loadGlobalDebts();
    }
}

async function loadLatestSettlementSnapshot() {
    const container =
        document.getElementById("simplified-debts");

    if (!container) {
        return;
    }

    const workspaceId = getWorkspaceId();

    if (!workspaceId) {
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/workspaces/${workspaceId}/debts/simplified?user_id=${CURRENT_USER_ID}`
        );

        const settlement = await response.json();

        if (settlement === null) {
            container.innerHTML = `
                <div class="empty-state">
                    No settlement snapshot has been created yet.
                </div>
            `;
            return;
        }

        if (!response.ok) {
            throw new Error(
                `Failed to load settlement snapshot: ${response.status}`
            );
        }

        const createdAt = new Date(settlement.created_at);

        container.innerHTML = `
            <div class="settlement-meta">
                Calculated ${createdAt.toLocaleString()}
            </div>
        `;
        if (settlement.items.length === 0) {
            container.innerHTML += `
                <div class="empty-state">
                    No debts need to be settled.
                </div>
            `;
            return;
        }

        settlement.items.forEach(item => {
            const row = document.createElement("div");

            row.className = "debt-row";

            row.innerHTML = `
                <div class="debt-member">
                    ${item.debtor_name} → ${item.creditor_name}
                </div>

                <div class="debt-values">
                    <span class="debt-value negative">
                        ${item.amount.toFixed(2)} ${item.currency}
                    </span>

                    ${item.transaction_id
                    ? `<span class="settlement-compensated">Compensated</span>`
                    : `<button
                        class="compensate-button"
                        data-settlement-item-id="${item.id}"
                    >
                        Compensate
                    </button>`
                }
                </div>
            `;

            container.appendChild(row);
        });

    } catch (error) {
        console.error(error);

        container.innerHTML = `
            <div class="empty-state">
                Failed to load settlement snapshot.
            </div>
        `;
    }
}

document.addEventListener("click", async (event) => {
    const button = event.target.closest(".compensate-button");
    if (!button) {
        return;
    }
    const workspaceId = getWorkspaceId();
    if (!workspaceId) {
        return;
    }


    const settlementItemId = button.dataset.settlementItemId;

    button.disabled = true;

    try {
        const response = await fetch(

            `${API_BASE_URL}/workspaces/${workspaceId}/debts/simplified/items/${settlementItemId}/compensate?user_id=${CURRENT_USER_ID}`,
            {
                method: "POST"
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to compensate settlement item.");
        }

        await loadWorkspaceDebts();
        await loadLatestSettlementSnapshot();

    } catch (error) {
        console.error(error);
        alert(error.message);
        button.disabled = false;
    }
});

async function recalculateDebts() {
    const workspaceId = getWorkspaceId();

    if (!workspaceId) {
        return;
    }
    if (!confirm("Create a new settlement snapshot using the current debts?")) {
        return;
    }
    const button = document.getElementById("recalculate-debts-button");

    if (button) {
        button.disabled = true;
    }
    try {
        const response = await fetch(
            `${API_BASE_URL}/workspaces/${workspaceId}/debts/simplified?user_id=${CURRENT_USER_ID}&recalculate=true`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to recalculate debts: ${response.status}`
            );
        }

        await loadLatestSettlementSnapshot();

    } catch (error) {
        console.error(error);
    }
    finally {
        if (button) {
            button.disabled = false;
        }
    }
}

document.addEventListener(
    "DOMContentLoaded",
    async () => {
        await setupPage();
        await loadLatestSettlementSnapshot();

        const recalculateButton =
            document.getElementById("recalculate-debts-button");

        if (recalculateButton) {
            recalculateButton.addEventListener(
                "click",
                recalculateDebts
            );
        }
    }
);