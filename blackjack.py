from random import randrange

CARD_SYMBOLS = (None, "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

class BlackjackGame:
    def __init__(self, bet):
        self.bet = bet
        self.p_hand = []    # Player's hand
        self.d_hand = []    # Dealer's hand
        self.d_hand_visible = False

    '''
    Return number representing a card.
    1=Ace, 11=Jack, 12=Queen, 13=King.
    '''
    def draw_card(self):
        return randrange(1,14)

    '''
    Advance the game according to the player's command.
    Return a 3-tuple containing:
    0- whether the game is finished, 1- the payout (if any), 2- message to display to player.
    '''
    def act(self, action):
        if(action == "begin"):
            for i in range(0,2):
                self.p_hand.append(self.draw_card())
                self.d_hand.append(self.draw_card())
        elif(action == "hit"):
            self.p_hand.append(self.draw_card())
        elif(action == "stand"):
            self.d_hand_visible = True
            while(self.get_score(self.d_hand) < 17):
                self.d_hand.append(self.draw_card())

        message = self.status_msg()
        if(self.game_finished()):
            results = self.game_results()
            message += results[1]
            return (True, results[0], message)
        message += "\n You may hit or stand.\n"
        return (False, None, message)

    '''
    Return value of hand.
    '''
    def get_score(self, hand):
        hand_copy = hand.copy()
        hand_copy.sort(reverse=True)    #Ensure that aces are counted last
        score = 0
        for card in hand_copy:
            if(card > 1):
                score += min(10, card)    #Jacks/queens/kings are worth 10
            elif(card == 1):
                score += (1 if (score > 11) else 11)
        return score

    '''
    Return whether game is finished.
    Game is finished if the player and/or dealer has a score of 21 or higher,
    or if the dealer's hand has been revealed and carries a score of at least 17.
    '''
    def game_finished(self):
        p_score = self.get_score(self.p_hand)
        d_score = self.get_score(self.d_hand)
        return (p_score >= 21) or (d_score == 21) or (self.d_hand_visible and d_score >= 17)

    '''
    Returns payout for player, and string describing game results.
    Should only be called when game is finished.
    '''
    def game_results(self):
        p_score = self.get_score(self.p_hand)
        d_score = self.get_score(self.d_hand)
        if(p_score > 21):
            return (0, "Your score is over 21, so you bust and win nothing.")
        elif(d_score > 21):
            payout = int(self.bet * 1.5)
            return (payout, "The dealer bust, so you win!")
        elif(p_score == d_score):
            return (self.bet, "You and the dealer tied, so your bet is returned.")
        elif(p_score == 21):
            payout = int(self.bet * 1.5)
            return (payout, "You reached exactly 21, so you win!")
        elif(p_score > d_score):
            payout = int(self.bet * 1.5)
            return (payout, "You have a higher score than the dealer, so you win!")
        else:
            return (0, "The dealer has a higher score than you, so you lose.")

    '''
    Return message describing player's and dealer's hands.
    '''
    def status_msg(self):
        message = "Your hand: " + ", ".join([CARD_SYMBOLS[card] for card in self.p_hand])
        message += " (Total: " + str(self.get_score(self.p_hand)) + ")\n"
        if(self.d_hand_visible):
            message += "Dealer's hand: " + ", ".join([CARD_SYMBOLS[card] for card in self.d_hand])
            message += " (Score: " + str(self.get_score(self.d_hand)) + ")\n"
        else:
            d_card = self.d_hand[0]
            message += "Dealer's hand: " + CARD_SYMBOLS[d_card] + ", ?"
            message += " (Score: " + str(d_card if (d_card > 1) else 11) + ")\n"
        return message
        
        
    
