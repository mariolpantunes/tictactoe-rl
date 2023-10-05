const statusDisplay = document.querySelector('.game--status');

let gameActive = true;
let currentPlayer = "X";
let gameState = ["", "", "", "", "", "", "", "", ""];

const winningMessage = () => `Player ${currentPlayer} has won!`;
const drawMessage = () => `Game ended in a draw!`;
const currentPlayerTurn = () => `It's ${currentPlayer}'s turn`;

let previousBotCell = null;

statusDisplay.innerHTML = currentPlayerTurn();

const winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

function handleCellPlayed(clickedCell, clickedCellIndex) {
    gameState[clickedCellIndex] = currentPlayer;
    clickedCell.innerHTML = currentPlayer;
    clickedCell.style.color = '';
}

function handlePlayerChange() {
    currentPlayer = currentPlayer === "X" ? "O" : "X";
    statusDisplay.innerHTML = currentPlayerTurn();
}

function handleResultValidation() {
    let roundWon = false;
    for (let i = 0; i <= 7; i++) {
        const winCondition = winningConditions[i];
        let a = gameState[winCondition[0]];
        let b = gameState[winCondition[1]];
        let c = gameState[winCondition[2]];
        if (a === '' || b === '' || c === '') {
            continue;
        }
        if (a === b && b === c) {
            roundWon = true;
            break
        }
    }

    if (roundWon) {
        statusDisplay.innerHTML = winningMessage();
        gameActive = false; 
        return true;
    }

    let roundDraw = !gameState.includes("");
    if (roundDraw) {
        statusDisplay.innerHTML = drawMessage();
        gameActive = false;
        return true;
    }

    handlePlayerChange();
    return false;
}

function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function requestBotPlay(index) {
    //let row =  Math.trunc(index / 3),col = index % 3;

    // code the board into a an array
    let board = []
    let boardFull = true;
    for(let i = 0; i < 9; i++) {
        if(gameState[i] == "X") {
            board.push(1);
        } else if(gameState[i] == "O") {
            board.push(-1);
        } else {
            board.push(0);
            boardFull = false;
        }
    }

    if(boardFull) {
        return -1
    } else {
        //console.log('Board = '+board);
        let url_parameters=''
        for (const b of board) {
            url_parameters += 'board='+b+'&'
        }
        url_parameters += 'player=-1'
        
        //console.log('url parameters = '+url_parameters)

        //console.log(row+' '+col);
        let response = JSON.parse(httpGet('play?'+url_parameters)); //board='+row+'&col='+col));
        
        // OPTIONAL -- get the neural network
        if (response.hasOwnProperty('neural_network') && document.getElementById('canvas_network')) {
            console.log(response['neural_network']);
            requestAnimationFrame(function() {
                draw_network(response['neural_network'].networkLayer, response['neural_network'].activations);
            });
        }
        
        let clickedCellIndex = response['row'] * 3 + response['col'];
        //console.log(clickedCellIndex);
        return clickedCellIndex;
    }   
}

function handleBotPlay(index) {
    console.log('Handle bot play...')
    let clickedCellIndex = requestBotPlay(index);
    let clickedCell = document.getElementById(clickedCellIndex);
    console.log(clickedCell);
    handleCellPlayed(clickedCell, clickedCellIndex)
}

function handleCellClick(clickedCellEvent) {
    previousBotCell=null;
    const clickedCell = clickedCellEvent.target;
    const clickedCellIndex = parseInt(clickedCell.getAttribute('data-cell-index'));

    if (gameState[clickedCellIndex] !== "" || !gameActive) {
        return;
    }

    handleCellPlayed(clickedCell, clickedCellIndex);
    let done = handleResultValidation();
    if (!done) {
        handleBotPlay(clickedCellIndex);
        handleResultValidation();
    }
}

function handleRestartGame() {
    gameActive = true;
    currentPlayer = "X";
    gameState = ["", "", "", "", "", "", "", "", ""];
    statusDisplay.innerHTML = currentPlayerTurn();
    document.querySelectorAll('.cell').forEach(cell => cell.innerHTML = "");
}

function handleCellIn(clickedCellEvent) {
    const clickedCell = clickedCellEvent.target;
    const clickedCellIndex = parseInt(clickedCell.getAttribute('data-cell-index'));

    if (gameState[clickedCellIndex] == '') {
        // request the bot next move
        gameState[clickedCellIndex] = currentPlayer;
        let botClickedCellIndex = requestBotPlay(clickedCellIndex);
        gameState[clickedCellIndex] = '';

        if(botClickedCellIndex>=0) {
            let botClickedCell = document.getElementById(botClickedCellIndex);
            let botPlayer = currentPlayer === "X" ? "O" : "X";
            botClickedCell.innerHTML = botPlayer;
            botClickedCell.style.color = 'red';
            previousBotCell = botClickedCell;
        }
    }
}

function handleCellOut(clickedCellEvent) {
    if (previousBotCell != null) {
        previousBotCell.style.color = '';
        previousBotCell.innerHTML = '';
        previousBotCell = null;
    }
}

document.querySelectorAll('.cell').forEach(cell => cell.addEventListener('click', handleCellClick));
document.querySelectorAll('.cell').forEach(cell => cell.addEventListener('mouseenter', handleCellIn));
document.querySelectorAll('.cell').forEach(cell => cell.addEventListener('mouseleave', handleCellOut));
document.querySelector('.game--restart').addEventListener('click', handleRestartGame);
 