"""
This version doesn't include print statements for the game, just results.

Rules: 
- no splitting twice in a row
- no surrendering after a split
"""

import random

# creates the shoe. Can customize number of decks
def create_shoe(count):
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    shoe = ranks * 4 * count
    random.shuffle(shoe)
    return shoe

# takes in a hand and count, adds another card to hand and updates the count.
def draw_card(hand, shoe, totalCount):
    new_card = shoe.pop()
    totalCount += count([new_card])
    hand.append(new_card)
    return totalCount

def count(hand):
    count = 0
    for card in hand:
        if card in ['10', 'J', 'Q', 'K', 'A']:
            count -= 1
        elif card in ['2', '3', '4', '5', '6']:
            count += 1
    return count

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

def round_summary(player_hand, dealer_hand, totalCount, shoe, bal):
    # print('Round Summary:')
    # print_hand(player_hand, 'Player')
    # print_hand(dealer_hand, 'Dealer')
    # print('Current balance: ' + str(bal))
    # print('Running Count at end of round: ' + str(totalCount))
    # print("Number of cards left in the shoe:", len(shoe))
    # print('--------------')
    pass

# check for double down
def check_doubleDown(player_hand, dealer_hand):
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score([dealer_hand[0]])
    
    if player_score == 9 and dealer_score in (3, 4, 5, 6):
        return True
    elif player_score == 10 and dealer_score in range (2, 10): # includes 2 but doesnt include 10
        return True
    elif player_score == 11:
        return True
    #checks cases with the player having an A
    elif 'A' in player_hand:
        if "2" in player_hand and dealer_score in (5, 6):
            return True
        elif "3" in player_hand and dealer_score in (5, 6):
            return True
        elif "4" in player_hand and dealer_score in (4, 5, 6):
            return True
        elif "5" in player_hand and dealer_score in (4, 5, 6):
            return True
        elif "6" in player_hand and dealer_score in (3, 4, 5, 6):
            return True
        elif "7" in player_hand and dealer_score in (3, 4, 5, 6):
            return True
    elif player_hand == ['5', '5'] and dealer_score in range (2,10):
        return True
    else:
        return False

def check_surrender(player_hand, dealer_hand):
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score([dealer_hand[0]])

    if "A" not in player_hand:            # checks if these values are obtained without an Ace
        if player_score == 15 and dealer_score == 10:
            return True
        elif player_score == 16 and dealer_score in (9, 10):
            return True
        elif player_score == 16 and dealer_hand[0] == 'A':
            return True
        else:
            return False
    else:
        return False

def check_split(player_hand, dealer_hand):
    dealer_score = calculate_score(dealer_hand[0])

    if calculate_score([player_hand[0]]) == calculate_score([player_hand[1]]):      # checks if splitting is possible
        if ("2" in player_hand or "3" in player_hand) and dealer_score in range(2, 8):
            return True
        if '4' in player_hand and dealer_score in (5, 6):
            return True
        if '6' in player_hand and dealer_score in range (2, 7):
            return True
        if '7' in player_hand and dealer_score in range (2, 8):
            return True
        if '8' in player_hand:
            return True
        if '9' in player_hand and dealer_score in (2, 3, 4, 5, 6, 8, 9):
            return True
        if 'A' in player_hand:
            return True
    else:
        return False
    
