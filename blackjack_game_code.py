import random

def create_deck():
    """Create a standard 52-card deck."""
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [{'rank': rank} for rank in ranks * 4]
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    score = 0
    num_aces = 0
    for card in hand:
        if card['rank'] in ['J', 'Q', 'K']:
            score += 10
        elif card['rank'] == 'A':
            num_aces += 1
            score += 11
        else:
            score += int(card['rank'])
    # convert aces to 1 if over 21
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score

def print_hand(hand, name):
    total_value = calculate_score(hand)
    print(f"\n{name}'s hand ({total_value}):")
    for card in hand:
        print(card['rank'])

def blackjack():
    """Play a game of blackjack."""
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    bet = 1
    
    print("Welcome to Blackjack!")
    print_hand(player_hand, "Player")
    print_hand([dealer_hand[0]], "Dealer")

    # Check for natural blackjack
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    if player_score == 21 and dealer_score == 21:
        print("Both player and dealer have a natural Blackjack. It's a tie!")
        return
    if player_score == 21 and dealer_score != 21:
        print("Natural Blackjack! You win!")
        return
    
    # First player choice with dd option
    choice = input("Do you want to hit, stand, or double down? (h/s/d): ").lower()
    if choice == 'd':
        bet *= 2
        new_card = deck.pop()
        player_hand.append(new_card)
        print("\nYou double down and draw:", new_card['rank'])
        print_hand(player_hand, "Player")
        # Player can only stand after doubling down (assuming they didn't bust)
        if calculate_score(player_hand) <= 21:
            choice = 's'
    elif choice == 'h':
        new_card = deck.pop()
        player_hand.append(new_card)
        print("\nYou draw:", new_card['rank'])
        print_hand(player_hand, "Player")
    elif choice == 's':
        pass
    
    # second player choice if they hit
    while choice != 's':         # can keep on hitting if under 21
        player_score = calculate_score(player_hand)
        if player_score == 21:
            print("Blackjack! You win!")
            break
        elif player_score > 21:
            print("Busted! You lose!")
            print_hand(dealer_hand, "Dealer")
            break
        
        choice = input("Do you want to hit or stand? (h/s): ").lower()
        if choice == 'h':
            new_card = deck.pop()
            player_hand.append(new_card)
            print("\nYou draw:", new_card['rank'])
            print_hand(player_hand, "Player")
        elif choice == 's':
            break

    if calculate_score(player_hand) <= 21:
        print_hand(dealer_hand, "Dealer")
        while calculate_score(dealer_hand) < 17:
            new_card = deck.pop()
            dealer_hand.append(new_card)
            print("\nDealer draws:", new_card['rank'])
        dealer_score = calculate_score(dealer_hand)
        print("\nDealer's score:", dealer_score)
        
        if dealer_score > 21:
            print("Dealer busted! You win!")
        elif dealer_score == player_score:
            print("It's a tie!")
        elif dealer_score > player_score:
            print("Dealer wins!")
        else:
            print("You win!")
    
    print("\nNumber of cards left in the deck:", len(deck))

blackjack()
