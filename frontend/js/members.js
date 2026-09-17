/* =========================================================
   Family Finance
   Workspace members
   ========================================================= */


async function loadWorkspaceMembers() {
    const membersList =
        document.getElementById("workspace-members");

    if (!membersList) {
        return;
    }

    const workspaceId = getWorkspaceId();

    if (!workspaceId) {
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/workspaces/${workspaceId}/members?user_id=${CURRENT_USER_ID}`
        );

        if (!response.ok) {
            throw new Error(
                `Failed to load members: ${response.status}`
            );
        }

        const members = await response.json();

        membersList.innerHTML = "";

        members
            .filter(member => member.active)
            .forEach(member => {

                const row =
                    document.createElement("div");

                row.className = "member-row";

                row.innerHTML = `
                    <div class="member-info">
                        <span class="member-name">
                            ${member.name}
                        </span>

                        <span class="permission-badge">
                            ${member.permission}
                        </span>
                    </div>
                `;

                membersList.appendChild(row);
            });

    } catch (error) {

        console.error(error);

        membersList.innerHTML = `
            <div class="member-row">
                Failed to load members.
            </div>
        `;
    }
}


document.addEventListener(
    "DOMContentLoaded",
    loadWorkspaceMembers
);