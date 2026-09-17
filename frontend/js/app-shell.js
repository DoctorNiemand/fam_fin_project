/* =========================================================
   Family Finance
   Global application shell
   ========================================================= */

let userWorkspaces = [];
let userWorkspacesPromise = null;
let userAccounts = [];
let userAccountsPromise = null;


function getWorkspaceId() {
    const params = new URLSearchParams(
        window.location.search
    );

    const workspaceId =
        Number(params.get("workspace_id"));

    if (!workspaceId) {
        return null;
    }

    return workspaceId;
}


function createAppShell() {

    const existingShell =
        document.querySelector(".app");

    if (existingShell) {
        return;
    }

    const shell =
        document.createElement("div");

    shell.className = "app";

    shell.innerHTML = `
        <aside class="sidebar">

            <div class="sidebar-header">
                <div class="logo">
                    Family Finance
                </div>
            </div>

            <nav class="navigation">

                <a href="index.html" class="nav-item" id="dashboard-link">
                    <span class="nav-icon">⌂</span>
                    <span>Dashboard</span>
                </a>

                <div class="nav-section">
                    <div class="nav-section-title">
                        Workspaces
                    </div>

                    <div
                        id="workspace-list"
                        class="nav-section-workspaces"
                    ></div>

                    <a
                        href="#"
                        class="nav-item nav-add-item"
                        id="add-workspace-link"
                    >
                        <span class="nav-icon">+</span>
                        <span>Add workspace</span>
                    </a>
                </div>

                <div class="nav-section">
                    <div class="nav-section-title">
                        Accounts
                    </div>

                    <div id="account-list" class="nav-section-accounts"></div>

                    <a href="#" class="nav-item nav-add-item" id="add-account-link">
                        <span class="nav-icon">+</span>
                        <span>Add account</span>
                    </a>
                </div>
                <a href="#" class="nav-item" id="debts-link-sidebar">
                    <span class="nav-icon">⇄</span>
                    <span>Debts</span>
                </a>
                <a href="#" class="nav-item" id="transactions-link-sidebar">
                    <span class="nav-icon">↔</span>
                    <span>Transactions</span>
                </a>
                <a href="#" class="nav-item nav-add-item" id="add-transaction-link">
                    <span class="nav-icon">+</span>
                    <span>New transaction</span>
                </a>

            </nav>

            <div class="sidebar-bottom">

                <a href="#" class="nav-item" id="settings-link">
                    <span class="nav-icon">⚙</span>
                    <span>Settings</span>
                </a>

            </div>

        </aside>


        <div class="main">

            <header class="topbar">

                <div
                    class="topbar-title"
                    id="workspace-name"
                >
                    Family
                </div>

                <div class="topbar-user">

                    <span id="current-user-name">
                        User
                    </span>

                    <span class="user-arrow">
                        ▾
                    </span>

                </div>

            </header>


            <nav class="workspace-nav">

                <a
                    href="#"
                    id="overview-link"
                    class="workspace-nav-item"
                >
                    Overview
                </a>

                <a
                    href="#"
                    id="transactions-link"
                    class="workspace-nav-item"
                >
                    Transactions
                </a>

                <a
                    href="#"
                    id="debts-link"
                    class="workspace-nav-item"
                >
                    Debts
                </a>

                <a
                    href="#"
                    id="members-link"
                    class="workspace-nav-item"
                >
                    Members
                </a>

            </nav>


            <div id="app-content"></div>

        </div>
    `;

    const pageContent =
        document.getElementById("page-content");

    if (pageContent) {
        const main =
            shell.querySelector(".main");

        main.appendChild(pageContent);
    }

    document.body.appendChild(shell);
}


