from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        state = []
        peg1 = []
        for fact in self.kb.facts:
            if str(fact.statement) == "(on disk1 peg1)":
                peg1.append(1)
            elif str(fact.statement) == "(on disk2 peg1)":
                peg1.append(2)
            elif str(fact.statement) == "(on disk3 peg1)":
                peg1.append(3)
            elif str(fact.statement) == "(on disk4 peg1)":
                peg1.append(4)
            elif str(fact.statement) == "(on disk5 peg1)":
                peg1.append(5)

        peg1.sort()
        state.append(tuple(peg1))

        peg2 = []
        for fact in self.kb.facts:
            if str(fact.statement) == "(on disk1 peg2)":
                peg2.append(1)
            elif str(fact.statement) == "(on disk2 peg2)":
                peg2.append(2)
            elif str(fact.statement) == "(on disk3 peg2)":
                peg2.append(3)
            elif str(fact.statement) == "(on disk4 peg2)":
                peg2.append(4)
            elif str(fact.statement) == "(on disk5 peg2)":
                peg2.append(5)

        peg2.sort()
        state.append(tuple(peg2))

        peg3 = []
        for fact in self.kb.facts:
            if str(fact.statement) == "(on disk1 peg3)":
                peg3.append(1)
            elif str(fact.statement) == "(on disk2 peg3)":
                peg3.append(2)
            elif str(fact.statement) == "(on disk3 peg3)":
                peg3.append(3)
            elif str(fact.statement) == "(on disk4 peg3)":
                peg3.append(4)
            elif str(fact.statement) == "(on disk5 peg3)":
                peg3.append(5)

        peg3.sort()
        state.append(tuple(peg3))
        temp = tuple(state)

        return temp

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        split_up = str(movable_statement).split()
        disk = split_up[1]
        peg_from = split_up[2]
        peg_to = split_up[3]

        on_top_of_stack_old = str("fact: (onTopOfStack " + disk + " " + peg_from + ")")
        on_top_fact_to_retract = parse_input(on_top_of_stack_old)
        self.kb.kb_retract(on_top_fact_to_retract)

        # need to retract the old peg no longer being on top of old stack
        for fact in self.kb.facts:
            my_fact = str(fact.statement).split()
            predicate = my_fact[0]
            if predicate == "(onTopOfStack":
                peg = my_fact[2]
                if peg == str(peg_to):
                    last_statement_to_remove = str("fact: (onTopOfStack " + my_fact[1] + " " + peg + ")")
                    last_fact_to_remove = parse_input(last_statement_to_remove)
                    self.kb.kb_retract(last_fact_to_remove)

        on_top_of_stack_new = str("fact: (onTopOfStack " + disk + " " + peg_to + ")")
        on_top_fact_to_add = parse_input(on_top_of_stack_new)
        self.kb.kb_add(on_top_fact_to_add)

        old_statement = str("fact: (on " + disk + " " + peg_from + ")")
        fact_to_retract = parse_input(old_statement)
        self.kb.kb_retract(fact_to_retract)

        new_statement = str("fact: (on " + disk + " " + peg_to + ")")
        fact_to_add = parse_input(new_statement)
        self.kb.kb_add(fact_to_add)

        old_peg_being_empty = str("fact: (empty " + peg_to + ")")
        another_fact_to_add = parse_input(old_peg_being_empty)
        self.kb.kb_retract(another_fact_to_add)

        # check if peg we're removing from is now empty
        on_disks = []
        for fact in self.kb.facts:
            my_fact = str(fact.statement).split()
            predicate = my_fact[0]
            if predicate == "(on":
                peg = my_fact[2]
                if peg == str(peg_from + ")"):
                    disk = my_fact[1]
                    on_disks.append(int(disk[4]))
        if len(on_disks)==0:
            new_peg_being_empty = str("fact: (empty " + peg_from + ")")
            third_fact_to_add = parse_input(new_peg_being_empty)
            self.kb.kb_add(third_fact_to_add)
        else:
            on_disks.sort()
            new_peg_being_empty = str("fact: (onTopOfStack disk" + str(on_disks[0]) + " " + peg_from + ")")
            third_fact_to_add = parse_input(new_peg_being_empty)
            self.kb.kb_add(third_fact_to_add)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for fact in self.kb.facts:
            if (len(str(fact.statement)) == 26):
                fact_statement = str(fact.statement)
                x = fact_statement[19]
                y = fact_statement[24]
                tile_num = fact_statement[14]
                if tile_num == 'y':
                    tile_num = -1
                else:
                    tile_num = int(tile_num)
                if x == '1':
                    if y == '1':
                        state[0][0] = tile_num
                    elif y == '2':
                        state[1][0] = tile_num
                    elif y == '3':
                        state[2][0] = tile_num
                elif x == '2':
                    if y == '1':
                        state[0][1] = tile_num
                    elif y == '2':
                        state[1][1] = tile_num
                    elif y == '3':
                        state[2][1] = tile_num
                elif x == '3':
                    if y == '1':
                        state[0][2] = tile_num
                    elif y == '2':
                        state[1][2] = tile_num
                    elif y == '3':
                        state[2][2] = tile_num
            else:
                continue
        state[0] = tuple(state[0])
        state[1] = tuple(state[1])
        state[2] = tuple(state[2])
        return tuple(state)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        split_up = str(movable_statement).split()
        if len(split_up) != 6:
            return
        tile = split_up[1]
        x_from = split_up[2]
        y_from = split_up[3]
        x_to = split_up[4]
        y_to = split_up[5]

        statement_to_retract = str("fact: (hasCoord " + tile + " " + x_from + " " + y_from + ")")
        fact_to_retract = parse_input(statement_to_retract)
        self.kb.kb_retract(fact_to_retract)

        another_statement_to_retract = str("fact: (hasCoord empty " + x_to + " " + y_to + ")")
        another_fact_to_retract = parse_input(another_statement_to_retract)
        self.kb.kb_retract(another_fact_to_retract)

        new_statement = str("fact: (hasCoord " + tile + " " + x_to + " " + y_to + ")")
        fact_to_add = parse_input(new_statement)
        self.kb.kb_add(fact_to_add)

        another_statement_to_add = str("fact: (hasCoord empty " + x_from + " " + y_from + ")")
        fact_to_add_two = parse_input(another_statement_to_add)
        self.kb.kb_add(fact_to_add_two)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
