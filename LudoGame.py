# Author: Rachel Xing
# GitHub username: rachelx000
# Date: 08/04/2022
# Description: Write a program for a board game called Ludo game that allows two to four people to play.

class Player:
    """
    A Player class that represents the player who plays the game at a certain position.
    """
    def __init__(self, position):
        """
        Initializes a Player with required data members by taking the position the player chooses.
        All data members are private.
        """
        self._position = position  # The position the player choose (A, B, C, or D)
        self._start = None  # Initializes the start position to None
        self._end = None  # Initializes the end position to None
        self._p_current_position = "H"  # Initializes the token p's position
        self._q_current_position = "H"  # Initializes the token q's position
        # There are four possible positions of two tokens: in the home yard ("H"), ready to go ("R"),
        # somewhere on the board (an integer or in the home square), or has finished ("E").
        self._p_step_count = -1  # Initializes the total steps the token p has moved to 0
        self._q_step_count = -1  # Initializes the total steps the token p has moved to 0
        self._player_current_state = "is still playing"  # Initializes the current state of the player
        # There are three possible states of players: has won, finished the game, or is still playing.

    def set_player(self, position):
        """
        Sets the start and end of the player by taking the chosen position.
        """
        if position == "A":
            self._start = 1
            self._end = 50
        elif position == "B":
            self._start = 15
            self._end = 8
        elif position == "C":
            self._start = 29
            self._end = 22
        elif position == "D":
            self._start = 43
            self._end = 36
        else:
            return

    def set_p_ready_to_go(self):
        """
        Sets token p to the ready-to-go position.
        """
        self._p_current_position = "R"
        self._p_step_count = 0

    def set_q_ready_to_go(self):
        """
        Sets token q to the ready-to-go position.
        """
        self._q_current_position = "R"
        self._q_step_count = 0

    def set_winner(self):
        """
        Sets the state of the player to "has won" when the player won the game.
        """
        self._player_current_state = "has won"

    def set_finished(self):
        """
        Sets the state of the player to "finished the game" when the player finished the game and the other has won the game.
        """
        self._player_current_state = "finished the game"

    def get_completed(self):
        """
        Returns True if the player has finished the game without accepting any parameters; Otherwise, return False.
        """
        if self._p_current_position == "E" and self._q_current_position == "E":
            return True
        else:
            return False

    def get_player_current_state(self):
        """
        Returns the current state of the player.
        """
        return self._player_current_state

    def get_p_current_position(self):
        """
        Returns the current position of the token p.
        """
        return self._p_current_position

    def get_q_current_position(self):
        """
        Returns the current position of the token q.
        """
        return self._q_current_position

    def get_token_p_step_count(self):
        """
        Returns the total steps the token p has taken on the board.
        """
        return self._p_step_count

    def get_token_q_step_count(self):
        """
        Returns the total steps the token q has taken on the board.
        """
        return self._q_step_count

    def get_space_name(self, total_steps_of_the_token):
        """
        Returns the name of the space the token has landed on the board by taking the total steps of the token.
        """
        if total_steps_of_the_token == -1:  # steps = -1 for the home yard position
            return "H"
        elif total_steps_of_the_token == 0:  # steps = 0 for the ready to go position
            return "R"
        elif total_steps_of_the_token == 57:  # steps = 57 for the end position
            return "E"
        elif total_steps_of_the_token <= 50:  # the token is at somewhere on the board (pos is an integer from 1 to 56).
            current_token_pos = self._start + total_steps_of_the_token - 1
            if current_token_pos > 56:
                current_token_pos = current_token_pos - 56
            return str(current_token_pos)
        elif total_steps_of_the_token > 50:  # the token is at somewhere of home squares.
            return self._position + str(total_steps_of_the_token-50)

    def move_p_token(self, steps_token_moved):
        """
        Moves the token p on the broad with the given steps.
        """
        self._p_step_count += steps_token_moved
        if self._p_step_count > 57:  # the total step should not be larger than 57.
            self._p_step_count = 57 - (self._p_step_count - 57)
        self._p_current_position = self.get_space_name(self._p_step_count)

    def move_q_token(self, steps_token_moved):
        """
        Moves the token q on the broad with the given steps.
        """
        self._q_step_count += steps_token_moved
        if self._q_step_count > 57:  # the total step should not be larger than 57.
            self._q_step_count = 57 - (self._q_step_count - 57)
        self._q_current_position = self.get_space_name(self._q_step_count)

    def kick_out_token(self, token_name):
        """
        Kicks the token from the board to its home yard by taking the token name.
        """
        if token_name == "p":
            self._p_current_position = "H"
            self._p_step_count = -1
        elif token_name == "q":
            self._q_current_position = "H"
            self._q_step_count = -1


