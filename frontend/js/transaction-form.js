/* =========================================================
   Family Finance
   Transaction form helpers
   ========================================================= */

function loadTransactionWorkspaces(workspaces) {
    const workspaceSelect =
        document.getElementById("new-transaction-workspace");

    if (!workspaceSelect) {
        return;
    }

    workspaceSelect.innerHTML = `
        <option value="">Select workspace...</option>
    `;

    workspaces.forEach(workspace => {
        workspaceSelect.innerHTML += `
            <option value="${workspace.id}">
                ${workspace.name}
            </option>
        `;
    });
}

async function loadTransactionMembers(workspaceId) {
    if (!workspaceId) {
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/workspaces/${workspaceId}/members?user_id=${CURRENT_USER_ID}`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to load workspace members: ${response.status}`
            );
        }

        const members = await response.json();
        transactionMembers = members.filter(
            member => member.active
        );
        const activeMembers = transactionMembers;

        const payerMemberSelect =
            document.getElementById(
                "new-transaction-payer-member"
            );

        const recipientMemberSelect =
            document.getElementById(
                "new-transaction-recipient-member"
            );

        const recipientMembersSelect =
            document.getElementById(
                "new-transaction-recipient-members"
            );


        /*
         * Payer
         */
        if (payerMemberSelect) {
            payerMemberSelect.innerHTML = `
                <option value="">
                    Select member...
                </option>
            `;

            activeMembers.forEach(member => {
                payerMemberSelect.innerHTML += `
                    <option value="${member.id}">
                        ${member.name}
                    </option>
                `;
            });
        }

        /*
         * Direct transfer recipient
         */
        if (recipientMemberSelect) {
            recipientMemberSelect.innerHTML = `
                <option value="">
                    Select member...
                </option>
            `;

            activeMembers.forEach(member => {
                recipientMemberSelect.innerHTML += `
                    <option value="${member.id}">
                        ${member.name}
                    </option>
                `;
            });
        }

        /*
         * Shared payment recipients
         */
        if (recipientMembersSelect) {
            recipientMembersSelect.innerHTML = "";

            activeMembers.forEach(member => {
                recipientMembersSelect.innerHTML += `
            <label class="transaction-member-option">
                <input
                    type="checkbox"
                    value="${member.id}"
                    name="transaction-recipients"
                >
                <span>${member.name}</span>
            </label>
        `;
            });
        }

        /*
         * Preselect current user as payer
         */
        const currentUserMember = activeMembers.find(
            member => member.user_id === CURRENT_USER_ID
        );

        if (currentUserMember && payerMemberSelect) {
            payerMemberSelect.value = currentUserMember.id;

            loadTransactionAccounts(
                currentUserMember.user_id,
                "new-transaction-source-account"
            );
        }
        if (payerMemberSelect) {
            payerMemberSelect.dataset.userIdMap =
                JSON.stringify(
                    Object.fromEntries(
                        activeMembers.map(member => [
                            member.id,
                            member.user_id
                        ])
                    )
                );
        }

    } catch (error) {
        console.error(error);
    }
}

async function loadTransactionAccounts(userId, selectId) {
    const accountSelect = document.getElementById(selectId);

    if (!accountSelect) {
        return;
    }

    accountSelect.innerHTML = `
        <option value="">
            No account
        </option>
    `;

    if (!userId) {
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/accounts/user/${userId}`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to load accounts: ${response.status}`
            );
        }

        const accounts = await response.json();

        accounts.forEach(account => {
            accountSelect.innerHTML += `
                <option value="${account.id}">
                    ${account.name} (${account.currency})
                </option>
            `;
        });

    } catch (error) {
        console.error(error);
    }
}

