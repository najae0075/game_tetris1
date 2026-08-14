from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Tetris Game", page_icon="🎮", layout="wide")
st.title("🎮 Tetris")
st.caption("브라우저 정적 Tetris를 Streamlit 환경에서 실행합니다.")

HTML = """
<div id="overlay" class="start-overlay visible">
  <div class="overlay-card">
    <h1 id="overlay-title">Tetris</h1>
    <p id="overlay-text">방향키로 이동하고, C로 홀드, Space로 드롭하세요.</p>
    <button id="overlay-start-btn" type="button">Start Game</button>
  </div>
</div>

<div class="tetris-shell">
  <div class="game-panel">
    <canvas id="board" width="300" height="600"></canvas>
  </div>

  <aside class="side-panel">
    <div class="info-box">
      <h2>Score</h2>
      <p id="score">0</p>
    </div>
    <div class="info-box">
      <h2>Best</h2>
      <p id="best-score">0</p>
    </div>
    <div class="info-box">
      <h2>Level</h2>
      <p id="level">1</p>
    </div>
    <div class="info-box">
      <h2>Lines</h2>
      <p id="lines">0</p>
    </div>
    <div class="info-box">
      <h2>Hold</h2>
      <canvas id="hold" width="120" height="120"></canvas>
    </div>
    <div class="info-box">
      <h2>Next</h2>
      <canvas id="next" width="120" height="120"></canvas>
    </div>
    <div class="controls">
      <button id="start-btn" type="button">Start</button>
      <button id="pause-btn" type="button">Pause</button>
      <button id="restart-btn" type="button">Restart</button>
    </div>
    <div class="mobile-controls">
      <button data-action="left">◀</button>
      <button data-action="right">▶</button>
      <button data-action="rotate">⟳</button>
      <button data-action="down">▼</button>
      <button data-action="drop">Drop</button>
      <button data-action="hold">Hold</button>
    </div>
  </aside>
</div>

<style>
  * { box-sizing: border-box; }
  html, body {
    margin: 0;
    min-height: 100%;
    width: 100%;
    background: #020817;
  }
  body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px;
  }
  .tetris-shell {
    width: min(100%, 920px);
    display: flex;
    gap: 18px;
    align-items: flex-start;
    justify-content: center;
    margin: 0 auto;
    padding: 18px;
    background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(17,24,39,0.96));
    border-radius: 18px;
    box-shadow: 0 12px 32px rgba(0,0,0,0.25);
    flex-wrap: wrap;
  }
  .game-panel {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0f172a;
    border: 4px solid #374151;
    border-radius: 10px;
    padding: 0;
    flex: 0 0 auto;
  }
  #board {
    display: block;
    width: min(82vw, 300px);
    height: auto;
    background: #0f172a;
    touch-action: none;
    user-select: none;
  }
  .side-panel {
    display: flex;
    flex-direction: column;
    gap: 12px;
    min-width: 180px;
    width: min(100%, 220px);
    flex: 1 1 180px;
  }
  .info-box {
    background: #111827;
    border: 2px solid #374151;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
  }
  .info-box h2 {
    font-size: 14px;
    margin: 0 0 6px 0;
    color: #cbd5e1;
  }
  .info-box p {
    font-size: 24px;
    font-weight: bold;
    margin: 0;
    color: white;
  }
  #score, #level, #lines {
    transition: transform 0.15s ease, color 0.15s ease;
  }
  #score.score-bump,
  #level.score-bump,
  #lines.score-bump {
    transform: scale(1.15);
    color: #facc15;
  }
  .start-overlay {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: min(420px, 86vw);
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.78);
    border-radius: 18px;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
    z-index: 20;
  }
  .start-overlay.hidden {
    display: none;
  }
  .overlay-card {
    background: rgba(17, 24, 39, 0.95);
    border: 2px solid #374151;
    border-radius: 18px;
    padding: 28px 24px;
    text-align: center;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
  }
  .overlay-card h1 {
    margin-bottom: 12px;
    font-size: 42px;
    letter-spacing: 2px;
  }
  .overlay-card p {
    margin-bottom: 18px;
    color: #cbd5e1;
    line-height: 1.5;
  }
  #hold, #next {
    display: block;
    margin: 0 auto;
    background: #0f172a;
    border: 2px solid #374151;
    border-radius: 8px;
  }
  .controls {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  button {
    padding: 10px 14px;
    border: none;
    border-radius: 8px;
    background: #2563eb;
    color: white;
    font-weight: bold;
    cursor: pointer;
  }
  button:hover { background: #1d4ed8; }
  .mobile-controls {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
    margin-top: 8px;
    padding: 10px;
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(148, 163, 184, 0.28);
  }
  .mobile-controls button {
    min-height: 52px;
    padding: 10px 8px;
    font-size: 15px;
    font-weight: 800;
    border-radius: 12px;
    box-shadow: inset 0 -2px 0 rgba(0, 0, 0, 0.2);
    touch-action: manipulation;
  }

  @media (max-width: 760px) {
    body {
      padding: 8px;
      align-items: flex-start;
    }

    .tetris-shell {
      width: min(100%, 520px);
      padding: 12px;
      gap: 12px;
    }

    .game-panel {
      width: 100%;
    }

    #board {
      width: min(88vw, 320px);
    }

    .side-panel {
      width: min(100%, 420px);
    }

    .controls {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
    }

    .controls button {
      width: 100%;
    }
  }

  @media (max-width: 480px) {
    .tetris-shell {
      padding: 10px;
    }

    .info-box p {
      font-size: 20px;
    }

    .mobile-controls {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .mobile-controls button[data-action="space"] {
      grid-column: span 2;
    }
  }
</style>

<script>
  const COLS = 10;
  const ROWS = 20;
  const BLOCK = 30;
  const BASE_DROP_INTERVAL = 700;
  const MIN_DROP_INTERVAL = 120;
  const SCORE_TABLE = { 1: 100, 2: 300, 3: 500, 4: 800 };
  const COLORS = {
    I: '#38bdf8',
    O: '#facc15',
    T: '#a78bfa',
    S: '#4ade80',
    Z: '#f87171',
    J: '#60a5fa',
    L: '#fb923c'
  };

  const SHAPES = {
    I: [[1, 1, 1, 1]],
    O: [[1, 1], [1, 1]],
    T: [[0, 1, 0], [1, 1, 1]],
    S: [[0, 1, 1], [1, 1, 0]],
    Z: [[1, 1, 0], [0, 1, 1]],
    J: [[1, 0, 0], [1, 1, 1]],
    L: [[0, 0, 1], [1, 1, 1]]
  };

  const boardCanvas = document.getElementById('board');
  const boardCtx = boardCanvas.getContext('2d', { alpha: false });
  const nextCanvas = document.getElementById('next');
  const nextCtx = nextCanvas.getContext('2d', { alpha: false });
  const holdCanvas = document.getElementById('hold');
  const holdCtx = holdCanvas.getContext('2d', { alpha: false });

  const scoreEl = document.getElementById('score');
  const bestEl = document.getElementById('best-score');
  const levelEl = document.getElementById('level');
  const linesEl = document.getElementById('lines');
  const overlay = document.getElementById('overlay');
  const overlayTitle = document.getElementById('overlay-title');
  const overlayText = document.getElementById('overlay-text');
  const overlayStartBtn = document.getElementById('overlay-start-btn');

  function bumpValue(element) {
    element.classList.remove('score-bump');
    void element.offsetWidth;
    element.classList.add('score-bump');
    setTimeout(() => element.classList.remove('score-bump'), 170);
  }

  function showOverlay(title, text, buttonLabel = 'Start Game') {
    overlayTitle.textContent = title;
    overlayText.innerHTML = String(text).replace(/\n/g, '<br>');
    overlayStartBtn.textContent = buttonLabel;
    overlay.classList.remove('hidden');
  }

  function hideOverlay() {
    overlay.classList.add('hidden');
  }

  function ensureAudio() {
    if (!window.__tetrisAudio) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        window.__tetrisAudio = new AudioCtx();
      }
    }
    if (window.__tetrisAudio && window.__tetrisAudio.state === 'suspended') {
      window.__tetrisAudio.resume();
    }
  }

  function playTone(frequency, duration = 0.08, type = 'square', volume = 0.04) {
    const audioCtx = window.__tetrisAudio;
    if (!audioCtx) return;
    const oscillator = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    oscillator.type = type;
    oscillator.frequency.value = frequency;
    gain.gain.value = volume;
    gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);

    oscillator.connect(gain);
    gain.connect(audioCtx.destination);
    oscillator.start();
    oscillator.stop(audioCtx.currentTime + duration);
  }

  function createBoard() {
    return Array.from({ length: ROWS }, () => Array(COLS).fill(null));
  }

  function randomType() {
    const types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];
    return types[Math.floor(Math.random() * types.length)];
  }

  function createPiece(type) {
    const matrix = SHAPES[type].map(row => [...row]);
    return { type, matrix, x: 0, y: 0, color: COLORS[type] };
  }

  function rotateMatrix(matrix) {
    const rows = matrix.length;
    const cols = matrix[0].length;
    const rotated = Array.from({ length: cols }, () => Array(rows).fill(0));
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) {
        rotated[x][rows - 1 - y] = matrix[y][x];
      }
    }
    return rotated;
  }

  function collide(board, piece, offsetX = 0, offsetY = 0) {
    for (let y = 0; y < piece.matrix.length; y++) {
      for (let x = 0; x < piece.matrix[y].length; x++) {
        if (!piece.matrix[y][x]) continue;
        const newX = piece.x + x + offsetX;
        const newY = piece.y + y + offsetY;
        if (newX < 0 || newX >= COLS || newY >= ROWS) return true;
        if (newY >= 0 && board[newY][newX]) return true;
      }
    }
    return false;
  }

  function mergePiece(board, piece) {
    piece.matrix.forEach((row, y) => {
      row.forEach((value, x) => {
        if (value) {
          const boardY = piece.y + y;
          const boardX = piece.x + x;
          if (boardY >= 0 && boardY < ROWS && boardX >= 0 && boardX < COLS) {
            board[boardY][boardX] = piece.type;
          }
        }
      });
    });
  }

  function clearLines(board) {
    let cleared = 0;
    for (let y = ROWS - 1; y >= 0; y--) {
      if (board[y].every(Boolean)) {
        board.splice(y, 1);
        board.unshift(Array(COLS).fill(null));
        cleared += 1;
        y += 1;
      }
    }
    return cleared;
  }

  function readBestScore() {
    try {
      return Number(window.localStorage.getItem('tetris-best-score') || 0);
    } catch (error) {
      return 0;
    }
  }

  function saveBestScore(value) {
    try {
      window.localStorage.setItem('tetris-best-score', String(value));
    } catch (error) {
      // ignore storage restrictions in sandboxed iframe contexts
    }
  }

  let board = createBoard();
  let currentPiece = null;
  let nextPiece = null;
  let holdPiece = null;
  let canHold = true;
  let score = 0;
  let bestScore = readBestScore();
  let lines = 0;
  let level = 1;
  let dropInterval = BASE_DROP_INTERVAL;
  let gameOver = false;
  let paused = false;
  let gameStarted = false;
  let dropAccumulator = 0;
  let lastTime = 0;

  function updateHud() {
    const previousScore = Number(scoreEl.textContent || 0);
    const previousLevel = Number(levelEl.textContent || 1);
    const previousLines = Number(linesEl.textContent || 0);

    scoreEl.textContent = String(score);
    bestEl.textContent = String(bestScore);
    levelEl.textContent = String(level);
    linesEl.textContent = String(lines);

    if (score !== previousScore) bumpValue(scoreEl);
    if (level !== previousLevel) bumpValue(levelEl);
    if (lines !== previousLines) bumpValue(linesEl);
  }

  function drawCell(ctx, x, y, color, size = BLOCK) {
    ctx.fillStyle = color;
    ctx.fillRect(x * size, y * size, size, size);
    ctx.strokeStyle = '#1f2937';
    ctx.strokeRect(x * size, y * size, size, size);
  }

  function drawGrid(ctx, canvas) {
    ctx.strokeStyle = 'rgba(148,163,184,0.18)';
    ctx.lineWidth = 1;
    for (let y = 0; y <= ROWS; y++) {
      ctx.beginPath();
      ctx.moveTo(0, y * BLOCK);
      ctx.lineTo(canvas.width, y * BLOCK);
      ctx.stroke();
    }
    for (let x = 0; x <= COLS; x++) {
      ctx.beginPath();
      ctx.moveTo(x * BLOCK, 0);
      ctx.lineTo(x * BLOCK, canvas.height);
      ctx.stroke();
    }
  }

  function drawGhost() {
    if (!currentPiece) return;
    const ghost = { ...currentPiece, matrix: currentPiece.matrix.map(row => [...row]) };
    while (!collide(board, ghost, 0, 1)) {
      ghost.y += 1;
    }
    ghost.matrix.forEach((row, y) => {
      row.forEach((value, x) => {
        if (value) {
          boardCtx.fillStyle = 'rgba(255,255,255,0.18)';
          boardCtx.fillRect((ghost.x + x) * BLOCK, (ghost.y + y) * BLOCK, BLOCK, BLOCK);
        }
      });
    });
  }

  function drawBoard() {
    boardCtx.clearRect(0, 0, boardCanvas.width, boardCanvas.height);
    drawGrid(boardCtx, boardCanvas);

    board.forEach((row, y) => {
      row.forEach((cell, x) => {
        if (cell) drawCell(boardCtx, x, y, COLORS[cell]);
      });
    });

    drawGhost();

    if (currentPiece) {
      currentPiece.matrix.forEach((row, y) => {
        row.forEach((value, x) => {
          if (value) drawCell(boardCtx, currentPiece.x + x, currentPiece.y + y, currentPiece.color);
        });
      });
    }

    if (gameOver) {
      boardCtx.fillStyle = 'rgba(15, 23, 42, 0.72)';
      boardCtx.fillRect(0, 220, boardCanvas.width, 120);
      boardCtx.fillStyle = '#f8fafc';
      boardCtx.font = 'bold 30px Arial';
      boardCtx.textAlign = 'center';
      boardCtx.fillText('Game Over', boardCanvas.width / 2, 285);
    }

    if (paused && !gameOver) {
      boardCtx.fillStyle = 'rgba(15, 23, 42, 0.72)';
      boardCtx.fillRect(0, 220, boardCanvas.width, 120);
      boardCtx.fillStyle = '#f8fafc';
      boardCtx.font = 'bold 30px Arial';
      boardCtx.textAlign = 'center';
      boardCtx.fillText('Paused', boardCanvas.width / 2, 285);
    }
  }

  function drawPreview(context, piece, canvas) {
    context.clearRect(0, 0, canvas.width, canvas.height);
    if (!piece) return;

    const matrix = piece.matrix;
    const offsetX = Math.floor((4 - matrix[0].length) / 2);
    const offsetY = Math.floor((4 - matrix.length) / 2);
    const color = COLORS[piece.type];

    matrix.forEach((row, y) => {
      row.forEach((value, x) => {
        if (!value) return;
        const px = (x + offsetX) * 20;
        const py = (y + offsetY) * 20;
        context.fillStyle = color;
        context.fillRect(px, py, 20, 20);
        context.strokeStyle = '#1f2937';
        context.strokeRect(px, py, 20, 20);
      });
    });
  }

  function drawEverything() {
    drawBoard();
    drawPreview(nextCtx, nextPiece, nextCanvas);
    if (holdPiece) {
      drawPreview(holdCtx, { ...createPiece(holdPiece), matrix: SHAPES[holdPiece].map(row => [...row]) }, holdCanvas);
    } else {
      holdCtx.clearRect(0, 0, holdCanvas.width, holdCanvas.height);
    }
    updateHud();
  }

  function spawnNextPiece() {
    currentPiece = nextPiece || createPiece(randomType());
    currentPiece.x = Math.floor(COLS / 2) - Math.ceil(currentPiece.matrix[0].length / 2);
    currentPiece.y = 0;
    nextPiece = createPiece(randomType());
    if (collide(board, currentPiece)) {
      gameOver = true;
      bestScore = Math.max(bestScore, score);
      saveBestScore(bestScore);
      updateHud();
    }
  }

  function movePiece(dx, dy) {
    if (!currentPiece || gameOver || paused) return false;
    currentPiece.x += dx;
    currentPiece.y += dy;
    if (collide(board, currentPiece)) {
      currentPiece.x -= dx;
      currentPiece.y -= dy;
      if (dy > 0) {
        mergePiece(board, currentPiece);
        const cleared = clearLines(board);
        if (cleared > 0) {
          lines += cleared;
          score += (SCORE_TABLE[cleared] || 0) * level;
          level = Math.floor(lines / 10) + 1;
          dropInterval = Math.max(MIN_DROP_INTERVAL, BASE_DROP_INTERVAL - (level - 1) * 60);
        }
        canHold = true;
        spawnNextPiece();
      }
      return false;
    }
    return true;
  }

  function rotateCurrent() {
    if (!currentPiece || gameOver || paused) return;
    const rotated = rotateMatrix(currentPiece.matrix);
    const oldMatrix = currentPiece.matrix;
    currentPiece.matrix = rotated;
    if (collide(board, currentPiece)) {
      currentPiece.matrix = oldMatrix;
    }
  }

  function holdCurrent() {
    if (!currentPiece || gameOver || paused || !canHold) return;
    if (!holdPiece) {
      holdPiece = currentPiece.type;
      spawnNextPiece();
    } else {
      const swapped = holdPiece;
      holdPiece = currentPiece.type;
      currentPiece = createPiece(swapped);
      currentPiece.x = Math.floor(COLS / 2) - Math.ceil(currentPiece.matrix[0].length / 2);
      currentPiece.y = 0;
      if (collide(board, currentPiece)) {
        gameOver = true;
      }
    }
    canHold = false;
  }

  function hardDrop() {
    if (!currentPiece || gameOver || paused) return;
    let distance = 0;
    while (!gameOver) {
      const moved = movePiece(0, 1);
      if (!moved) break;
      distance += 1;
    }
    if (distance > 0) {
      score += distance * 2;
      bestScore = Math.max(bestScore, score);
      saveBestScore(bestScore);
    }
    updateHud();
  }

  function startGame() {
    ensureAudio();
    board = createBoard();
    currentPiece = createPiece(randomType());
    nextPiece = createPiece(randomType());
    holdPiece = null;
    canHold = true;
    score = 0;
    lines = 0;
    level = 1;
    dropInterval = BASE_DROP_INTERVAL;
    gameOver = false;
    paused = false;
    gameStarted = true;
    dropAccumulator = 0;
    lastTime = 0;
    currentPiece.x = Math.floor(COLS / 2) - Math.ceil(currentPiece.matrix[0].length / 2);
    currentPiece.y = 0;
    hideOverlay();
    updateHud();
    drawEverything();
  }

  function togglePause() {
    if (!gameStarted || gameOver) return;
    paused = !paused;
    if (paused) {
      showOverlay('Paused', '계속하려면 다시 눌러주세요.', 'Resume');
    } else {
      hideOverlay();
    }
    drawEverything();
  }

  function loop(timestamp) {
    const delta = timestamp - (lastTime || timestamp);
    lastTime = timestamp;
    if (gameStarted && !paused && !gameOver) {
      dropAccumulator += delta;
      if (dropAccumulator >= dropInterval) {
        dropAccumulator = 0;
        movePiece(0, 1);
      }
    }
    drawEverything();
    requestAnimationFrame(loop);
  }

  function bindControls() {
    window.startGame = startGame;
    window.togglePause = togglePause;
    window.dispatchTetrisStart = () => {
      if (paused) {
        togglePause();
        return;
      }
      startGame();
    };
    window.dispatchTetrisPause = togglePause;

    const startButton = document.getElementById('start-btn');
    const restartButton = document.getElementById('restart-btn');
    const pauseButton = document.getElementById('pause-btn');

    const triggerStart = () => {
      if (paused) {
        togglePause();
        return;
      }
      startGame();
    };

    const bindClick = (element, handler) => {
      if (!element) return;
      element.onclick = (event) => {
        event.preventDefault();
        event.stopPropagation();
        handler();
      };
      element.addEventListener('touchstart', (event) => {
        event.preventDefault();
        event.stopPropagation();
        handler();
      }, { passive: false });
    };

    bindClick(startButton, startGame);
    bindClick(restartButton, startGame);
    bindClick(pauseButton, togglePause);
    bindClick(overlayStartBtn, triggerStart);

    document.addEventListener('click', (event) => {
      const target = event.target;
      if (!target || !document.getElementById('overlay')) return;
      if (!overlay.classList.contains('hidden')) {
        const clickedOverlayButton = target.closest && target.closest('#overlay-start-btn');
        if (clickedOverlayButton) {
          event.preventDefault();
          event.stopPropagation();
          triggerStart();
        }
      }
    }, true);

    document.querySelectorAll('[data-action]').forEach((button) => {
      button.onclick = () => {
        ensureAudio();
        const action = button.dataset.action;
        if (action === 'left') {
          movePiece(-1, 0); playTone(220, 0.05, 'square', 0.025);
        }
        if (action === 'right') {
          movePiece(1, 0); playTone(300, 0.05, 'square', 0.025);
        }
        if (action === 'down') {
          movePiece(0, 1); score += 1; playTone(180, 0.04, 'square', 0.02);
        }
        if (action === 'rotate') {
          rotateCurrent(); playTone(400, 0.06, 'triangle', 0.03);
        }
        if (action === 'drop') {
          hardDrop(); playTone(520, 0.08, 'sawtooth', 0.04);
        }
        if (action === 'hold') {
          holdCurrent(); playTone(600, 0.08, 'triangle', 0.04);
        }
      };
    });

    document.onkeydown = (event) => {
      if (event.key === 'ArrowLeft') { movePiece(-1, 0); playTone(220, 0.05, 'square', 0.025); }
      if (event.key === 'ArrowRight') { movePiece(1, 0); playTone(300, 0.05, 'square', 0.025); }
      if (event.key === 'ArrowDown') { movePiece(0, 1); score += 1; playTone(180, 0.04, 'square', 0.02); }
      if (event.key === 'ArrowUp' || event.key.toLowerCase() === 'x') { rotateCurrent(); playTone(400, 0.06, 'triangle', 0.03); }
      if (event.key === ' ') {
        event.preventDefault();
        hardDrop();
        playTone(520, 0.08, 'sawtooth', 0.04);
      }
      if (event.key.toLowerCase() === 'c') { holdCurrent(); playTone(600, 0.08, 'triangle', 0.04); }
      if (event.key.toLowerCase() === 'p') togglePause();
    };
  }

  bestScore = readBestScore();
  showOverlay('Tetris', '방향키로 이동하고, C로 홀드, Space로 드롭하세요.', 'Start Game');
  updateHud();
  bindControls();
  requestAnimationFrame(loop);
</script>
"""

html = (Path(__file__).resolve().parent / "game.html").read_text(encoding="utf-8")
components.html(html, height=820, scrolling=False)