class LudoGame:
    """
    A LudoGame class that represents the Ludo game as played.
    """
    def __init__(self):
        """
        Initializes a LudoGame with information about players and the board without taking any parameters.
        All data members are private.
        """
        self._game_info = {}  # Initialize an empty dictionary to store players' information on the game board.

    def get_player_by_position(self, player_pos):
        """
        Returns the player object by taking the player's position as a string.
        Returns "Player not found!" if taking an invalid string parameter.
        """
        if player_pos in self._game_info:
            return self._game_info[player_pos]
        else:
            return "Player not found!"

    def decide_token_to_move(self, player, steps_token_moved):
        """
        Returns the name of the recommended token to be moved by taking the current player and moved steps.
        The movement of token follows the below rules:
        Rule 1: If the die roll is 6, try to let the token that is still in the home yard get out of the home yard
                (if both tokens are in the home yard, choose the first one ‘p’)
        Rule 2: If one token is already in the home squares and the step number is exactly what is needed to reach the
                end squares, let that token move and finish.
        Rule 3: If one token can move and kick out an opponent token, then move that token
        Rule 4: Move the token that is further away from the finishing square
        """
        p_step_count_before = player.get_token_p_step_count()
        p_step_count_after = p_step_count_before + steps_token_moved
        if p_step_count_after > 57:  # the total step should not be larger than 57.
            p_step_count_after = 57 - (p_step_count_after - 57)
        p_after_pos = player.get_space_name(p_step_count_after)
        q_step_count_before = player.get_token_q_step_count()
        q_step_count_after = q_step_count_before + steps_token_moved
        if q_step_count_after > 57:  # the total step should not be larger than 57.
            q_step_count_after = 57 - (q_step_count_after - 57)
        q_after_pos = player.get_space_name(q_step_count_after)
        if steps_token_moved == 6:  # Rule 1
            if player.get_p_current_position() == "H":
                return "p"
            elif player.get_p_current_position() != "H" and player.get_q_current_position() == "H":
                return "q"
        if p_after_pos == "E":  # Rule 2
            return "p"
        elif q_after_pos == "E":
            return "q"
        for player_pos in self._game_info:  # Rule 3
            if self._game_info[player_pos] != player:
                if self._game_info[player_pos].get_p_current_position() == p_after_pos or \
                        self._game_info[player_pos].get_q_current_position() == p_after_pos:
                    return "p"
                elif self._game_info[player_pos].get_p_current_position() == q_after_pos or \
                        self._game_info[player_pos].get_q_current_position() == q_after_pos:
                    return "q"
        if q_step_count_before > p_step_count_before and player.get_p_current_position() != "H":  # Rule 4
            return "p"
        elif q_step_count_before > p_step_count_before and player.get_p_current_position() == "H" and \
                player.get_q_current_position() != "H":
            return "q"
        elif q_step_count_before < p_step_count_before and player.get_q_current_position() != "H":  # Rule 4
            return "q"
        elif q_step_count_before < p_step_count_before and player.get_q_current_position() == "H" and \
                player.get_p_current_position() != "H":
            return "p"
        elif q_step_count_before == p_step_count_before and player.get_q_current_position() != "H" and \
                player.get_p_current_position() != "H":
            return "p"

    def move_token(self, player, token_name, steps_token_moved):
        """
        Move the one token on the board by taking the player object, the token name, and the steps the token will move.
        Will also update the token's total steps, and kick out other opponent tokens as needed.
        play_game() uses this method.
        """
        if token_name == "p":
            if player.get_p_current_position() == "H":
                player.set_p_ready_to_go()
            elif player.get_p_current_position() == "R":
                player.move_p_token(steps_token_moved)
            elif player.get_p_current_position() == player.get_q_current_position():
                player.move_p_token(steps_token_moved)
                player.move_q_token(steps_token_moved)
            else:
                player.move_p_token(steps_token_moved)
            if player.get_p_current_position() != "R":
                for player_pos in self._game_info:  # take care of kicking out other opponent tokens as needed
                    if self._game_info[player_pos] != player and \
                            self._game_info[player_pos].get_player_current_state() == "is still playing":
                        if self._game_info[player_pos].get_p_current_position() == player.get_p_current_position():
                            self._game_info[player_pos].kick_out_token("p")
                        if self._game_info[player_pos].get_q_current_position() == player.get_p_current_position():
                            self._game_info[player_pos].kick_out_token("q")
        elif token_name == "q":
            if player.get_q_current_position() == "H":
                player.set_q_ready_to_go()
            elif player.get_q_current_position() == "R":
                player.move_q_token(steps_token_moved)
            elif player.get_p_current_position() == player.get_q_current_position():
                player.move_p_token(steps_token_moved)
                player.move_q_token(steps_token_moved)
            else:
                player.move_q_token(steps_token_moved)
            if player.get_q_current_position() != "R":
                for player_pos in self._game_info:  # take care of kicking out other opponent tokens as needed
                    if self._game_info[player_pos] != player and \
                            self._game_info[player_pos].get_player_current_state() == "is still playing":
                        if self._game_info[player_pos].get_p_current_position() == player.get_q_current_position():
                            self._game_info[player_pos].kick_out_token("p")
                        if self._game_info[player_pos].get_q_current_position() == player.get_q_current_position():
                            self._game_info[player_pos].kick_out_token("q")

    def get_token_list(self):
        """
        Return a list of strings representing the current space of all the tokens for each player in the list.
        """
        current_token_list = []
        for player_pos in self._game_info:
            player = self.get_player_by_position(player_pos)
            player_p_pos = player.get_p_current_position()
            current_token_list.append(player_p_pos)
            player_q_pos = player.get_q_current_position()
            current_token_list.append(player_q_pos)
        return current_token_list

    def play_game(self, players_list, turns_list, turns_count=-1, winner=0):
        """
        Return a list of strings representing the current spaces of all of the tokens for each player in the players_list
        after all moving is done in the turns_list by taking players_list and turns_list.
        """
        if turns_count == -1:  # Base case for the start of the game
            for player_pos in players_list:
                # Initialize tokens on the game broad and insert their information into game_info list.
                player = Player(player_pos)
                player.set_player(player_pos)
                self._game_info[player_pos] = player
            return self.play_game(players_list, turns_list, turns_count+1, winner)
        elif turns_count == len(turns_list):  # Base case for passing all turns
            final_token_list = self.get_token_list()
            return final_token_list
        else:
            current_player = self.get_player_by_position(turns_list[turns_count][0])
            if type(current_player) is not str:
                # print(current_player.get_player_current_state())
                if current_player.get_player_current_state() == "is still playing":
                    token_to_move = self.decide_token_to_move(current_player, turns_list[turns_count][1])
                    # print(token_to_move)
                    self.move_token(current_player, token_to_move, turns_list[turns_count][1])
                    if current_player.get_completed() is True:  # check completeness of the current player
                        if winner == 0:
                            current_player.set_winner()
                            winner += 1
                        else:
                            current_player.set_finished()
            # print(self.get_token_list())
            return self.play_game(players_list, turns_list, turns_count+1, winner)
