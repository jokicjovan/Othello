from state import State
from hashmap import ChainedHashMap
from tree import Tree, TreeNode
from copy import deepcopy
import time

hash_map = ChainedHashMap(100000)

def make_tree(state, color, depth, tree, tree_root=None):
    result = state.is_end()
    if depth == 0 or result == True:
        return

    if color == "⭘":
        op_color = "●"
    else:
        op_color = "⭘"

    all_valid_moves = state.get_valid_moves(color)
    child_node = TreeNode(state)

    if tree_root == None:
        tree.root = child_node
    else:
        tree_root.add_child(child_node)

    for i in all_valid_moves:
        new_state = deepcopy(state)
        x = i[0]
        y = i[1]
        new_state.play_move(x, y, color)
        make_tree(new_state, op_color, depth-1, tree, child_node)


def minimax(node, alpha, beta, maximizingPlayer):
    if (node.is_leaf() == True or node.data.is_end() == True):
        temp = hash_map[node.data.board]
        if temp == None:
            result = node.data.dynamic_heuristic_evaluation()
            hash_map[node.data.board] = result
            return result
        else:
            return temp

    if maximizingPlayer:
        maxEval = -99999999999999
        for child in node.children:
            eval = minimax(child, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = 99999999999999
        for child in node.children:
            eval = minimax(child, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

class Game(object):

    __slots__ = ['_current_state', '_player_turn']

    def __init__(self):
        self._current_state = None
        self._player_turn = "⭘"
        self.initialize_game()

    def initialize_game(self):
        self._current_state = State()
        self._player_turn = "⭘"


    def play(self):
        br = 0
        print("⭘ - black player")
        print("● - white player (AI)")
        while True:
            br+= 1
            print(self._current_state)
            if  self._current_state.is_end() == True:
                winner = self._current_state.declare_winner()
                print("Game over!")
                if winner == "Tie":
                    print("It's a Tie!")
                else:
                    print("The Winner is " + winner + "!")
                    black, white = self._current_state.get_board_score()
                    print("Black score: " + str(black))
                    print("White score: " + str(white))
                print("Game finished in " + str(br) + " turns!")
                break

            if self._player_turn == "⭘":
                if self._current_state.get_valid_moves("⭘") == []:
                    print("No free moves, opponent plays again!")
                    self._player_turn = "●"
                    continue

                while True:
                    print("Fields you can play: ")
                    turns = ""
                    for i in self._current_state.get_valid_moves("⭘"):
                        turns = turns + str(i) + ", "
                    print(turns[:-2])
                    px = input("Insert the row number: ")
                    py = input("Insert the column number: ")

                    if px.isnumeric() == True and py.isnumeric() == True and 0 <= int(px) <= 7 and 0 <= int(py) <= 7 \
                            and self._current_state.move_validation(int(px), int(py), "⭘") != False:
                        self._current_state.play_move(int(px), int(py), "⭘")
                        self._player_turn = "●"
                        break
                    else:
                        print("The move is not valid! Try again.\n")

            elif self._player_turn == "●":
                valid_moves = self._current_state.get_valid_moves("●")
                num_of_valid_moves = len(valid_moves)

                if num_of_valid_moves == 0:
                    print("AI have no free moves, you play again!")
                    self._player_turn = "⭘"
                    continue

                if num_of_valid_moves == 1:
                    self._current_state.play_move(valid_moves[0][0], valid_moves[0][1], "●")
                else:
                    if num_of_valid_moves < 4:
                        depth = 5
                    elif 4 < num_of_valid_moves < 12:
                        depth = 4
                    else:
                        depth = 3

                    start = time.time()
                    tree = Tree()
                    state = self._current_state
                    make_tree(state, self._player_turn, depth, tree)
                    max = -9999999999999999999

                    for child in tree.root.children:
                        temp = minimax(child, -99999999999999, 99999999999999, True)
                        if temp > max:
                            max = temp
                            state = child.data
                    end = time.time()
                    print("Time of execution: " + str(round(end - start, 7)))
                    self._current_state = deepcopy(state)
                self._player_turn = "⭘"