// board = [[null, null, null],
// [null, null, null],
// [null, null, null],]

let BOARD = [
    ['_', '_', '_'],
    ['_', '_', '_'],
    ['_', '_', '_']
]

const x_image = './assets/x.svg';
const o_image = './assets/o.svg';

const alpha_default = -9999
const beta_default = 9999

let start_game = false;

let human = 'o'
let bot = 'x'
let human_img = null
let bot_img = null

function get_absolute_score(board) {
    let count = 0
    for (var i = 0; i < board.length; i++) {
        for (var j = 0; j < board[i].length; j++) {
            if (board[i][j] === '_') {
                count++;
            }
        }
    }
    return count;
}

function get_score(board) {
    if (board[0][0] === board[1][1] && board[1][1] === board[2][2]) {
        if (board[1][1] === bot) {
            return get_absolute_score(board) + 1
        }
        if (board[1][1] === human) {
            return 0 - (get_absolute_score(board) + 1)
        }
    }
    if (board[2][0] === board[1][1] && board[1][1] === board[0][2]) {
        if (board[1][1] === bot) {
            return get_absolute_score(board) + 1
        }
        if (board[1][1] === human) {
            return 0 - (get_absolute_score(board) + 1)
        }
    }
    for (var i = 0; i < board.length; i++) {
        if (board[i][0] === board[i][1] && board[i][1] === board[i][2]) {
            if (board[i][1] === bot) {
                return get_absolute_score(board) + 1
            }
            if (board[i][1] === human) {
                return 0 - (get_absolute_score(board) + 1)
            }
        }
        if (board[0][i] === board[1][i] && board[1][i] === board[2][i]) {
            if (board[1][i] === bot) {
                return get_absolute_score(board) + 1
            }
            if (board[1][i] === human) {
                return 0 - (get_absolute_score(board) + 1)
            }
        }
    }
    return 0
}

function minimax(board, depth, isMax, alpha, beta) {
    let score = get_score(board);
    if (score > 0)
        return score;
    if (score < 0)
        return score;
    if (get_absolute_score(board) == 0)
        return 0;
    if (isMax) {
        let best = -1000;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                if (board[i][j] == '_') {
                    board[i][j] = bot;
                    best = Math.max(best, minimax(board, depth + 1, !isMax, alpha, beta));
                    alpha = Math.max(alpha, best);
                    board[i][j] = '_';
                    if (alpha >= beta) {
                        break;
                    }
                }
            }
        }
        return best;
    }
    else {
        let best = 1000;

        // Traverse all cells
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {

                if (board[i][j] == '_') {
                    board[i][j] = human;
                    best = Math.min(best, minimax(board, depth + 1, !isMax, alpha, beta));
                    beta = Math.min(beta, best);
                    board[i][j] = '_';
                    if (alpha >= beta) {
                        break;
                    }
                }
            }
        }
        return best;
    }
}

function bot_move(board) {
    let best_score = -9999;
    let position = [-1, -1];
    // BOARD.forEach(element => { console.log(element); });
    for (var i = 0; i < board.length; i++) {
        for (var j = 0; j < board[i].length; j++) {
            if (board[i][j] === '_') {
                board[i][j] = bot;
                let child_value = minimax(board, 0, false, -9999, 9999);
                board[i][j] = '_';
                if (child_value > best_score) {
                    best_score = child_value;
                    position[0] = i;
                    position[1] = j;
                }
            }
        }
    }
    return position;
}

function human_move(cubik) {

    if (!start_game) {
        alert('You must choose your symbol first !');
        return;
    }

    if (document.getElementById(cubik.id).childElementCount == 1) {
        return
    }
    img_human = document.createElement('img');
    img_human.src = human_img;
    img_human.style = 'height:75px; width:75px;';
    document.getElementById(cubik.id).appendChild(img_human);
    BOARD[cubik.id.charAt(0)][cubik.id.charAt(1)] = human;
    pos = bot_move(BOARD);
    BOARD[pos[0]][pos[1]] = bot;
    new_id = pos[0].toString().concat(pos[1].toString());
    img_bot = document.createElement('img');
    img_bot.src = bot_img;
    img_bot.style = 'height:75px; width:75px;';
    document.getElementById(new_id).appendChild(img_bot);
    BOARD.forEach(element => { console.log(element); });
}

function reset() {
    console.log("res");
    for (var i = 0; i < BOARD.length; i++) {
        for (var j = 0; j < BOARD[i].length; j++) {
            BOARD[i][j] = '_';
            if (document.getElementById(i.toString().concat(j.toString())).childElementCount == 1) {
                document.getElementById(i.toString().concat(j.toString())).removeChild(
                    document.getElementById(i.toString().concat(j.toString())).firstChild
                );
            }

        }
    }
}

function plays_as_x() {
    human = 'x';
    bot = 'o';
    human_img = x_image;
    bot_img = o_image;
    start_game = true;
}

function plays_as_o() {
    human = 'o';
    bot = 'x';
    human_img = o_image;
    bot_img = x_image;
    start_game = true;
}