document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       Application Status Updates
       ===================================================== */

    const statusDropdowns =
        document.querySelectorAll(".status-dropdown");


    function updateStatusStyle(dropdown) {

        dropdown.classList.remove(
            "status-applied",
            "status-screening",
            "status-interviewing",
            "status-offer",
            "status-rejected"
        );

        const status = dropdown.value.toLowerCase();

        dropdown.classList.add(
            `status-${status}`
        );
    }


    statusDropdowns.forEach(dropdown => {

        updateStatusStyle(dropdown);


        dropdown.addEventListener("change", async () => {

            const applicationId =
                dropdown.dataset.id;

            const newStatus =
                dropdown.value;


            dropdown.disabled = true;


            try {

                const response = await fetch(
                    `/api/applications/${applicationId}/status`,
                    {
                        method: "PATCH",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            status: newStatus
                        })
                    }
                );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Failed to update status"
                    );

                }


                updateStatusStyle(dropdown);


                console.log(
                    "Status updated:",
                    data
                );


            } catch (error) {

                console.error(
                    "Error updating status:",
                    error
                );


                alert(
                    "Could not update application status."
                );

            } finally {

                dropdown.disabled = false;

            }

        });

    });


    /* =====================================================
       Dashboard Metrics
       ===================================================== */

    async function loadMetrics() {

        const totalApplied =
            document.getElementById("total-applied");

        const interviewRate =
            document.getElementById("interview-rate");

        const totalOffers =
            document.getElementById("total-offers");


        if (
            !totalApplied ||
            !interviewRate ||
            !totalOffers
        ) {
            return;
        }


        try {

            const response =
                await fetch("/api/metrics");


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Failed to load metrics"
                );

            }


            totalApplied.textContent =
                data.total_applied;


            interviewRate.textContent =
                data.interview_rate + "%";


            totalOffers.textContent =
                data.offers;


            totalApplied.classList.remove(
                "loading"
            );

            interviewRate.classList.remove(
                "loading"
            );

            totalOffers.classList.remove(
                "loading"
            );


        } catch (error) {

            console.error(
                "Error loading metrics:",
                error
            );


            totalApplied.textContent =
                "—";

            interviewRate.textContent =
                "—";

            totalOffers.textContent =
                "—";

        }

    }


    loadMetrics();

});