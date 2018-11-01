# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 16:00:16 2018

@author: Chris
"""

# Go Fish

# Contains all the functions to run a simulation of go-fish
# It has not been optimized for efficiency

import numpy as np

# Objects


# Possible objects



#### Variables

hand1 = []
hand2 = []
hand3 = []
hand4 = []
pile1 = []
pile2 = []
pile3 = []
pile4 = []
score1 = 0
score2 = 0
score3 = 0
score4 = 0

    
player1 = [hand1, pile1, score1]
player2 = [hand2, pile2, score2]
player3 = [hand3, pile3, score3]
player4 = [hand4, pile4, score4]


players = [player1, player2, player3, player4]

wins = [0,0,0,0]

    
def reset_players():        # This function resets the players' hands
    global hand1            # It also defines the players'
    global hand2            # hand, pile, and score
    global hand3            # Definitely does not look efficient
    global hand4            # by any means.
    global pile1            # Now that I'm finished I realize that I
    global pile2            # probably don't need most of these
    global pile3            # variables, but I don't want to break
    global pile4            # anything.
    global score1
    global score2
    global score3
    global score4
    global player1
    global player2
    global player3
    global player4
    global players
    hand1 = []
    hand2 = []
    hand3 = []
    hand4 = []
    pile1 = []
    pile2 = []
    pile3 = []
    pile4 = []
    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0
    player1 = [hand1, pile1, score1]
    player2 = [hand2, pile2, score2]
    player3 = [hand3, pile3, score3]
    player4 = [hand4, pile4, score4]
    players = [player1, player2, player3, player4]

def reset_wins():         # This function resets the number of wins
    global win1           # after the simulation finishes.
    global win2
    global win3
    global win4
    global wins
    win1 = 0
    win2 = 0
    win3 = 0
    win4 = 0
    wins = [win1, win2, win3, win4]

###################################################
# Determine turn order
    
# The function below is used to determine the turn order.
# It randomly generates one of the player's index value and then chooses
# the turn order where that player goes first.
# I explicitly made lists for the turn orders because I assumed
# the players sat at the same spot each game and went clockwise
# i.e. if player 2 goes first, then player 3 goes next and so on.

def get_turn_order():
    turn_orders = [[0,1,2,3], [1,2,3,0], [2,3,0,1], [3,0,1,2]]
    n = np.random.rand()
    rn = int(len(turn_orders)*n)
    turn_order = turn_orders[rn]
    return turn_order

    
#### Define and Shuffle Deck
    
# This function creates the deck and shuffles it. The textbook code for
# generating a deck was used.

def prepare_deck():
    global deck
    global ranks
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = []
    for i in ranks:
        for j in suits:
            deck.append(i + ' ' + j)
    np.random.shuffle(deck)


#### Deal Cards
    
# This function deals out 5 cards to each player. It uses a counter
# to keep track of how many cards were given to everyone.

def deal_cards():
    init_hand_count = 0
    while init_hand_count < 5:
        for player in players:
            player[0].append(deck[0])
            deck.remove(deck[0])
        init_hand_count = init_hand_count + 1   

#### player's turn ########################
    
################# Asking Functions

# The next set of functions handle "asking" players for cards

# hand_info gathers the unique ranks that the player has in their hand.
# It uses the list of ranks defined in the deck generating code
# With the for loop, it goes through each rank and checks if the 
# player has that rank in hand. A list if the set of those ranks is made
                    
def hand_info(player):
    ranks_in_hand = []
    for i in ranks:
        for card in player[0]:
            if card.count(i) > 0:
                ranks_in_hand.append(i)
    new_ranks = list(set(ranks_in_hand))            
    return new_ranks


# This function below randomly selects another player besides itself.
# It returns a value that is used as an index to identify player to ask
# The value of this function is called in the main ask function.
    
def select_player_to_ask(player):        
    player_id = [0,1,2,3]
    player_id.remove(players.index(player))
    n = np.random.rand(1)
    n = (n*len(player_id)).astype(int)
    player_to_ask = np.take(player_id, n)
    return player_to_ask[0]

# The function below selects a random rank from the list generated from
# the hand_info function noted previously. This rank is called in 
# the main ask function
    
def select_rank_to_ask(player):
    p_ranks = hand_info(player)
    n = np.random.rand()
    rn = int(len(p_ranks)*n)
    ask_rank = np.take(p_ranks, rn)
    return ask_rank[0]

# The function below looks for any matches the player has after asking
# other players. It uses append and remove to move cards from the hand
# to the discard pile.
    

def match_cards(player, card_rank):
    for card in player[0]:
        if card.count(card_rank) > 0:
            player[1].append(card)
            player[0].remove(card)
    player[2] = player[2] + 1        


# The function below is the main ask function that calls for the previous 
# functions to work. It also determines if the player "wins" and gets 
# ask for another card.            
    
def ask_for_card(player):
    global win
    matches = 0    
    ask_player = select_player_to_ask(player)
    ask_rank = select_rank_to_ask(player)
    for card in players[ask_player][0]:
        if card.count(ask_rank) > 0:
            player[0].append(card)
            players[ask_player][0].remove(card)
            win = 1
            matches = matches + 1
    if matches > 0:        
        match_cards(player, ask_rank)
    else:
        win = 0              
    

############# fishing functions
        
# This is the function that tells the player to "fish" from the "pond"
# It appends the first entry of the deck to the player's hand and 
# removes the same card from the deck.
                        
def go_fish(player):
    player[0].append(deck[0])
    deck.remove(deck[0])
             
################################
    
######## End Turn Functions
    
# The following functions are called after the end of a player's turn.

# draw_five draws 5 cards for the player. Uses an if statement in a 
# for loop to check the deck size after each draw. It is called for in
# the next function.
    
def draw_five(player):
    for i in list(range(5)):
        if len(deck) != 0:
            player[0].append(deck[0])
            deck.remove(deck[0]) 
        
# check_hand checks to see if the player has 0 cards and calls
# the draw_five function.
            
def check_hand(player):
    if len(player[0]) == 0:
        draw_five(player)
        
# The function below is used to check the hands of every player and 
# retrieve the unique ranks for each hand. This function is used
# in tandem with check_for_unique to determine whether to end the game
# or continue. The sets of ranks from each player is made into a list,
# and then combined into a large list. 
    
def get_all_card_ranks():
    total_ranks = []
    for player in players:
        h = []
        for card in player[0]:
            r = card[0]
            h.append(r)
        h2 = list(set(h))
        total_ranks.extend(h2)
    all_ranks = ''.join(total_ranks)
    return all_ranks

# The list generated above is then checked for duplicate ranks. 
# If there are no duplicates, then it is no longer
# possible to continue the game. The global variable end_game
# is changed to 1 so the game terminates.

def check_for_unique(all_ranks):
    global end_game    
    for r in ranks:
        if all_ranks.count(r) > 1 :
            break
        else:
            end_game = 1
            
# The function below is the function that calls the previous
# two functions to determine the state of the game.
            
def check_game_state():
    if len(deck) == 0:
        all_ranks = get_all_card_ranks()
        check_for_unique(all_ranks)
            
        
######################################
        
####### player_turn(player):
        
# This is the function that calls on the functions necessary for a 
# single player's turn. It calls for the functions that:
        # ask for a card
        # make the player go fish
        # check the player's hand

def player_turn(player):
    global win
    win = ''
    while win != 0:
        ask_for_card(player)
    if win == 0 and len(deck) > 0:
        go_fish(player)
    check_hand(player)
        
     
#######################################

##### End Game Functions
    
# These are the end game functions that are used to determine the winner


# This function makes a list of each player's score for the game
# The indices for this list match that of the list of players
    
def get_scores():
    scores = []
    for player in players:
        scores.append(player[2])
    return scores

# Using the list of scores, this next function checks to see which
# player had the highest score.
# It stores a score and its index in a variable and replaces the score
# and index when it comes across a higher score. The index is returned.

    
def get_winner(players):
    high_score = 0
    victor = 0
    scores = get_scores()
    for score in scores:
        if score > high_score:
            high_score = score
            victor = scores.index(score)
    return victor
   

# The index from the last function is used in this function. 
# The index corresponds to the winning player who gets 1 win added to 
# their number of wins, which is an element of the global variable, wins.
         
def add_win(victor):
    wins[victor] = wins[victor] + 1


# Tally_win is the main function that calls get_winner and add_win.
def tally_win():
    victor = get_winner(players)
    add_win(victor)
        
##############################################



##############################################


# The function below is the simulation function itself. It allows for
# the specification of the number of games to simulate. 
# This function keeps track of the end_game variable
# It also resets the wins before running the sim.
# The function returns the list of wins for each player. 
    # The elements in the list are the wins for players 1 through 4 
    # respectively.

def play_gofish(n_games):
    global end_game
    reset_wins()
    for n in list(range(n_games)):
        reset_players()
        prepare_deck()
        deal_cards()
        playerid = get_turn_order()
        end_game = 0
        while end_game == 0:
            for p in playerid:
                player = players[p]
                player_turn(player)
                check_game_state()
        tally_win()
    return wins

################################################
    
############################################
    
########### Testing ####
    
#reset_players()
#prepare_deck()
#deal_cards()
#player1
#player2
#player3
#player4
#get_all_card_ranks()
#play_gofish(100)
#en(deck)
