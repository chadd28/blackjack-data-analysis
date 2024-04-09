import random

def create_deck():
    """Create a standard 52-card deck."""
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = ranks * 4
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    score = 0
    num_aces = 0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            score += 10
        elif card == 'A':
            num_aces += 1
            score += 11
        else:
            score += int(card)
    # convert aces to 1 if over 21
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score

def print_hand(hand, name):
    total_value = calculate_score(hand)
    print(f"\n{name}'s hand ({total_value}):")
    for card in hand:
        print(card)

# check for double down
def check_doubleDown(player_hand, dealer_hand):
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand[0])
    
    if player_score == 9 and dealer_score in (3, 4, 5, 6):
        print('double down')
    elif player_score == 10 and dealer_score in range (2, 10): # doesnt include 10
        print('double down')
    elif player_score == 11:
        print('double down')
    #checks cases with the player having an A
    elif 'A' in player_hand:
        if "2" in player_hand and dealer_score in (5, 6):
            print('double down')
        elif "3" in player_hand and dealer_score in (5, 6):
            print('double down')
        elif "4" in player_hand and dealer_score in (4, 6):
            print('double down')
        elif "5" in player_hand and dealer_score in (4, 6):
            print('double down')
        elif "6" in player_hand and dealer_score in (3, 6):
            print('double down')
        elif "7" in player_hand and dealer_score in (3, 6):
            print('double down')
    

# cpu plays blackjack with basic strategy
def autoBlackjack_basic(bal, bet):
    bal -= bet
    deck = create_deck()
    player_hand = ['A', '2']
    dealer_hand = ['5', '5']
    #dealer_hand = [deck.pop(), deck.pop()]
    
    print_hand(player_hand, "Player")
    print_hand([dealer_hand[0]], "Dealer")

    # Check for natural blackjack
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    if player_score == 21 and dealer_score == 21:
        bal += bet
        print("Both player and dealer have a natural Blackjack. It's a tie!. Your balance is now " + str(bal))
        return
    if player_score == 21 and dealer_score != 21:
        bal += bet*2
        print("Natural Blackjack! You win! Your balance is now " + str(bal))
        return
    
    # no option for insurance since basic strat never buys insurance
    
    check_doubleDown(player_hand, dealer_hand)
    
    # break loop when the player should stand
    while True:
        if calculate_score(player_hand) <= 8:
            new_card = deck.pop()
            player_hand.append(new_card)
        else:
            print_hand(player_hand, "Player")
            print('Player done drawing cards.')
            break
    
    # end of while loop. at this point, the player is done with their turn.

    # dealer drawing cards algorithm
    if calculate_score(player_hand) <= 21:
        print_hand(dealer_hand, "Dealer")
        while calculate_score(dealer_hand) < 17:
            new_card = deck.pop()
            dealer_hand.append(new_card)
            print("\nDealer draws:", new_card)
            
        # all drawing cards are done. calculate final scores    
        dealer_score = calculate_score(dealer_hand)
        player_score = calculate_score(player_hand)
        print("\nDealer's score:", dealer_score)
        
        if dealer_score > 21:
            bal += bet*2
            print("Dealer busted! You win! Your balance is now " + str(bal))
        elif dealer_score == player_score:
            bal += bet
            print("It's a tie! Your balance is now " + str(bal))
        elif dealer_score > player_score:
            print("Dealer wins! Your balance is now " + str(bal))
        else:
            bal += bet*2
            print("You win! Your balance is now " + str(bal))
    
    print("\nNumber of cards left in the deck:", len(deck))
    


bal = 100       # player balance
bet = 10        # bet per round

print("Welcome to Blackjack! Each bet is " + str(bet))
#blackjack(bal, bet)
autoBlackjack_basic(bal, bet)