def check_hit(player_hand, dealer_hand, shoe, totalCount):
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score([dealer_hand[0]])   # temporarily sets dealer_score to just score of visible card

        # this contains when the player should hit, given they didn't already double down, surrender, or split
    if player_score <= 11:                                
        totalCount = draw_card(player_hand, shoe, totalCount)
        return False, totalCount

    elif len(player_hand) == 2 and calculate_score([player_hand[0]]) == calculate_score([player_hand[1]]):    # checks hands with a pair ONLY if you have 2 cards
        if player_score <= 17:               # also takes in scenario of (A, A) = 12
            totalCount = draw_card(player_hand, shoe, totalCount)
            return False, totalCount
        elif player_score == 18 and dealer_score in (2, 3, 4, 5, 6, 8, 9):
            totalCount = draw_card(player_hand, shoe, totalCount)
            return False, totalCount
        else:            
            return True, totalCount

    elif player_score == 12 and dealer_score in (2, 3, 7, 8, 9, 10, 11):
        totalCount = draw_card(player_hand, shoe, totalCount)
        return False, totalCount
    elif player_score in range (13, 17) and dealer_score in range (7, 12):
        totalCount = draw_card(player_hand, shoe, totalCount)
        return False, totalCount

    elif 'A' in player_hand:                                                        # checks values with an Ace, a soft hit
        if player_score in range (13, 18):
            totalCount = draw_card(player_hand, shoe, totalCount)
            return False, totalCount
        elif player_score == 18:
            totalCount = draw_card(player_hand, shoe, totalCount)
            return False, totalCount
        else:
            return True, totalCount
            
    else:
        return True, totalCount
    

def split_hand(player_hand, dealer_hand, shoe, bal, bet, totalCount):
    global numNaturalBlackjacks      
    global numDoubleDowns
    global numDoubleDownsWins
    global numDoubleDownsLosses

    # deal with hand 1
    hand1 = [player_hand[0]]
    totalCount = draw_card(hand1, shoe, totalCount)
    
    doubledDown_1 = False
    naturalBJ_1 = False

    # Check for natural blackjack
    hand1_score = calculate_score(hand1)
    if hand1_score == 21:        # no need to check dealer since that was checked at beginning of game
        numNaturalBlackjacks += 1
        naturalBJ_1 = True
    
    if naturalBJ_1 == False:   # only continue if player didn't get a natural blackjack
        isStanding = False
    
        shouldDoubleDown = check_doubleDown(hand1, dealer_hand)
        if shouldDoubleDown == True:
            numDoubleDowns += 1
            doubledDown_1 = True
            bal -= bet
            totalCount = draw_card(hand1, shoe, totalCount)
            isStanding = True
    
        # break loop when the player should stand
        while isStanding == False:
            isStanding, totalCount = check_hit(hand1, dealer_hand, shoe, totalCount)
        
        # end of while loop. at this point, the player is done with their turn.


    # deal with hand2
    hand2 = [player_hand[1]]
    totalCount = draw_card(hand2, shoe, totalCount)
    
    doubledDown_2 = False
    naturalBJ_2 = False

    hand2_score = calculate_score(hand2)
    if hand2_score == 21:        # no need to check dealer since that was checked at beginning of game     
        numNaturalBlackjacks += 1
        naturalBJ_2 = True
    
    if naturalBJ_2 == False:   # only continue if player didn't get a natural blackjack
        isStanding = False
    
        shouldDoubleDown = check_doubleDown(hand2, dealer_hand)
        if shouldDoubleDown == True:
            numDoubleDowns += 1
            doubledDown_2 = True
            bal -= bet
            totalCount = draw_card(hand2, shoe, totalCount)
            isStanding = True
    
        # break loop when the player should stand
        while isStanding == False:
            isStanding, totalCount = check_hit(hand2, dealer_hand, shoe, totalCount)
        
        # end of while loop. at this point, the player is done with their turn.


    hand1_score = calculate_score(hand1)
    hand2_score = calculate_score(hand2)

    # dealer DOES NOT play when you bust both hands
    if hand1_score > 21 and hand2_score > 21:
        totalCount += count([dealer_hand[1]])
        round_summary(player_hand, dealer_hand, totalCount, shoe, bal)
        return bal, bet, shoe, totalCount

    # dealer drawing cards algorithm assuming you didn't bust both hands
    if calculate_score(player_hand) <= 21:
        while calculate_score(dealer_hand) < 17:
            new_card = shoe.pop()
            dealer_hand.append(new_card)
            totalCount += count([new_card])
        dealer_score = calculate_score(dealer_hand)
        totalCount += count([dealer_hand[1]])
        
        # all drawing cards are done. calculate final scores and payouts
        # checks first hand with dealer
        if doubledDown_1 == True:
            bet *= 2
        if hand1_score <= 21:
            if dealer_score > 21:    
                if naturalBJ_1 == True:      # checks if your hand was a natural blackjack when the dealer busts
                    bal += bet*2.5
                else:
                    bal += bet*2
                    if doubledDown_1 == True:
                        numDoubleDownsWins += 1
            elif dealer_score == hand1_score:   # checks a tie
                bal += bet
            elif naturalBJ_1 == True:          # checks if the hand score was a natural blackjack or not
                bal += bet*2.5
            elif dealer_score > hand1_score:     # checks if dealer beat player
                if doubledDown_1 == True:
                        numDoubleDownsLosses += 1
                pass
            else:
                bal += bet*2
                if doubledDown_1 == True:
                        numDoubleDownsWins += 1
        else:
            if doubledDown_1 == True:
                        numDoubleDownsLosses += 1
            pass

        # checks second hand with dealer
        if doubledDown_1 == True:    # if already doubled down, reset bet value back to normal for second hand.
            bet /= 2
        if doubledDown_2 == True:
            bet *= 2

        if hand2_score <= 21:
            if dealer_score > 21:           
                if naturalBJ_2 == True:     
                    bal += bet*2.5
                else:
                    bal += bet*2
                    if doubledDown_2 == True:
                        numDoubleDownsWins += 1
            elif dealer_score == hand2_score:
                bal += bet
            elif naturalBJ_2 == True:
                bal += bet*2.5
            elif dealer_score > hand2_score:
                if doubledDown_2 == True:
                    numDoubleDownsLosses += 1
                pass
            else:
                bal += bet*2
                if doubledDown_2 == True:
                    numDoubleDownsWins += 1
        else:
            if doubledDown_2 == True:
                numDoubleDownsLosses += 1
            pass
        
    # print('Round Summary (split):')
    # print_hand(hand1, 'Hand 1')
    # print_hand(hand2, 'Hand 2')
    # print_hand(dealer_hand, 'Dealer')
    # print('Current balance: ' + str(bal))
    # print('Running Count at end of round: ' + str(totalCount))
    # print("Number of cards left in the shoe:", len(shoe))
    # print('--------------')
    return bal, bet, shoe, totalCount
        