/* =========================================================
   Family Finance
   Transaction form
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    const newTransactionButton =
        document.getElementById("new-transaction-button");

    const newTransactionForm =
        document.getElementById("new-transaction-form");

    const cancelNewTransactionButton =
        document.getElementById("cancel-new-transaction-button");

    const transactionType =
        document.getElementById("new-transaction-type");

    const transactionFields =
        document.getElementById("new-transaction-fields");

    const workspaceSelect =
        document.getElementById("new-transaction-workspace");

    if (
        !newTransactionButton ||
        !newTransactionForm ||
        !cancelNewTransactionButton ||
        !transactionType ||
        !transactionFields ||
        !workspaceSelect
    ) {
        return;
    }

    const params = new URLSearchParams(window.location.search);
    const workspaceIdFromUrl = params.get("workspace_id");

    loadUserWorkspaces().then(workspaces => {

        loadTransactionWorkspaces(workspaces);

        if (workspaceIdFromUrl) {
            workspaceSelect.value = workspaceIdFromUrl;
            workspaceSelect.dispatchEvent(
                new Event("change")
            );
        }
    });

    newTransactionButton.addEventListener("click", () => {
        newTransactionForm.style.display = "block";
        transactionType.dispatchEvent(new Event("change"));
    });
    
    const newTransactionFromSidebar =
        params.get("new_transaction") === "true";

    if (newTransactionFromSidebar) {
        newTransactionButton.click();
    }

    cancelNewTransactionButton.addEventListener("click", () => {
        newTransactionForm.style.display = "none";
    });

    workspaceSelect.addEventListener("change", () => {
        transactionType.dispatchEvent(new Event("change"));
    });

    /*
     * Member changes
     */
    transactionFields.addEventListener("change", event => {
        if (
            event.target.name !==
            "transaction-recipients"
        ) {
            return;
        }

        const sharesContainer =
            document.getElementById(
                "new-transaction-shares"
            );

        if (!sharesContainer) {
            return;
        }

        const selectedRecipients =
            document.querySelectorAll(
                'input[name="transaction-recipients"]:checked'
            );

        sharesContainer.innerHTML = "";

        selectedRecipients.forEach(checkbox => {
            const member = transactionMembers.find(
                member =>
                    member.id === Number(checkbox.value)
            );

            if (!member) {
                return;
            }

            sharesContainer.innerHTML += `
            <div class="transaction-share-row">
                <label>
                    ${member.name}
                </label>

                <input
                    type="number"
                    class="transaction-share"
                    data-member-id="${member.id}"
                    min="0"
                    max="1"
                    step="0.01"
                    value=""
                    placeholder="0.00"
                >
            </div>
        `;
        });
    });
    transactionFields.addEventListener("change", event => {
        if (
            event.target.id ===
            "new-transaction-payer-member"
        ) {
            const payerMemberId = Number(
                event.target.value
            );

            const payerMember =
                transactionMembers.find(
                    member =>
                        member.id === payerMemberId
                );

            if (!payerMember) {
                return;
            }

            loadTransactionAccounts(
                payerMember.user_id,
                "new-transaction-source-account"
            );
        }

        if (
            event.target.id ===
            "new-transaction-recipient-member"
        ) {
            const recipientMemberId = Number(
                event.target.value
            );

            const recipientMember =
                transactionMembers.find(
                    member =>
                        member.id === recipientMemberId
                );

            if (!recipientMember) {
                return;
            }

            loadTransactionAccounts(
                recipientMember.user_id,
                "new-transaction-beneficiary-account"
            );
        }
    });

    /*
     * Transaction type
     */
    transactionType.addEventListener("change", () => {
        const workspaceId = workspaceSelect.value;

        if (transactionType.value === "expense") {

            transactionFields.innerHTML = `
                <div class="transaction-detail">
                    <label for="new-transaction-payer-member">
                        Payer
                    </label>

                    <select id="new-transaction-payer-member">
                        <option value="">
                            Select member...
                        </option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-source-account">
                        Source account
                    </label>

                    <select id="new-transaction-source-account">
                        <option value="">
                            No account
                        </option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-amount">
                        Amount
                    </label>

                    <input
                        type="number"
                        id="new-transaction-amount"
                        step="0.01"
                        min="0.01"
                    >
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-currency">
                        Currency
                    </label>

                    <select id="new-transaction-currency">
                        <option value="EUR">EUR</option>
                        <option value="USD">USD</option>
                        <option value="RUB">RUB</option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-description">
                        Description
                    </label>

                    <input
                        type="text"
                        id="new-transaction-description"
                    >
                </div>
            `;

        } else if (transactionType.value === "direct_transfer") {

            transactionFields.innerHTML = `
                <div class="transaction-detail">
                    <label for="new-transaction-payer-member">
                        Payer
                    </label>

                    <select id="new-transaction-payer-member">
                        <option value="">
                            Select member...
                        </option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-source-account">
                        Source account
                    </label>

                    <select id="new-transaction-source-account">
                        <option value="">
                            No account
                        </option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-recipient-member">
                        Recipient
                    </label>

                    <select id="new-transaction-recipient-member">
                        <option value="">
                            Select member...
                        </option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-beneficiary-account">
                        Beneficiary account
                    </label>

                    <select id="new-transaction-beneficiary-account">
                        <option value="">
                            No account
                        </option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-amount">
                        Amount
                    </label>

                    <input
                        type="number"
                        id="new-transaction-amount"
                        step="0.01"
                        min="0.01"
                    >
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-currency">
                        Currency
                    </label>

                    <select id="new-transaction-currency">
                        <option value="EUR">EUR</option>
                        <option value="USD">USD</option>
                        <option value="RUB">RUB</option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-description">
                        Description
                    </label>

                    <input
                        type="text"
                        id="new-transaction-description"
                    >
                </div>
            `;

        } else if (transactionType.value === "shared_payment") {

            transactionFields.innerHTML = `
                <div class="transaction-detail">
                    <label for="new-transaction-payer-member">
                        Payer
                    </label>

                    <select id="new-transaction-payer-member">
                        <option value="">
                            Select member...
                        </option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <label>
                        Recipients
                    </label>

                    <div
                        id="new-transaction-recipient-members"
                        class="transaction-member-list"
                    ></div>
                </div>

                <div
                    id="new-transaction-shares"
                    class="transaction-detail"
                ></div>

                <div class="transaction-detail">
                    <label for="new-transaction-amount">
                        Amount
                    </label>

                    <input
                        type="number"
                        id="new-transaction-amount"
                        step="0.01"
                        min="0.01"
                    >
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-currency">
                        Currency
                    </label>

                    <select id="new-transaction-currency">
                        <option value="EUR">EUR</option>
                        <option value="USD">USD</option>
                        <option value="RUB">RUB</option>
                    </select>
                </div>

                <div class="transaction-detail">
                    <label for="new-transaction-description">
                        Description
                    </label>

                    <input
                        type="text"
                        id="new-transaction-description"
                    >
                </div>
            `;
        }

        if (workspaceId) {
            loadTransactionMembers(workspaceId);
        }
    });
    const createTransactionButton =
        document.getElementById("create-transaction-button");

    if (createTransactionButton) {
        createTransactionButton.addEventListener("click", async () => {
            const workspaceId = Number(
                workspaceSelect.value
            );

            const type = transactionType.value;

            const amount = Number(
                document.getElementById(
                    "new-transaction-amount"
                )?.value
            );

            const currency =
                document.getElementById(
                    "new-transaction-currency"
                )?.value;

            const description =
                document.getElementById(
                    "new-transaction-description"
                )?.value || null;

            if (!workspaceId) {
                alert("Please select a workspace.");
                return;
            }

            if (!amount || amount <= 0) {
                alert("Please enter a valid amount.");
                return;
            }

            let url;
            let body;

            if (type === "expense") {
                const payerMemberId = Number(
                    document.getElementById(
                        "new-transaction-payer-member"
                    )?.value
                );

                const sourceAccountId =
                    document.getElementById(
                        "new-transaction-source-account"
                    )?.value || null;

                if (!payerMemberId) {
                    alert("Please select a payer.");
                    return;
                }

                url = `${API_BASE_URL}/transactions/expense`;

                body = {
                    workspace_id: workspaceId,
                    member_id: payerMemberId,
                    value: amount,
                    currency: currency,
                    payer_acc_id: sourceAccountId
                        ? Number(sourceAccountId)
                        : null,
                    recipient_acc_id: null,
                    description: description
                };

            } else if (type === "direct_transfer") {
                const payerMemberId = Number(
                    document.getElementById(
                        "new-transaction-payer-member"
                    )?.value
                );

                const recipientMemberId = Number(
                    document.getElementById(
                        "new-transaction-recipient-member"
                    )?.value
                );

                const sourceAccountId =
                    document.getElementById(
                        "new-transaction-source-account"
                    )?.value || null;

                const beneficiaryAccountId =
                    document.getElementById(
                        "new-transaction-beneficiary-account"
                    )?.value || null;

                if (!payerMemberId) {
                    alert("Please select a payer.");
                    return;
                }

                if (!recipientMemberId) {
                    alert("Please select a recipient.");
                    return;
                }

                url = `${API_BASE_URL}/transactions/transfer`;

                body = {
                    workspace_id: workspaceId,
                    payer_member_id: payerMemberId,
                    recipient_member_id: recipientMemberId,
                    value: amount,
                    currency: currency,
                    payer_acc_id: sourceAccountId
                        ? Number(sourceAccountId)
                        : null,
                    recipient_acc_id: beneficiaryAccountId
                        ? Number(beneficiaryAccountId)
                        : null,
                    description: description
                };

            } else if (type === "shared_payment") {
                const payerMemberId = Number(
                    document.getElementById(
                        "new-transaction-payer-member"
                    )?.value
                );

                const recipientCheckboxes =
                    document.querySelectorAll(
                        'input[name="transaction-recipients"]:checked'
                    );

                const recipients = Array.from(
                    recipientCheckboxes
                ).map(
                    checkbox => Number(checkbox.value)
                );

                if (!payerMemberId) {
                    alert("Please select a payer.");
                    return;
                }

                if (recipients.length === 0) {
                    alert("Please select at least one recipient.");
                    return;
                }
                const shareInputs =
                    document.querySelectorAll(
                        ".transaction-share"
                    );

                const shares = Array.from(
                    shareInputs
                ).map(input => Number(input.value));

                if (shares.length !== recipients.length) {
                    alert("Please provide a share for every recipient.");
                    return;
                }

                if (shares.some(share => !Number.isFinite(share) || share <= 0)) {
                    alert("Every share must be greater than zero.");
                    return;
                }

                const shareSum = shares.reduce(
                    (sum, share) => sum + share,
                    0
                );

                if (Math.abs(shareSum - 1) > 0.001) {
                    alert("Recipient shares must add up to 100%.");
                    return;
                }

                url = `${API_BASE_URL}/transactions/shared`;

                body = {
                    workspace_id: workspaceId,
                    payer_id: payerMemberId,
                    value: amount,
                    currency: currency,
                    description: description || "",
                    recipients: recipients,
                    shares: shares
                };
            }

            try {
                await createTransaction(type, body);

                newTransactionForm.style.display = "none";

                await initializeTransactionPage();

            } catch (error) {
                console.error(error);

                alert(
                    error.message ||
                    "Failed to create transaction."
                );
            }
        });
    }
});