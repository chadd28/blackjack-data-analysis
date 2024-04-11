import random

def create_deck():
    # creates standard 52 size deck
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

def split_hand(player_hand, dealer_hand, deck, bal, bet):     # only allow split once
        # deal with hand 1
        hand1 = [player_hand[0], deck.pop()]
        print_hand(hand1, "Hand 1")

        doubledDown_1 = False
        naturalBJ_1 = False
        # Check for natural blackjack
        hand1_score = calculate_score(hand1)
        if hand1_score == 21:        # no need to check dealer since that was checked at beginning of game
            print("Natural Blackjack pays 3:2!")
            naturalBJ_1 = True

        if naturalBJ_1 == False:   # only continue if player didn't get a natural blackjack
            choice = input("Do you want to hit, stand, double down? (h/s/d): ").lower()
            if choice == 'd':
                bal -= bet
                doubledDown_1 = True
                new_card = deck.pop()
                hand1.append(new_card)
                print("\nYou double down with $" + str(bet) + " and draw:", new_card)
                print_hand(hand1, "Hand 1")
                # Player can only stand after doubling down (assuming they didn't bust)
                if calculate_score(hand1) <= 21:
                    choice = 's'
            elif choice == 'h':
                new_card = deck.pop()
                hand1.append(new_card)
                print("\nYou draw:", new_card)
                print_hand(hand1, "Hand 1")
            elif choice == 's':
                pass
            
            # second player choice if they hit
            while choice != 's':         # can keep on hitting if under 21
                hand1_score = calculate_score(hand1)
                if hand1_score == 21:
                    print("Blackjack!")
                    break
                elif hand1_score > 21:
                    print("Busted! You lose! Your balance is now " + str(bal))
                    break
                
                choice = input("Do you want to hit or stand? (h/s): ").lower()
                if choice == 'h':
                    new_card = deck.pop()
                    hand1.append(new_card)
                    print("\nYou draw:", new_card)
                    print_hand(hand1, "Hand 1")
                elif choice == 's':
                    break
        print('\nYou are done with the first hand. Moving onto the second hand.')
        # end of while loop. at this point, the player is done with their first hand

        # deal with hand 2
        hand2 = [player_hand[1], deck.pop()]
        print_hand(hand2, "Hand 2")

        doubledDown_2 = False
        naturalBJ_2 = False
        # Check for natural blackjack
        hand2_score = calculate_score(hand2)
        if hand2_score == 21:        # no need to check dealer since that was checked at beginning of game
            print("Natural Blackjack pays 3:2!")
            naturalBJ_2 = True

        if naturalBJ_2 == False:      # only continue if player didn't get a natural blackjack
            choice = input("Do you want to hit, stand, double down? (h/s/d): ").lower()
            if choice == 'd':
                bal -= bet
                doubledDown_2 = True
                new_card = deck.pop()
                hand2.append(new_card)
                print("\nYou double down with $" + str(bet) + " and draw:", new_card)
                print_hand(hand2, "Hand 2")
                # Player can only stand after doubling down (assuming they didn't bust)
                if calculate_score(hand2) <= 21:
                    choice = 's'
            elif choice == 'h':
                new_card = deck.pop()
                hand2.append(new_card)
                print("\nYou draw:", new_card)
                print_hand(hand2, "Hand 2")
            elif choice == 's':
                pass
            
            # second player choice if they hit
            while choice != 's':         # can keep on hitting if under 21
                hand2_score = calculate_score(hand2)
                if hand2_score == 21:
                    print("Blackjack!")
                    break
                elif hand2_score > 21:
                    print("Busted! You lose! Your balance is still " + str(bal))
                    break
                
                choice = input("Do you want to hit or stand? (h/s): ").lower()
                if choice == 'h':
                    new_card = deck.pop()
                    hand2.append(new_card)
                    print("\nYou draw:", new_card)
                    print_hand(hand2, "Hand 2")
                elif choice == 's':
                    break
        # end of while loop. at this point, the player is done with their second hand

        hand1_score = calculate_score(hand1)
        hand2_score = calculate_score(hand2)
        print('\nValue of hand 1: ' + str(hand1_score) + '\nValue of hand 2: ' + str(hand2_score))

        # dealer plays
        print_hand(dealer_hand, "Dealer")
        while calculate_score(dealer_hand) < 17:
            new_card = deck.pop()
            dealer_hand.append(new_card)
            print("\nDealer draws:", new_card)
        dealer_score = calculate_score(dealer_hand)
        print("\nDealer's final score:", dealer_score, "\nResults:\n")
        
        # checks first hand with dealer
        if doubledDown_1 == True:
            print('Your first hand was doubled downed.')
            bet *= 2

        if hand1_score <= 21:
            if dealer_score > 21:    
                bal += bet*2
                print("Dealer busted! Your balance is now " + str(bal))
            elif dealer_score == hand1_score:
                bal += bet
                print("Your first hand was a tie. Your balance is now " + str(bal))
            elif naturalBJ_1 == True:          # checks if the hand score was a natural blackjack or not
                bal += bet*3
                print("Your first hand's natural blackjack pays 3:2. Your balance is now " + str(bal))
            elif dealer_score > hand1_score:
                print("Dealer wins against your first hand! Your balance is now " + str(bal))
            else:
                bal += bet*2
                print("Your first hand wins! Your balance is now " + str(bal))
        else:
            print('Your first hand busted. Your balance is now ' + str(bal))

        # checks second hand with dealer
        if doubledDown_1 == True:    # if already doubled down, reset bet value back to normal for second hand.
            bet /= 2
        if doubledDown_2 == True:
            print('Your second hand was doubled downed.')
            bet *= 2

        if hand2_score <= 21:
            if dealer_score > 21:           
                bal += bet*2
                print("Dealer busted! Your balance is now " + str(bal))
            elif dealer_score == hand2_score:
                bal += bet
                print("Your second hand was a tie. Your balance is now " + str(bal))
            elif naturalBJ_2 == True:
                bal += bet*3
                print("Your second hand's natural blackjack pays 3:2. Your balance is now " + str(bal))
            elif dealer_score > hand2_score:
                print("Dealer wins against your second hand! Your balance is now " + str(bal))
            else:
                bal += bet*2
                print("Your second hand wins! Your balance is now " + str(bal))
        else:
            print('Your second hand busted. Your balance is now ' + str(bal))
        
        print("\nNumber of cards left in the deck:", len(deck))


