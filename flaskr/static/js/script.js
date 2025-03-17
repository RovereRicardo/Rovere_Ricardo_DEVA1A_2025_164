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

function submitScore(button) {
    let form = document.getElementById("submitScoreForm");

    let row = button.closest("tr");
    let table = button.closest("table");

    let matchId = row.getAttribute("data-match-id");
    let teamId = table.getAttribute("data-team-id");

    form.elements["homeScore"].value = button.value;
    let total = button.value;


    let formData = new FormData(form);

    fetch('/view_match_table_ajax?id_match={{ match.id_match }}', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            console.log(data);
            document.getElementById('totaldata-' + total).innerHTML = data;

        })
        .catch(error => console.error('Error:', error));
}
