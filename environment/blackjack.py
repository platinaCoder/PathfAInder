import random
import numpy as np 

def create_deck():
    """Create a shuffled deck of 52 cards."""
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    random.shuffle(deck)
    return deck

def deal_card(deck):
    """Deal a single card from the deck."""
    if len(deck) == 0:
        deck = create_deck()
    card, *new_deck = deck
    return card, new_deck

def calculate_score(hand):
    """Calculate the score of a hand."""
    score = sum(hand)
    num_aces = hand.count(11)
    while score > 21 and num_aces:
        score -= 10
        num_aces -= 1
    return score

def play_dealer_hand(dealer_hand, deck):
    """Play the dealer's hand according to Blackjack rules."""
    while calculate_score(dealer_hand) < 17:
        card, deck = deal_card(deck)
        dealer_hand.append(card)
    return dealer_hand, deck

def evaluate_game(player_hand, dealer_hand, player_money, current_bet):
    """Evaluate the game and return updated player money."""
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    if player_score > 21:
        return player_money - current_bet, "Player busts, dealer wins!"
    elif dealer_score > 21 or player_score > dealer_score:
        return player_money + current_bet, "Player wins!"
    elif player_score < dealer_score:
        return player_money - current_bet, "Dealer wins!"
    else:
        return player_money, "Push!"

def get_state_representation(player_hand, dealer_visible_card):
    """Represents the game state as a one-hot encoded vector."""
    state = np.zeros(52 + 1 + 13)  # 13 for each card value, 1 for num aces, 13 for dealer's card
    for card in player_hand:
        state[card - 1] = 1
    state[26 + len(player_hand.count(11))] = 1  
    state[39 + dealer_visible_card - 1] = 1 
    return state

def start_game(player_money, base_bet):
    """Initialize the game, deal initial cards."""
    deck = create_deck()
    player_hand, dealer_hand = [], []
    for _ in range(2):
        card, deck = deal_card(deck)
        player_hand.append(card)
        card, deck = deal_card(deck)
        dealer_hand.append(card)
    current_bet = base_bet
    return player_hand, dealer_hand, deck, player_money, current_bet

def player_decision(player_hand, deck, decision):
    """Process the player's decision: 'hit' or 'stand'."""
    if decision == 'hit':
        card, deck = deal_card(deck)
        player_hand.append(card)
    return player_hand, deck

# Example of playing a game
player_money, base_bet = 1000, 10
player_hand, dealer_hand, deck, player_money, current_bet = start_game(player_money, base_bet)
print(f"Initial hands: Player: {player_hand}, Dealer: {dealer_hand[0]} [hidden]")
# Assume player decides to hit
player_hand, deck = player_decision(player_hand, deck, 'hit')
# Dealer plays
dealer_hand, deck = play_dealer_hand(dealer_hand, deck)
# Evaluate game
player_money, outcome = evaluate_game(player_hand, dealer_hand, player_money, current_bet)
print(outcome)
print(f"Player's final money: {player_money}")
