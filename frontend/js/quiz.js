
const gameId = localStorage.getItem("game_id");
const playerName = localStorage.getItem("player_name");


let currentQuestionIndex = 0;
let socket;

// Initialize UI
document.getElementById("game-id").innerText = gameId;


// CONNECT WEBSOCKET

function connectWebSocket() {
   
    socket = new WebSocket(`ws://localhost:8000/ws/quiz/${gameId}/${playerName}`);

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

      if (data.type === "NEXT_QUESTION") {
    loadQuestion();
}


        if (data.type === "GAME_OVER") {
            showResult(data);
        }
    };

    socket.onclose = () => {
        console.warn("WebSocket disconnected. Attempting to reconnect...");
        
    };

    socket.onerror = (error) => {
        console.error("WebSocket Error: ", error);
    };
}


// LOAD QUESTION

let pollTimer = null;

async function loadQuestion(index = null) {
    if (index !== null) {
        currentQuestionIndex = index;
    }

    try {
        const res = await fetch(`${BASE_URL}/game/question?game_id=${gameId}`);
        const data = await res.json();

        // GAME FINISHED show result and STOP everything
        if (data.status === "FINISHED") {
            clearInterval(pollTimer);
            showResult(data);
            return;
        }

        // Waiting for other player
        if (data.status === "WAITING") {
            document.getElementById("waiting-message").style.display = "block";
            document.getElementById("submit-btn").style.display = "none";

            // Start polling ONLY if not already polling
            if (!pollTimer) {
                pollTimer = setInterval(loadQuestion, 1500);
            }
            return;
        }

        // QUESTION RECEIVED (normal existing flow)
        if (data.status === "QUESTION") {

            // Stop polling once question arrives
            if (pollTimer) {
                clearInterval(pollTimer);
                pollTimer = null;
            }

            // UI State Management 
            document.getElementById("waiting-message").style.display = "none";
            document.getElementById("submit-btn").style.display = "block";

            document.getElementById("question-number").innerText =
                `Question ${data.question_number}`;

            document.getElementById("question-text").innerText = data.question;

            const form = document.getElementById("options-form");
            form.innerHTML = ""; // Clear previous options

            data.options.forEach((opt) => {
                const label = document.createElement("label");
                label.innerHTML = `
                    <input type="radio" name="option" value="${opt}">
                    ${opt}
                `;
                form.appendChild(label);
                form.appendChild(document.createElement("br"));
            });

            return;
        }

        console.warn("Unexpected response:", data);

    } catch (error) {
        console.error("Failed to load question:", error);
    }
}




// SUBMIT ANSWER
async function submitAnswer() {
    const selected = document.querySelector('input[name="option"]:checked');

    if (!selected) {
        alert("Please select an answer!");
        return;
    }

    // Toggle UI to prevent double-submission
    document.getElementById("submit-btn").style.display = "none";
    document.getElementById("waiting-message").style.display = "block";

    const encodedAnswer = encodeURIComponent(selected.value);

    try {
        await fetch(
            `${BASE_URL}/game/answer?game_id=${gameId}&player_name=${playerName}&answer=${encodedAnswer}`,
            { method: "POST" }
        );
    } catch (error) {
        console.error("Error submitting answer:", error);
    }
    // pollTimer = setInterval(loadQuestion, 1500);

}

// SHOW RESULT
function showResult(data) {
    document.getElementById("question-area").style.display = "none";
    document.getElementById("waiting-message").style.display = "none";
    document.getElementById("result-area").style.display = "block";

    document.getElementById("result-message").innerText =
        data.winner === "DRAW" ? "It's a Draw!" : `Winner: ${data.winner}`;

    const you = data.players.find((p) => p.name === playerName);
    const opponent = data.players.find((p) => p.name !== playerName);

    if (you) document.getElementById("your-score").innerText = you.score;
    if (opponent) document.getElementById("opponent-score").innerText = opponent.score;
}

// Execution
connectWebSocket();
loadQuestion(0);