# cpu plays blackjack with basic strategy
def autoBlackjack_basic(bal, bet, shoe, totalCount):
    original_bet = bet
    bal -= bet
    player_hand = [shoe.pop(), shoe.pop()]
    dealer_hand = [shoe.pop(), shoe.pop()]

    totalCount = totalCount + count(player_hand) + count([dealer_hand[0]])


    # Check for player having a natural blackjack
    global numNaturalBlackjacks 
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    if player_score == 21 and dealer_score == 21:
        bal += bet
        totalCount += count([dealer_hand[1]])     
        numNaturalBlackjacks += 1
        round_summary(player_hand, dealer_hand, totalCount, shoe, bal)
        bet = original_bet 
        return bal, bet, shoe, totalCount
    if player_score == 21 and dealer_score != 21:
        bal += bet*2.5
        totalCount += count([dealer_hand[1]])    
        numNaturalBlackjacks += 1
        round_summary(player_hand, dealer_hand, totalCount, shoe, bal)
        bet = original_bet 
        return bal, bet, shoe, totalCount
    
    # no option for insurance since basic strat never buys insurance
    
    isStanding = False
    
    shouldDoubleDown = check_doubleDown(player_hand, dealer_hand)
    if shouldDoubleDown == True:
        global numDoubleDowns        # makes this variable accessable everywhere
        numDoubleDowns += 1
        bal -= bet
        bet *= 2
        totalCount = draw_card(player_hand, shoe, totalCount)
        isStanding = True

    shouldSplit = check_split(player_hand, dealer_hand)
    if shouldSplit == True:
        global numSplits       
        numSplits += 1
        bal -= bet
        bal, bet, shoe, totalCount = split_hand(player_hand, dealer_hand, shoe, bal, bet, totalCount)
        bet = original_bet  
        return bal, bet, shoe, totalCount
    
    shouldSurrender = check_surrender(player_hand, dealer_hand)
    if shouldSurrender == True:
        global numSurrenders       
        numSurrenders += 1
        bal += bet/2
        totalCount += count([dealer_hand[1]])
        round_summary(player_hand, dealer_hand, totalCount, shoe, bal)
        bet = original_bet 
        return bal, bet, shoe, totalCount # end the function, round is over.


    # break loop when the player should stand
    while isStanding == False:
        isStanding, totalCount = check_hit(player_hand, dealer_hand, shoe, totalCount)
    
    # end of while loop. at this point, the player is done with their turn.

    # check if player busted. If they did, reveal dealer's hand
    if calculate_score(player_hand) > 21:
        totalCount += count([dealer_hand[1]])

    # dealer drawing cards algorithm
    if calculate_score(player_hand) <= 21:
        while calculate_score(dealer_hand) < 17:
            new_card = shoe.pop()
            dealer_hand.append(new_card)
            totalCount += count([new_card])
            
        # all drawing cards are done. calculate final scores    
        dealer_score = calculate_score(dealer_hand)
        player_score = calculate_score(player_hand)
        totalCount += count([dealer_hand[1]])
        
        global numDoubleDownsWins
        global numDoubleDownsLosses
        if dealer_score > 21:
            if shouldDoubleDown == True:
                numDoubleDownsWins += 1
            bal += bet*2
        elif dealer_score == player_score:
            bal += bet
        elif dealer_score > player_score:
            if shouldDoubleDown == True:
                numDoubleDownsLosses += 1
            pass
        else:
            if shouldDoubleDown == True:
                numDoubleDownsWins += 1
            bal += bet*2
    
    round_summary(player_hand, dealer_hand, totalCount, shoe, bal)
    bet = original_bet   # resets bet to original value (if double downs increased the bet)
    return bal, bet, shoe, totalCount


