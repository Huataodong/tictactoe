import sys


visited_node = []
g_depth = 100


class MiniMax:
    next_pos = None
    global visited_node
    global g_depth

    def __init__(self, board, player, ai_sign, isPrune, depth,  _alpha, _beta):
        self.board = board
        self.player_turn = player
        # self.depth = depth
        self.chose_state = None
        self.winner = False
        self.ai_sign = ai_sign
        # self.visited_node = []
        self.alpha = _alpha
        self.beta = _beta
        self.isPrune = isPrune
        self.depth = depth

    def next_move(self, board):
        self.board = board
        self.get_score()
        # self.file.close()
        return self.next_pos

    def get_score(self):
        aiToken = self.ai_sign

        winner = self.check_win()
        if winner != False:
            state = ''.join(self.board) + ' '
            if winner == 'draw':
                state += str(1)
                return 1
            if winner == aiToken:
                state += str(2)
                return 2
            else:
                state += str(0)
                return 0

        available_pos = self.get_available_pos()

        scores = []

        maxScore = -1000
        minScore = 1000

        for pos in available_pos:
            new_board = self.generate_newBoard(pos, self.player_turn)

            child_state = MiniMax(new_board, change_turn(self.player_turn), self.ai_sign, self.isPrune, self.depth+1, self.alpha, self.beta)
            child_score = child_state.get_score()

            scores.append((pos, child_score))

            visited_node.append(''.join(new_board) + ' ' + str(child_score-1) + '\n')

            #if self.depth > g_depth:
            #    break

            # prune
            if self.isPrune:
                if self.player_turn == aiToken:
                    if child_score > maxScore:
                        maxScore = child_score
                        self.alpha = maxScore
                    if self.alpha >= self.beta:
                        break
                else:
                    if child_score < minScore:
                        minScore = child_score
                        self.beta = minScore
                    if self.alpha >= self.beta:
                        break

        # FOR node of MAX, return the max value of leaf node
        if self.player_turn == aiToken:
            max_score_pos = max(scores, key=lambda x: x[1])
            max_score = max_score_pos[1]
            self.next_pos = max_score_pos[0]
            return max_score
        else:
            # FOR node of MIN, return the min value of leaf node
            min_score_pos = min(scores, key=lambda x: x[1])
            min_score = min_score_pos[1]
            self.next_pos = min_score_pos[0]
            return min_score

    def check_win(self):
        board = self.board

        # Check Vertical
        for i in range(0, 9, 3):
            if board[i] != '-' and board[i] == board[i + 1] == board[i + 2]:
                return board[i]

        # Check Horizontal
        for i in range(3):
            if board[i] != '-' and board[i] == board[i + 3] == board[i + 6]:
                return board[i]

        # Check Diagonal
        if board[0] != '-' and board[0] == board[4] == board[8]:
            return board[0]
        if board[2] != '-' and board[2] == board[4] == board[6]:
            return board[2]

        # If there is no position which could place a piece, then it is a draw
        for i in range(9):
            if board[i] == '-':
                return False
        return 'draw'

    def get_available_pos(self):
        result = []
        for i in range(9):
            if self.board[i] == '-':
                result.append(i)
        result.sort()
        return result

    def generate_newBoard(self, pos, player):
        newBoard = list(self.board)
        newBoard[pos] = player
        return newBoard


def change_turn(player):
    if player == 'x':
        return 'o'
    else:
        return 'x'


def main(state, path, isPrune):
    global visited_node
    # determine if there are further moves
    if '-' not in state:
        # print('No further moves!')
        return

    # determine whose turn it is
    if 'x' not in state and 'o' not in state:
        turn = 'x'
    elif state.count('x') > state.count('o'):
        turn = 'o'
    else:
        turn = 'x'

    state_list = list(state)
    ai = MiniMax(state_list, turn, 'x', isPrune, 0, -1000, 1000)
    next_pos = ai.next_move(state_list)
    state_list[next_pos] = turn
    print(''.join(state_list))

    with open(path, 'w') as f:
        for node in visited_node:
            f.write(node)
    f.close()


if __name__ == '__main__':
    state = sys.argv[1]
    path = sys.argv[2]
    # print('state:', state)
    # print('path:', path)
    args = len(sys.argv)
    isPrune = False
    if args > 3 and sys.argv[3] == 'prune':
        isPrune = True
    if args > 4:
        g_depth = int(sys.argv[4])

    main(state, path, isPrune)
