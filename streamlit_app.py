import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Snake Game",
    page_icon="🐍",
    layout="centered"
)

st.markdown(
    """
    <style>
        .main {
            text-align: center;
        }

        h1 {
            text-align: center;
        }

        .game-info {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🐍 Snake Game")

st.markdown(
    '<div class="game-info">Use Arrow Keys or WASD to move the snake</div>',
    unsafe_allow_html=True
)

game_html = """
<!DOCTYPE html>
<html>
<head>

<style>

body {
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: Arial, sans-serif;
    text-align: center;
}

#gameContainer {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

canvas {
    border: 4px solid #222;
    background-color: #111;
    border-radius: 10px;
}

#score {
    font-size: 22px;
    font-weight: bold;
    margin: 10px;
}

#message {
    font-size: 20px;
    font-weight: bold;
    margin: 10px;
}

button {
    padding: 10px 25px;
    font-size: 17px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    background-color: #2196F3;
    color: white;
}

button:hover {
    background-color: #1976D2;
}

</style>

</head>

<body>

<div id="gameContainer">

<div id="score">
    Score: <span id="scoreValue">0</span>
</div>

<canvas id="gameCanvas" width="500" height="500"></canvas>

<div id="message">
    Press Arrow Keys or WASD to start
</div>

<button onclick="restartGame()">🔄 Restart Game</button>

</div>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const gridSize = 25;
const tileCount = canvas.width / gridSize;

let snake;
let food;

let dx;
let dy;

let score;
let gameRunning;
let gameOver;

let gameSpeed = 100;

function initializeGame() {

    snake = [
        {x: 10, y: 10},
        {x: 9, y: 10},
        {x: 8, y: 10}
    ];

    food = {
        x: Math.floor(Math.random() * tileCount),
        y: Math.floor(Math.random() * tileCount)
    };

    dx = 0;
    dy = 0;

    score = 0;

    gameRunning = false;
    gameOver = false;

    document.getElementById("scoreValue").innerText = score;

    document.getElementById("message").innerText =
        "Press Arrow Keys or WASD to start";

    drawGame();
}

function drawGame() {

    ctx.fillStyle = "#111";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw grid

    ctx.strokeStyle = "#222";

    for (let x = 0; x <= canvas.width; x += gridSize) {

        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();

    }

    for (let y = 0; y <= canvas.height; y += gridSize) {

        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();

    }

    // Draw food

    ctx.fillStyle = "red";

    ctx.beginPath();

    ctx.arc(
        food.x * gridSize + gridSize / 2,
        food.y * gridSize + gridSize / 2,
        gridSize / 2 - 3,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // Draw snake

    snake.forEach((segment, index) => {

        if (index === 0) {
            ctx.fillStyle = "#00FF00";
        } else {
            ctx.fillStyle = "#32CD32";
        }

        ctx.fillRect(
            segment.x * gridSize + 2,
            segment.y * gridSize + 2,
            gridSize - 4,
            gridSize - 4
        );

    });

}

function moveSnake() {

    if (!gameRunning || gameOver) {
        return;
    }

    const head = {
        x: snake[0].x + dx,
        y: snake[0].y + dy
    };

    // Wall collision

    if (
        head.x < 0 ||
        head.x >= tileCount ||
        head.y < 0 ||
        head.y >= tileCount
    ) {

        endGame();
        return;
    }

    // Snake collision

    for (let i = 0; i < snake.length; i++) {

        if (
            head.x === snake[i].x &&
            head.y === snake[i].y
        ) {

            endGame();
            return;
        }
    }

    snake.unshift(head);

    // Food collision

    if (
        head.x === food.x &&
        head.y === food.y
    ) {

        score += 10;

        document.getElementById("scoreValue").innerText = score;

        generateFood();

    } else {

        snake.pop();

    }

    drawGame();
}

function generateFood() {

    let validPosition = false;

    while (!validPosition) {

        food.x = Math.floor(Math.random() * tileCount);
        food.y = Math.floor(Math.random() * tileCount);

        validPosition = true;

        for (let segment of snake) {

            if (
                segment.x === food.x &&
                segment.y === food.y
            ) {

                validPosition = false;
                break;

            }

        }
    }
}

function endGame() {

    gameRunning = false;
    gameOver = true;

    document.getElementById("message").innerText =
        "💥 Game Over! Your Score: " + score;

    drawGame();
}

function restartGame() {

    initializeGame();

}

function changeDirection(newDx, newDy) {

    // Prevent snake from moving directly backwards

    if (dx === -newDx && dy === -newDy) {
        return;
    }

    dx = newDx;
    dy = newDy;

    gameRunning = true;

    document.getElementById("message").innerText =
        "Game Running 🐍";
}

document.addEventListener("keydown", function(event) {

    const key = event.key.toLowerCase();

    if (key === "arrowup" || key === "w") {

        changeDirection(0, -1);

    }

    else if (key === "arrowdown" || key === "s") {

        changeDirection(0, 1);

    }

    else if (key === "arrowleft" || key === "a") {

        changeDirection(-1, 0);

    }

    else if (key === "arrowright" || key === "d") {

        changeDirection(1, 0);

    }

});

initializeGame();

setInterval(moveSnake, gameSpeed);

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=650,
    scrolling=False
)

st.markdown("---")

st.markdown(
    """
    ### 🎮 Controls

    | Key | Movement |
    |---|---|
    | ⬆️ / W | Up |
    | ⬇️ / S | Down |
    | ⬅️ / A | Left |
    | ➡️ / D | Right |

    **🍎 Red = Food**  
    **🐍 Green = Snake**  
    **💥 Hit the wall or yourself = Game Over**
    """
)
