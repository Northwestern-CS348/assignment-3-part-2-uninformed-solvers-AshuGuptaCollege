import sys
from solver import *
from heapq import heappop, heappush

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # check its gameStates and if its equal to victory condition, return true

        if self.gm.getGameState() == self.victoryCondition:
            return True

        # how do we get the next game state as a node?
        currNode = self.currentState
        currMove = currNode.requiredMovable
        currDepth = currNode.depth

        next_game_states = self.gm.getMovables()

        # if moves is empty
        if len(next_game_states) == 0:
            self.gm.reverseMove(currMove)
            self.currentState = self.currentState.parent
            self.solveOneStep()
        else:
            unvisited_child_found = False
            for move in next_game_states:
                self.gm.makeMove(move)
                # create a node
                # whats depth
                child = GameState(self.gm.getGameState(), currDepth+1, move)
                # reverse the move
                self.gm.reverseMove(move)
                if child in self.visited:
                    continue
                else:
                    unvisited_child_found = True
                    self.currentState.children.append(child)
                    child.parent = self.currentState
                    # mark the node as not visited
                    self.visited[child] = True
                    self.gm.makeMove(move)
                    self.currentState = child
                    break
            if unvisited_child_found is False:
                self.gm.reverseMove(currMove)
                self.currentState = self.currentState.parent
                self.solveOneStep()
                #my_parent = currNode.parent
                #next_move = my_parent.requiredMovable
                #self.gm.makeMove(next_move)


class SolverBFS(UninformedSolver):
    my_queue = []

    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.gm.getGameState() == self.victoryCondition:
            return True

        currNode = self.currentState
        currDepth = currNode.depth

        next_game_states = self.gm.getMovables()

        if len(next_game_states) == 0 and currNode.parent is not None and len(self.my_queue) > 0:
            to_pop = self.my_queue.pop(0)
            self.node_traveral_helper(to_pop)
            return
        elif len(next_game_states) == 0 and len(self.my_queue) == 0:
            return False
        else:
            for move in next_game_states:
                self.gm.makeMove(move)
                # create a node
                next_depth = currDepth + 1
                child = GameState(self.gm.getGameState(), next_depth, move)
                # reverse the move
                self.gm.reverseMove(move)
                if child in self.visited:
                    continue
                else:
                    self.currentState.children.append(child)
                    child.parent = self.currentState
                    # mark the node as not visited
                    self.visited[child] = False
                    self.my_queue.append(child)

        if len(self.my_queue) == 0:
            return False
        else:
            next_move_to_make = self.my_queue.pop(0)
            self.visited[next_move_to_make] = True
            self.node_traveral_helper(next_move_to_make)


    def node_traveral_helper(self, Next_GameState):
        # reverse the node until you get back to root
        while self.currentState.parent is not None:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        moves = []
        Some_State = Next_GameState
        while Some_State.parent is not None:
            moves.insert(0, Some_State.requiredMovable)
            Some_State = Some_State.parent

        for move in moves:
            if move is not None:
                #print(str(move))
                self.gm.makeMove(move)

        self.currentState = Next_GameState