async function loadCurrentUser() {

    const userNameElement =
        document.getElementById("current-user-name");

    if (!userNameElement) {
        return;
    }

    try {

        const response = await fetch(
            `${API_BASE_URL}/users/${CURRENT_USER_ID}`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to load current user: ${response.status}`
            );
        }

        const user =
            await response.json();

        userNameElement.textContent =
            user.name;

    } catch (error) {

        console.error(error);
    }
}


async function loadWorkspace() {

    const workspaceId =
        getWorkspaceId();

    if (!workspaceId) {
        return null;
    }

    try {

        const response = await fetch(
            `${API_BASE_URL}/workspaces/${workspaceId}?user_id=${CURRENT_USER_ID}`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to load workspace: ${response.status}`
            );
        }

        const workspace =
            await response.json();

        const workspaceNameElements =
            document.querySelectorAll(
                "#workspace-name, #page-workspace-name"
            );

        workspaceNameElements.forEach(element => {
            element.textContent =
                workspace.name;
        });

        return workspace;

    } catch (error) {

        console.error(error);

        return null;
    }
}


function loadUserWorkspaces() {

    if (userWorkspacesPromise) {
        return userWorkspacesPromise;
    }

    userWorkspacesPromise =
        (async () => {

            try {

                const response =
                    await fetch(
                        `${API_BASE_URL}/users/${CURRENT_USER_ID}/workspaces`
                    );

                if (!response.ok) {
                    throw new Error(
                        `Failed to load workspaces: ${response.status}`
                    );
                }

                const workspaces =
                    await response.json();

                userWorkspaces =
                    workspaces;

                const workspaceList =
                    document.getElementById(
                        "workspace-list"
                    );

                if (workspaceList) {

                    workspaceList.innerHTML =
                        "";

                    const currentWorkspaceId =
                        getWorkspaceId();

                    workspaces.forEach(
                        workspace => {

                            const link =
                                document.createElement("a");

                            link.className =
                                "nav-item";

                            if (
                                currentWorkspaceId &&
                                workspace.id ===
                                currentWorkspaceId
                            ) {
                                link.classList.add(
                                    "active"
                                );
                            }

                            link.href =
                                `workspace.html?workspace_id=${workspace.id}`;

                            link.innerHTML = `
                                <span class="nav-icon">▣</span>
                                <span>${workspace.name}</span>
                            `;

                            workspaceList.appendChild(
                                link
                            );
                        }
                    );
                }

                return workspaces;

            } catch (error) {

                console.error(error);

                userWorkspaces = [];

                return [];
            }

        })();

    return userWorkspacesPromise;
}

function loadUserAccounts() {

    if (userAccountsPromise) {
        return userAccountsPromise;
    }

    userAccountsPromise = (async () => {

        try {

            const response = await fetch(
                `${API_BASE_URL}/accounts/user/${CURRENT_USER_ID}`
            );

            if (!response.ok) {
                throw new Error(
                    `Failed to load accounts: ${response.status}`
                );
            }

            const accounts = await response.json();

            userAccounts = accounts;

            const accountList =
                document.getElementById("account-list");

            if (accountList) {

                accountList.innerHTML = "";

                accounts.forEach(account => {

                    const link =
                        document.createElement("a");

                    link.className = "nav-item";

                    link.href =
                        `account.html?account_id=${account.id}`;

                    link.innerHTML = `
                        <span class="nav-icon">▣</span>
                        <span>${account.name}</span>
                    `;

                    accountList.appendChild(link);
                });
            }

            return accounts;

        } catch (error) {

            console.error(error);

            userAccounts = [];

            return [];
        }

    })();

    return userAccountsPromise;
}

