const gameId = localStorage.getItem("game_id");
const playerName = localStorage.getItem("player_name");
const isHost = localStorage.getItem("is_host") === "true";

document.getElementById("game-id").innerText = gameId;

async function loadStatus() {
    const res = await fetch(
        `${BASE_URL}/game/status?game_id=${gameId}`
    );
    const data = await res.json();

    document.getElementById("player-count").innerText =
        data.player_count;

    // HOST LOGIC
    if (isHost) {
        if (data.player_count === 2) {
            document.getElementById("start-btn").style.display = "block";
            document.getElementById("info").innerText =
                "Both players joined. You can start the game.";
        } else {
            document.getElementById("info").innerText =
                "Waiting for second player...";
        }
    }
    // PLAYER 2 LOGIC
    else {
        document.getElementById("info").innerText =
            "Waiting for host to start the game...";
    }

    // 🔥 Redirect everyone when game starts
    if (data.status === "STARTED") {
        window.location.href = "quiz.html";
    }
}

async function startGame() {
    await fetch(
        `${BASE_URL}/game/start?game_id=${gameId}`,
        { method: "POST" }
    );
}

// Poll every 2 seconds
setInterval(loadStatus, 2000);
loadStatus();