# main blackjack function
def blackjack(bal, bet):
    bal -= bet
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    print_hand(player_hand, "Player")
    print_hand([dealer_hand[0]], "Dealer")      # pass the dealer hand item as a list of length 1

    # Check for natural blackjack
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    if player_score == 21 and dealer_score == 21:
        bal += bet
        print("Both player and dealer have a natural Blackjack. It's a tie! Your balance is now " + str(bal))
        return
    if player_score == 21 and dealer_score != 21:
        bal += bet*3
        print("Natural Blackjack pays 3:2! You win! Your balance is now " + str(bal))
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
    
    #check for split
    if calculate_score([player_hand[0]]) == calculate_score([player_hand[1]]):      # need to pass the strings from the list as single item lists, the method takes list as parameter
        choice = input("Do you want to split? (y/n): ").lower()
        if choice == 'y':
            bal -= bet
            print('You split your cards and bet another ' + str(bet) + '. Your balance is now ' + str(bal))
            split_hand(player_hand, dealer_hand, deck, bal, bet)    # splitting plays a whole new version of the code that you can find above.
            return
        else:
            pass
   
    # First player choice includes the option to double down, surrender, and buy insurance if possible
    choice = input("Do you want to hit, stand, double down, surrender? (h/s/d/su): ").lower()
    if choice == 'd':
        bal -= bet
        bet *= 2
        new_card = deck.pop()
        player_hand.append(new_card)
        print("\nYou double down with $" + str(bet/2) + " and draw:", new_card)
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
        print("\nDealer's final score:", dealer_score)
        
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
