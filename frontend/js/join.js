async function joinGame() {
    const name = document.getElementById("join-name").value;
    const gameId = document.getElementById("join-game-id").value;

    if (!name || !gameId) {
        alert("Enter name and game ID");
        return;
    }

    const res = await fetch(
        `${BASE_URL}/game/join?game_id=${encodeURIComponent(gameId)}&player_name=${encodeURIComponent(name)}`,
        { method: "POST" }
    );

    const data = await res.json();

    if (!res.ok) {
        alert(data.detail || "Unable to join game");
        return;
    }

    localStorage.setItem("game_id", gameId);
    localStorage.setItem("player_name", name);
    localStorage.setItem("is_host", "false");

    window.location.href = "waiting.html";
}