# ------- ACTUAL MAIN RUNNING CODE ------- #
totalCount = 0
numDecks = 6        # number of decks in shoe
penetration = 0.75  # penetration of shoe before shoe resets
bal = 1000          # player balance
bet = 30            # bet per round
rounds = 1000         # number of rounds to simulate

# other statistics
numShoeResets = 0
numSplits = 0
numDoubleDowns = 0
numDoubleDownsWins = 0
numDoubleDownsLosses = 0
numSurrenders = 0
numNaturalBlackjacks = 0
maxCount = 0
minCount = float('inf')

print(f'\nWe are playing Blackjack with {numDecks} deck(s) and a shoe penetration of {penetration*100}%.')
print("Balance starts at " + str(bal) + ". Each bet is " + str(bet))
shoe = create_shoe(numDecks)

for i in range(rounds):
    #print('Round #' + str(i))
    bal, bet, shoe, totalCount = autoBlackjack_basic(bal, bet, shoe, totalCount)     # oops i didn't learn global variables before this 
    
    if totalCount > maxCount:
        maxCount = totalCount
    if totalCount < minCount:
        minCount = totalCount

    if len(shoe) < (1-penetration) * (numDecks * 52):     # if the number of cards remaining in the shoe is less than x% of all decks, reset shoe
        shoe = create_shoe(numDecks)
        totalCount = 0
        numShoeResets += 1

print('\nSummary after ' + str(rounds) + ' rounds of Blackjack:')
print('Current balance: $' + str(bal))
print(f"Running Count of current shoe: {totalCount}    |    Cards left in current shoe: {len(shoe)}    |    Num of shoe resets: {numShoeResets}")

print(f"""
Other Statistics:
Splits: {numSplits}    |    Double Downs: {numDoubleDowns}    |    Surrenders: {numSurrenders}    |    Natural BJs: {numNaturalBlackjacks}   
                Double Down Wins: {numDoubleDownsWins}
                Double Down Losses: {numDoubleDownsLosses}

Max Count: {maxCount}    |    Min Count: {minCount}
""")


