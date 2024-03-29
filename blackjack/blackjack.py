import tkinter
import random


def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']

    if tkinter.TkVersion >= 8.5:
        extension = 'png'
    else:
        extension = 'ppm'

    for suit in suits:                                                         # ???
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))                                 # appending the tuple (x, y,) , - end

        for card in face_cards:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))                                   # 10 - points


def _deal_cards(frame):
    # pop the next card off the top of the deck
    next_card = deck.pop(0)
    # and add it to back of the pack
    deck.append(next_card)
    # add the image to the label and display the label - image[1] as it's inside the tuple! -> 0 - points, 1 - image
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')   # pack inside grid - OK
    # now return the card's face value
    return next_card


def score_hand(hand):
    # Calculate the total score of all cards in the list
    # Only one ace can have the value 11 and this will be reduce to 1 if the hand busts
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we bust, check if there's an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(_deal_cards(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set('Dealer wins!')
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set('Player wins!')
    elif dealer_score > player_score:
        result_text.set('Dealer wins!')
    else:
        result_text.set('Draw!')


def deal_player():
    player_hand.append(_deal_cards(player_card_frame))
    player_score = score_hand(player_hand)
    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set('Dealer wins!')
    print(locals())

    # global player_score
    # global player_ace
    # card_value = deal_cards(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     player_ace = True
    #     card_value = 11
    # player_score += card_value
    # # if we bust, check if there's an ace and subtract
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set('Dealer wins!')
    # print(locals())


def initial_deal():
    deal_player()
    dealer_hand.append(_deal_cards(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    # clearing both dealer and player frames
    dealer_card_frame.destroy()
    player_card_frame.destroy()
    # creating new ones with the very same names
    dealer_card_frame = tkinter.Frame(table, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    player_card_frame = tkinter.Frame(table, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set('')
    # resetting the cards
    dealer_hand = []
    player_hand = []
    initial_deal()


def shuffle():
    random.shuffle(deck)


def play():
    initial_deal()

    root.mainloop()


root = tkinter.Tk()
# Setup
root.title('Blackjack')
root.geometry('640x480')
root.configure(background='green')

result_text = tkinter.StringVar()
result = tkinter.Label(root, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

table = tkinter.Frame(root, relief='sunken', borderwidth=1, background='green')
table.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)
# dealer's score
dealer_score_label = tkinter.IntVar()
tkinter.Label(table, text='Dealer', background='green', fg='white').grid(row=0, column=0)
tkinter.Label(table, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)
# dealer's cards frame
dealer_card_frame = tkinter.Frame(table, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
# player's score
player_score_label = tkinter.IntVar()
# player_score = 0  - needed for 1st deal_player()
# player_ace = False

tkinter.Label(table, text='Player', background='green', fg='white').grid(row=2, column=0)
tkinter.Label(table, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)
# player's cards frame
player_card_frame = tkinter.Frame(table, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)
# buttons
button_frame = tkinter.Frame(root)
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')

dealer_button = tkinter.Button(button_frame, text='Dealer', command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text='Player', command=deal_player)
player_button.grid(row=0, column=1)

new_game_button = tkinter.Button(button_frame, text='New Game', command=new_game)
new_game_button.grid(row=0, column=2)

shuffle_button = tkinter.Button(button_frame, text='Shuffle', command=shuffle)
shuffle_button.grid(row=0, column=3)

# motor
cards = []
load_images(cards)
print(cards)
# deck/pack of cards and shuffle
deck = list(cards)
shuffle()

# dealer's and player's hands
dealer_hand = []
player_hand = []

if __name__ == "__main__":
    play()

