console.log("create.js loaded");

async function createGame() {
    console.log("createGame function called");

    const name = document.getElementById("create-name").value;
    const topic = document.getElementById("topic").value;

    if (!name) {
        alert("Enter your name");
        return;
    }

    const response = await fetch(
        `${BASE_URL}/game/create?player_name=${encodeURIComponent(name)}&topic=${encodeURIComponent(topic)}`,
        { method: "POST" }
    );

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("game_id", data.game_id);
        localStorage.setItem("player_name", name);
        localStorage.setItem("is_host", "true");

        document.getElementById("game-id-display").innerText = data.game_id;
        document.getElementById("create-message").innerText =
            "Game created! Share this Game ID with Player 2.";

        window.location.href = "waiting.html";
    }
}















// async function createGame() {
//     const name = document.getElementById("create-name").value;
//     const topic = document.getElementById("topic").value;

//     if (!name) {
//         alert("Enter your name");
//         return;
//     }

//     // Send data as QUERY PARAMETERS (not JSON body)
//     const response = await fetch(
//         `${BASE_URL}/game/create?player_name=${encodeURIComponent(name)}&topic=${encodeURIComponent(topic)}`,
//         {
//             method: "POST"
//         }
//     );

//     const data = await response.json();

// if (response.ok) {
//     localStorage.setItem("game_id", data.game_id);
//     localStorage.setItem("player_name", name);

//     document.getElementById("game-id-display").innerText = data.game_id;
//     document.getElementById("create-message").innerText =
//         "Game created! Share this Game ID with Player 2.";

//     // Optional: delay redirect
//     // window.location.href = "quiz.html";
// }
//  else {
//         document.getElementById("message").innerText = data.detail || "Error creating game";
//     }
// }
