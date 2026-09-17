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
        document.getElementById("global-debts");

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
                        <span class="debt-value ${
                            value.amount > 0
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

        container.innerHTML = "";

        for (const workspace of workspaces) {

            const response = await fetch(
                `${API_BASE_URL}/workspaces/${workspace.id}/debts?user_id=${CURRENT_USER_ID}`
            );

            if (!response.ok) {
                throw new Error(
                    `Failed to load debts for workspace ${workspace.id}: ${response.status}`
                );
            }

            const debts =
                await response.json();

            const rows = debts.filter(debt =>
                debt.eur !== 0 ||
                debt.rub !== 0 ||
                debt.usd !== 0
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
                            <span class="debt-value ${
                                value.amount > 0
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

    const workspaceId =
        getWorkspaceId();

    if (workspaceId) {

        // Workspace-specific debts page

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
                        `${workspace.name} — Debts`;
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

        await loadUserPosition();
        await loadGlobalDebts();
    }
}


document.addEventListener(
    "DOMContentLoaded",
    async () => {
        await setupPage();
    }
);