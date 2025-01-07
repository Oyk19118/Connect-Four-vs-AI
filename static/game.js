const canvas = document.getElementById("connect4");
const ctx = canvas.getContext("2d");

const ROWS = 6;
const COLS = 7;
const CELL_SIZE = 100;

let grid = Array.from({ length: ROWS }, () => Array(COLS).fill(null));
let gameOver = false;

function drawGrid() {
    ctx.fillStyle = "blue";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            ctx.beginPath();
            ctx.arc(
                col * CELL_SIZE + CELL_SIZE / 2,
                row * CELL_SIZE + CELL_SIZE / 2,
                CELL_SIZE / 2 - 10,
                0,
                Math.PI * 2
            );
            ctx.fillStyle = grid[row][col] || "white"; // Default color for empty cells
            ctx.fill();
        }
    }
}

function placePiece(col, color) {
    if (col < 0 || col >= COLS) return null; // Ensure column is within bounds
    for (let row = ROWS - 1; row >= 0; row--) {
        if (!grid[row][col]) {
            grid[row][col] = color; // Set the cell to the current player's color
            drawGrid(); // Redraw the board
            return row;
        }
    }
    return null;
}

function showRestartButton() {
    const restartButton = document.createElement("button");
    restartButton.innerText = "Restart Game";
    restartButton.style.position = "absolute";
    restartButton.style.top = "50%";
    restartButton.style.left = "50%";
    restartButton.style.transform = "translate(-50%, -50%)";
    restartButton.style.padding = "15px 30px";
    restartButton.style.fontSize = "18px";
    restartButton.style.cursor = "pointer";
    document.body.appendChild(restartButton);

    restartButton.addEventListener("click", () => {
        fetch("/reset", { method: "POST" }) // Send reset signal to the server
            .then(() => {
                grid = Array.from({ length: ROWS }, () => Array(COLS).fill(null)); // Clear frontend grid
                gameOver = false;
                drawGrid(); // Redraw empty grid
                restartButton.remove(); // Remove the restart button
            });
    });
}

canvas.addEventListener("click", (e) => {
    if (gameOver) return;

    const col = Math.floor(e.offsetX / CELL_SIZE);

    // Ignore clicks outside the grid area
    if (col < 0 || col >= COLS) return;

    fetch("/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ player_col: col }),
    })
        .then((response) => response.json())
        .then((data) => {
            placePiece(col, "red"); // Place player's piece

            if (data.winner) {
                gameOver = true;
                alert(`${data.winner} wins!`);
                showRestartButton();
                return;
            }

            // Place AI's piece immediately
            if (data.ai_col !== null) {
                placePiece(data.ai_col, "yellow"); // Place AI's piece

                if (data.winner) {
                    gameOver = true;
                    alert(`${data.winner} wins!`);
                    showRestartButton();
                }
            }
        });
});

drawGrid();