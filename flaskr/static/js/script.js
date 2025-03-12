function registerStats(button) {
    let form = document.getElementById("statSenderForm");

    // Find the player's row
    let row = button.closest("tr");
    let table = button.closest("table");

    // Get the player's ID
    let playerId = row.getAttribute("data-player-id");
    let teamId = table.getAttribute("data-team-id");
    // Populate form fields

    form.elements["idPlayer"].value = playerId;
    form.elements["idTeam"].value = teamId;
    form.elements["statType"].value = button.name;
    form.elements["statValue"].value = button.value;

    let formData = new FormData(form);

    fetch('/view_match_table_ajax?id_match={{ match.id_match }}', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            console.log('teamdata-table-' + teamId)
            document.getElementById('teamdata-table-' + teamId).innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("submitScoreButton").addEventListener("click", function () {
        submitScore(this);
    });
});

function submitScore(button) {
    let form = document.getElementById("submitScoreForm");

    // Find the table that the button belongs to
    let row = button.closest("tr");
    let table = row.closest("table");
    let matchId = table.getAttribute("data-team-id");

    // Find the cell with the total points by ID
    let cell = table.querySelector("#totalPoints");

    if (cell) {
        let totalPoints = cell.textContent.trim();
        form.elements['homeTeamScore'].value = totalPoints;
    } else {
        console.error("Total points cell not found");
        return;
    }

    let formData = new FormData(form);

    fetch('/view_match_table_ajax?id_match={{ match.id_match }}', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            console.log('scoredata-table-' + matchId);
            document.getElementById('scoredata-table-' + matchId).innerHTML = data;
        })
        .catch(error => console.error('Error:', error));

    console.log(matchId);
}