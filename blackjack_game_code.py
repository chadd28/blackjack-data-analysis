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

def blackjack(bal, bet):
    """Play a game of blackjack."""
    bal -= bet
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    #dealer_hand = [deck.pop(), deck.pop()]
    dealer_hand = ['A', '10']

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
    
    # Check for insurance
    if dealer_hand[0] == 'A':
        choice = input("Do you want to buy insurance? (y/n): ").lower()
        if choice == 'y':
            insurance_bet = bet / 2  # Insurance bet is half of the original bet
            print(f"\nYou bought insurance for {insurance_bet}.")
            # Check if the dealer has blackjack
            if dealer_hand[1] in ['10', 'J', 'Q', 'K']:
                bal += insurance_bet * 2  # Insurance pays 2 to 1 if dealer has blackjack
                print("Dealer has blackjack! Insurance pays 2 to 1. Your balance is now " + str(bal))
                print_hand(dealer_hand, "Dealer")
                return
            else:
                print("Dealer doesn't have blackjack. You lose your insurance.")
                bal -= insurance_bet
        elif choice == 'n' and calculate_score(dealer_hand) == 21:
            print("\nDealer has blackjack!. You lose immediately. Your balance is now " + str(bal))
            print_hand(dealer_hand, "Dealer")
            return
   
    # First player choice includes the option to double down, surrender, and buy insurance if possible
    choice = input("Do you want to hit, stand, double down, surrender? (h/s/d/su): ").lower()
    if choice == 'd':
        bal -= bet
        bet *= 2
        new_card = deck.pop()
        player_hand.append(new_card)
        print("\nYou double down and draw:", new_card)
        print_hand(player_hand, "Player")
        # Player can only stand after doubling down (assuming they didn't bust)
        if calculate_score(player_hand) <= 21:
            choice = 's'
    elif choice == 'h':
        new_card = deck.pop()
        player_hand.append(new_card)
        print("\nYou draw:", new_card)
        print_hand(player_hand, "Player")
    elif choice == 's':
        pass
    elif choice == 'su':
        bal += bet/2
        print("\nYou surrender. Half your bet is returned. Your balance is now " + str(bal))
        print_hand(dealer_hand, "Dealer")
        return  # end the function, round is over.
    
    # second player choice if they hit
    while choice != 's':         # can keep on hitting if under 21
        player_score = calculate_score(player_hand)
        if player_score == 21:
            print("Blackjack!")
            break
        elif player_score > 21:
            print("Busted! You lose! Your balance is now " + str(bal))
            print_hand(dealer_hand, "Dealer")
            break
        
        choice = input("Do you want to hit or stand? (h/s): ").lower()
        if choice == 'h':
            new_card = deck.pop()
            player_hand.append(new_card)
            print("\nYou draw:", new_card)
            print_hand(player_hand, "Player")
        elif choice == 's':
            break
    # end of while loop. at this point, the player is done with their turn.

    if calculate_score(player_hand) <= 21:
        print_hand(dealer_hand, "Dealer")
        while calculate_score(dealer_hand) < 17:
            new_card = deck.pop()
            dealer_hand.append(new_card)
            print("\nDealer draws:", new_card)
        dealer_score = calculate_score(dealer_hand)
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
blackjack(bal, bet)
