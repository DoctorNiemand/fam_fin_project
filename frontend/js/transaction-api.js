/* =========================================================
   Family Finance
   Transaction API
   ========================================================= */

async function fetchTransactions(context, includeDeleted = false) {
    let url;

    const deletedParameter =
        includeDeleted ? "&include_deleted=true" : "";

    switch (context.type) {
        case "workspace":
            url =
                `${API_BASE_URL}/transactions/workspace/${context.id}` +
                `?user_id=${CURRENT_USER_ID}` +
                deletedParameter;
            break;

        case "account":
            url =
                `${API_BASE_URL}/transactions/account/${context.id}` +
                `?user_id=${CURRENT_USER_ID}` +
                deletedParameter;
            break;

        case "user":
            url =
                `${API_BASE_URL}/transactions/user/${CURRENT_USER_ID}` +
                (includeDeleted
                    ? "?include_deleted=true"
                    : "");
            break;

        default:
            throw new Error("Unknown transaction context");
    }

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(
            `Failed to load transactions: ${response.status}`
        );
    }

    return await response.json();
}

async function deleteTransaction(transactionId) {
    const response = await fetch(
        `${API_BASE_URL}/transactions/${transactionId}`,
        {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: CURRENT_USER_ID
            })
        }
    );

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        throw new Error(
            errorData.detail ||
            `Failed to delete transaction: ${response.status}`
        );
    }
}

async function restoreTransaction(transactionId) {
    const response = await fetch(
        `${API_BASE_URL}/transactions/${transactionId}/restore`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: CURRENT_USER_ID
            })
        }
    );

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        throw new Error(
            errorData.detail ||
            `Failed to restore transaction: ${response.status}`
        );
    }
}

async function deleteOperation(operationId) {
    const response = await fetch(
        `${API_BASE_URL}/transactions/operation/${operationId}?user_id=${CURRENT_USER_ID}`,
        {
            method: "DELETE"
        }
    );

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || "Failed to delete operation.");
    }

    return response.json();
}

async function restoreOperation(operationId) {
    const response = await fetch(
        `${API_BASE_URL}/transactions/operation/${operationId}/restore?user_id=${CURRENT_USER_ID}`,
        {
            method: "POST"
        }
    );

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || "Failed to restore operation.");
    }

    return response.json();
}

async function updateTransaction(
    transactionId,
    data
) {
    const response = await fetch(
        `${API_BASE_URL}/transactions/${transactionId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: CURRENT_USER_ID,
                ...data
            })
        }
    );

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        throw new Error(
            errorData.detail ||
            `Failed to update transaction: ${response.status}`
        );
    }

    return await response.json().catch(() => null);
}

async function createTransaction(
    type,
    data
) {
    let url;

    switch (type) {
        case "expense":
            url = `${API_BASE_URL}/transactions/expense`;
            break;

        case "direct_transfer":
            url = `${API_BASE_URL}/transactions/transfer`;
            break;

        case "shared_payment":
            url = `${API_BASE_URL}/transactions/shared`;
            break;

        default:
            throw new Error("Unknown transaction type");
    }

    const response = await fetch(
        url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
    );

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        throw new Error(
            errorData.detail ||
            `Failed to create transaction: ${response.status}`
        );
    }

    return await response.json().catch(() => null);
}
