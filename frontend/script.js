document.addEventListener("DOMContentLoaded", function () {
    let select = document.getElementById("year");
    let currentYear = new Date().getFullYear();

    for (let i = currentYear; i >= 1900; i--) {
        let option = document.createElement("option");
        option.value = i;
        option.textContent = i;
        select.appendChild(option);
    }

    document.getElementById("scrapeButton").addEventListener("click", function () {
        let year = select.value;
        document.getElementById("output").textContent = "Scraping data, please wait...";

        fetch("/scrape", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ year: year })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("output").textContent = data.message;
            let downloadLink = document.createElement("a");
            downloadLink.href = data.download_url;
            downloadLink.textContent = "Download CSV File";
            downloadLink.setAttribute("download", `fda_approvals_${year}.csv`);
            document.getElementById("output").appendChild(document.createElement("br"));
            document.getElementById("output").appendChild(downloadLink);
        })
        .catch(error => {
            document.getElementById("output").textContent = "Error: " + error;
        });
    });
});