function setupWorkspaceNavigation() {

    const addTransactionLink =
        document.getElementById("add-transaction-link");

    if (addTransactionLink) {
        addTransactionLink.href =
            "transactions.html?new_transaction=true";
    }

    const currentPage =
        window.location.pathname.split("/").pop();

    const dashboardLink =
        document.getElementById("dashboard-link");

    if (
        currentPage === "index.html" ||
        currentPage === ""
    ) {
        if (dashboardLink) {
            dashboardLink.classList.add("active");
        }
    }

    const debtsSidebarLink =
        document.getElementById("debts-link-sidebar");

    if (debtsSidebarLink) {
        debtsSidebarLink.href = "debts.html";

        if (
            currentPage === "debts.html" &&
            !getWorkspaceId()
        ) {
            debtsSidebarLink.classList.add("active");
        }
    }

    const workspaceId =
        getWorkspaceId();

    if (!workspaceId) {
        const workspaceNav =
            document.querySelector(".workspace-nav");

        if (workspaceNav) {
            workspaceNav.style.display = "none";
        }

        return;
    }

    const transactionsSidebarLink =
        document.getElementById("transactions-link-sidebar");

    if (transactionsSidebarLink) {
        transactionsSidebarLink.href = "transactions.html";

        if (currentPage === "transactions.html") {
            transactionsSidebarLink.classList.add("active");
        }
    }
    const overviewLink =
        document.getElementById(
            "overview-link"
        );

    const transactionsLink =
        document.getElementById(
            "transactions-link"
        );

    const debtsLink =
        document.getElementById(
            "debts-link"
        );

    const membersLink =
        document.getElementById(
            "members-link"
        );




    if (overviewLink) {
        overviewLink.href =
            `workspace.html?workspace_id=${workspaceId}`;
    }

    if (transactionsLink) {
        transactionsLink.href =
            `transactions.html?workspace_id=${workspaceId}`;
    }

    if (debtsLink) {
        debtsLink.href =
            `debts.html?workspace_id=${workspaceId}`;
    }

    if (membersLink) {
        membersLink.href =
            `members.html?workspace_id=${workspaceId}`;
    }

    if (currentPage === "workspace.html" && overviewLink) {
        overviewLink.classList.add("active");
    }

    if (currentPage === "transactions.html" && transactionsLink) {
        transactionsLink.classList.add("active");
    }

    if (currentPage === "debts.html" && debtsLink) {
        debtsLink.classList.add("active");
    }

    if (currentPage === "members.html" && membersLink) {
        membersLink.classList.add("active");
    }
}


function setupAddWorkspace() {

    const link =
        document.getElementById("add-workspace-link");

    if (!link) {
        return;
    }

    link.addEventListener("click", event => {
        event.preventDefault();

        const name =
            prompt("Workspace name:");

        if (!name || !name.trim()) {
            return;
        }

        createWorkspace(name.trim());
    });
}

async function createWorkspace(name) {
    try {
        const response = await fetch(
            `${API_BASE_URL}/workspaces/?user_id=${CURRENT_USER_ID}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    description: ""
                })
            }
        );

        if (!response.ok) {
            const error = await response.json().catch(() => null);
            throw new Error(
                error?.detail || `Failed to create workspace: ${response.status}`
            );
        }

        await response.json();

        // Refresh the sidebar workspace list
        userWorkspacesPromise = null;
        await loadUserWorkspaces();

    } catch (error) {
        console.error(error);
        alert(`Failed to create workspace: ${error.message}`);
    }
}

function setupAddAccount() {
    const link = document.getElementById("add-account-link");

    if (!link) {
        return;
    }

    link.addEventListener("click", async event => {
        event.preventDefault();

        const name = prompt("Account name:");

        if (!name || !name.trim()) {
            return;
        }

        const accType = prompt(
            "Account type:\n\nbank\ncash\ncrypto"
        );

        if (!accType) {
            return;
        }

        const currency = prompt(
            "Currency:\n\neur\nusd\nrub"
        );

        if (!currency) {
            return;
        }

        try {
            const response = await fetch(
                `${API_BASE_URL}/accounts/`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        user_id: CURRENT_USER_ID,
                        name: name.trim(),
                        acc_type: accType.toLowerCase(),
                        currency: currency.toUpperCase()
                    })
                }
            );

            if (!response.ok) {
                const error = await response.json().catch(() => null);
                const detail = error?.detail;

                throw new Error(
                    Array.isArray(detail)
                        ? detail.map(item => item.msg).join("\n")
                        : detail || `Failed to create account: ${response.status}`
                );
            }

            await response.json();

            // Refresh sidebar account list
            userAccountsPromise = null;
            await loadUserAccounts();

        } catch (error) {
            console.error(error);
            alert(`Failed to create account: ${error.message}`);
        }
    });
}


document.addEventListener(
    "DOMContentLoaded",
    async () => {

        createAppShell();

        setupAddWorkspace();
        setupWorkspaceNavigation();
        setupAddAccount();

        await loadCurrentUser();
        await loadWorkspace();
        await loadUserWorkspaces();
        await loadUserAccounts();

    }
);