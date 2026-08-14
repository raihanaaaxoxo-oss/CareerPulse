document.addEventListener("DOMContentLoaded", () => {

    const statusDropdowns = document.querySelectorAll(".status-dropdown");

    statusDropdowns.forEach(dropdown => {

        dropdown.addEventListener("change", async () => {

            const applicationId = dropdown.dataset.id;
            const newStatus = dropdown.value;

            try {
                const response = await fetch(`/api/applications/${applicationId}/status`, {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        status: newStatus
                    })
                });

                let data;

                try {
                    data = await response.json();
                } catch {
                    throw new Error("Server returned an invalid response.");
                }

                if (!response.ok) {
                    throw new Error(data.error || "Failed to update status");
                }

                console.log("Status updated:", data);

            } catch (error) {
                console.error("Error updating status:", error);
                alert("Could not update application status.");
            }

        });

    });

});


async function loadMetrics() {

    try {

        const response = await fetch("/api/metrics");

        if (!response.ok) {
            throw new Error("Failed to load dashboard metrics.");
        }

        const data = await response.json();

        document.getElementById("total-applied").textContent = data.total_applied;
        document.getElementById("interview-rate").textContent = data.interview_rate + "%";
        document.getElementById("total-offers").textContent = data.offers;

    } catch (error) {

        console.error("Error loading metrics:", error);

        const totalApplied = document.getElementById("total-applied");
        const interviewRate = document.getElementById("interview-rate");
        const totalOffers = document.getElementById("total-offers");

        if (totalApplied) {
            totalApplied.textContent = "Unavailable";
        }

        if (interviewRate) {
            interviewRate.textContent = "Unavailable";
        }

        if (totalOffers) {
            totalOffers.textContent = "Unavailable";
        }
    }
}


document.addEventListener("DOMContentLoaded", loadMetrics);