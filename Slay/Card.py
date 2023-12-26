import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Scrollbar, Listbox, Frame,Canvas,Label,ttk,Text,DISABLED,END,NORMAL
import glob

images = dict() 
#initialize widgets and images
root = tk.Tk()
root.title("Deck Manager")
background = Image.open("Misc/back.png")
backRen = ImageTk.PhotoImage(background)
background_label = tk.Label(root, image=backRen)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
buttonFrame = Frame(root)
buttonFrame.grid(row=0,column=0,sticky='n')
cardFrame = Frame(root)
cardFrame.grid(row = 0, column = 1, sticky='w')
textFrame = Frame(root)
textFrame.grid(row =1, column = 1,sticky='s')
text= Label(cardFrame)

allCards = []



for x in glob.glob("Buttons/*.png"):
    my_image = Image.open(x)
    my_image = my_image.resize((60, 60))  
    x = x.rsplit('\\')[1]
    name = x.rsplit('.')[0]
    red = ImageTk.PhotoImage(my_image)
    images[name]=red

for x in glob.glob("*.png"):
    my_image = Image.open(x)
    my_image = my_image.resize((339, 437))  
    name = x.rsplit('.')[0]
    red = ImageTk.PhotoImage(my_image)
    images[name]=red
    allCards.append(name)



root.geometry('800x800')


def showDmg():
    global cardFrame
    clear()
    val = maxAtk()

#calculates the maximum defense from the current deck, then displays the cards that achieve this feat
def maxDef():
    draw = deck.copy()
    play = list()
    man = 0
    for x in draw:
        #add a subset of the deck to the final calculation to avoid pointless further conplexity
        if cards[x][2] > 0:
                play.append(x)
                man = man + cards[x][0]
                print(play)
    diff = man - mana
    play = removeLowestDefs(play,diff)
    clearButtons()
    showCards(play,False)
    return totalDef(play)

#returns the total defence sum from the passed list of cards
def totalDef(deckVar):
    draw = deckVar.copy()
    man = 0
    play = list()
    defe = 0
    for x in draw:
        if  cards[x][2] > 0:
                play.append(x)
                man = man + cards[x][0]
                defe = defe + cards[x][2]
    return defe

#play is the current "hand" and man is the required mana to prune before all cards can be cast
#recursively prune cards from the hand untill the mana conforms within the cost requirements.
def removeLowestDefs(play,man):
    if man <= 0:
        if(len(states) > 0):
            if(totalDef(states[0]) < totalDef(play)):
                states.clear()   
                states.add((tuple(play))) 
        return play
    else:
        target = man
        hand = play.copy()
        ret = hand.copy()
        name = hand[0]
        min = 0
        counter = 0
        for y in hand:
            hand.remove(y)
            proc = hand.copy()
            target = target - cards[y][0]
            temp = removeLowestDefs(proc,target)
            if totalDef(temp) > min:
                min = totalDef(temp)
                ret = temp
            hand.insert(counter,y)
            counter = counter +1
            target = target + cards[y][0]
        target = target - cards[name][0]
        return ret


#returns the total defence sum from the passed list of cards, must take into account the "vulnurable" status effect which increases damage done
def maxAtk():

    draw = deck.copy()
    state = []
    man = 0
    vul = 0
    vulMin = 0
    play = list()
    atk = 0
    for x in draw:
        if cards[x][1] > 0:
                if cards[x][3]:
                    if not bool(vul):
                        vul = 1
                        vulMin = cards[x][1]
                    elif vulMin > cards[x][1]:
                        vulMin = cards[x][1]
                play.append(x)
                man = man + cards[x][0]
                print(play)
                atk = atk + cards[x][1]
    if bool(vul):
        atk = atk + (atk-vulMin)*.5
    diff = man - mana
    play = removeLowestAtks(play,diff)
    print(play)
    clearButtons()
    showCards(play,False)
    return totalAtk(play)

#returns the total attack sum from the passed list of cards
def totalAtk(deckVar):
    draw = deckVar.copy()
    state = []
    man = 0
    vul = 0
    vulMin = 0
    play = list()
    atk = 0
    for x in draw:
        if cards[x][1] > 0:
            #check if applies vul, if so then our math needs to change
                if cards[x][3]:
                    if not bool(vul):
                        vul = 1
                        vulMin = cards[x][1]
                    elif vulMin > cards[x][1]:
                        vulMin = cards[x][1]
                play.append(x)
                man = man + cards[x][0]
                atk = atk + cards[x][1]
    if bool(vul):
        atk = atk + (atk-vulMin)*.5
    return atk

#finds the cost of the passed list of cards.
def cost(play):
    val = 0
    for y in play:
        val = val + cards[y][0]
    return val

states = set()

#play is the current "hand" and man is the required mana to prune before all cards can be cast
#recursively prune cards from the hand untill the mana conforms within the cost requirements.
def removeLowestAtks(play,man):
    if man <= 0:
        if(len(states) > 0):
            if(totalAtk(states[0]) < totalAtk(play)):
                states.clear()   
                states.add((tuple(play))) 
        return play
    else:
        target = man

        hand = play.copy()
        ret = hand.copy()
        name = hand[0]
        min = 0
        counter = 0
        for y in hand:
            hand.remove(y)
            proc = hand.copy()
            target = target - cards[y][0]
            temp = removeLowestAtks(proc,target)
            if totalAtk(temp) > min:
                min = totalAtk(temp)
                ret = temp
            hand.insert(counter,y)
            counter = counter +1
            target = target + cards[y][0]
        target = target - cards[name][0]
        return ret

#clear all widgets and remake them.
def clearAll():
    clear()
    clearButtons()
    clearText()

# finds how synergistic a card is with the current deck.
def syn (card):
    pos = 0
    neg = 0
    temp = deck.copy()
    for x in temp:
        if x == card or card in counterSyn:
            neg = neg + 1
        if card in synergy:
            pos = pos + 1
    return pos - neg


#this is a list of evaluation maps to store information about the cards.
deck = ["Bash","Strike","Strike","Strike","Strike","Strike","Defend","Defend","Defend","Defend","Defend"]
mana = 3


cards = dict({"Strike": [1,6,0,0],"Defend": [1,0,5,0], 
"Bash" : [2,8,0,.5], "Perfected Strike" : [2,16,0,0], "Dropkick" : [1,5,0,0], "Uppercut" : [2,13,0,.5], 
"Anger" : [0,4,0,0], "Body Slam" : [1,0,0,0], "Clash" : [0,14,0,0], "Cleave" : [1,8,0,0], "Clothesline" : [2,13,0,1], "Headbutt" : [1,8,0,0], 
"Heavy Blade" : [2,12,0,0], "Iron Wave" : [1,5,5,0], "Sword Boomerang" : [1,9,0,0], "Wild Strike" : [1,12,0,0], "SearingBlow" : [2,12,0,0],
"BloodforBlood": [4,18,0,0], "Carnage" : [2,20,0,0],  "Rampage" : [1,8,0,0], "SeverSoul" : [2,16,0,0], "Whirlwind" : [1,5,0,0], "Pummel" : [1,8,0,0],
"Hemokinesis" : [1,15,0,0], "RecklessCharge" : [0,7,0,0], "Feed" : [1,10,0,0], "Reaper" : [1,4,0,0], "FiendFire" : [1,7,0,0], "Bludgeon" : [3,32,0,0],
"Immolate" : [2,21,0,0], "Armaments" : [1,0,5,0], "ShrugItOff" : [1,0,8,0], "TrueGrit" : [1,0,7,0], "FlameBarrier" : [2,0,12,0], "GhostlyArmor" : [1,0,10,0],
"Sentinel" : [1,0,5,0], "PowerThrough" : [1,0,15,0]})
cardAtk = dict({"Strike": 1, "Defend": 2, "Survivor": 3, "Neutrialize": 4}) 
cardStrength = dict({"Strike": 1, "Defend": 2, "Bash": 3, "Perfected Strike" : 4, "Dropkick" : 2, "Uppercut" : 3}) 
synergy = dict({"Bash" : [], "Perfected Strike" : ["Strike"], "Dropkick" : ["Bash","Thunderclap","Uppercut"],"Dropkick" : [],"Uppercut" : []})
counterSyn = dict({"Clash" : ["Defend"] })



scrollDist = 0
#clears the card frame
def clear():
    global cardFrame
    cardFrame.destroy()
    cardFrame = Frame(root)
    cardFrame.grid(row = 0, column = 1, sticky='w')
    cardFrame.configure(bg='')
#clears all the buttons
def clearButtons():
    global buttonFrame
    global card1,card2,card3
   
    buttonFrame.destroy()
    scrollDist = 0
    buttonFrame = Frame(root)
    buttonFrame.grid(row = 0, column = 0, sticky='n')
    imgBtn = tk.Button(buttonFrame, image=images["Deck"], command=lambda:[resetScroll(),showDeck()]).grid(row=0,column=0,sticky ='nw')
        
    select1 = tk.Button(buttonFrame, image=images["Red"], command=lambda:[resetScroll(), showSelection(1)]).grid(row=1,column=0,sticky ='s')
    select2 = tk.Button(buttonFrame, image=images["Blue"], command=lambda:[resetScroll(), showSelection(2)]).grid(row=2,column=0,sticky ='s')
    select3 = tk.Button(buttonFrame, image=images["Green"], command=lambda:[resetScroll(), showSelection(3)]).grid(row=3,column=0,sticky ='s')


    Evaluate = tk.Button(buttonFrame ,image=images["Str"], command=showDmg).grid(row=6,column=0,sticky ='s')
    EvaluateDef = tk.Button(buttonFrame ,image=images["Dex"], command=showDef).grid(row=7,column=0,sticky ='s')
    if card1 != '' and card2 != ''  and card3 != '':
        Take =  tk.Button(buttonFrame ,image=images["Eval"], command=evaluateSelections).grid(row=8,column=0,sticky ='s')

notDeck = False
#reset the scroll distance
def resetScroll():
    global scrollDist
    scrollDist = 0

# draw a new set of cards based on the current scroll being moved up or down.
def scrollDown(val,num):
    global scrollDist
    scrollDist = scrollDist - 1
    if scrollDist < 0 :
        scrollDist = 0
    clear()
    if( val):
        showDeck()
    else:
        showSelection(num)

def scrollUp(val,num):
    global scrollDist
    scrollDist = scrollDist +1
    clear()
    if(val):
        showDeck()
    else:
        showSelection(num)

#show all the cards in the deck
def showDeck():
    clearAll()
    global scrollDist
    global cardFrame
   
    over = False
    dc = deck.copy()
    counter = 1
    rows = 0
    total = scrollDist * 10
    size = len(dc) + total
    cardCount = 0
   # mylist = Listbox(frame, yscrollcommand = w.set).grid(row = 2,column=7, sticky = 'ns')
    for d in dc:
      
        if cardCount >= total and cardCount <= len(dc):
            my_mage_label = tk.Label(cardFrame,image =images[d]).grid(row = rows,column = counter,sticky='ws',padx=5, pady=5)
   
            counter = counter +1
            if counter >= 6:
                rows = rows +1
                counter = 1
        else:
            over = True
        cardCount = cardCount + 1
    if not over:
        imgBtn = tk.Button(buttonFrame, image=images["Up"], command=lambda: scrollUp(True,-1)).grid(row=4,column=0,sticky ='s')
    imgBtn = tk.Button(buttonFrame, image=images["Down"], command=lambda: scrollDown(True,-1)).grid(row=5,column=0,sticky ='s')

#add card to deck
def addCard(card):
    global deck
    deck.append(card)
#clear the text frame
def clearText():
    global textFrame
    textFrame.destroy()
    textFrame = Frame(root)
    textFrame.grid(row =1, column = 1,sticky='s')

#checks if 3 cards have been selected for evaluation, and if so then displays the eval button
def evalCheck():
    global buttonFrame
    if card1 != '' and card2 != ''  and card3 != '':
        Take =  tk.Button(buttonFrame ,image=images["Eval"], command=evaluateSelections).grid(row=8,column=0,sticky ='s')

#shows all the cards in the cards parameter. Disable modifies if the displayed cards act as buttons that add themselves to the deck.
def showCards(cards,disable):
    clearAll()

    dc = cards.copy()
    counter = 1
    rows = 0
    total = scrollDist * 10
    size = len(dc) + total
    cardCount = 0
   # mylist = Listbox(frame, yscrollcommand = w.set).grid(row = 2,column=7, sticky = 'ns')
    for d in dc:
       # if cardCount >= total and cardCount <= len(dc) and not disable:
        if disable:
            my_mage_label = tk.Label(cardFrame,image =images[d]).grid(row = rows  ,column = counter,sticky='ws',padx=5, pady=5)
        else:
            my_mage_label = tk.Button(cardFrame,image =images[d], command=lambda : [addCard(d),clear(),clearButtons(),clearText()]).grid(row = rows ,column = counter)

        counter = counter +1
        if counter >= 6:
            rows = rows +1
            counter = 1
        cardCount = cardCount + 1

#shows cards that can be selected to be evaluated.
def showSelection(num):
    clearAll()

    counter = 1
    rows = 0
    total = scrollDist * 10
    cards = allCards.copy()
    over = False
    cardCount = 0
    printed = 0
    for d in cards:
        cardCount = cardCount + 1
        if cardCount >= total and cardCount <= total + 15:
            printed = printed +1
            print(printed)
            my_mage_label = tk.Button(cardFrame,image =images[d], command=lambda d = d: [selectCard(d,num),evalCheck()]).grid(row = rows ,column = counter)
            counter = counter +1
            if counter >= 6:
                rows = rows +1
                counter = 1
        
    if printed >= 10:
        imgBtn = tk.Button(buttonFrame, image=images["Up"], command=lambda: scrollUp(False,num)).grid(row=4,column=0,sticky ='s')
    imgBtn = tk.Button(buttonFrame, image=images["Down"], command=lambda: scrollDown(False,num)).grid(row=5,column=0,sticky ='s')

card1=''
card2=''
card3=''
#depending on the passed num vairiable, set the corresponding card selection.
def selectCard(d,num):
#make switch
    global card1,card2,card3

    print(d)
    if num == 1:
        print("card1 is now: " + d)
        card1 = d
    elif num == 2:
        print("card2 is now: " + d)
        card2 = d
    else:
        print("card3 is now: " + d)
        card3 = d

#determines which card to take from the selections.
def evaluateSelections():
    global card1,card2,card3
    cards = [card1,card2,card3]
    showCards(cards,False)
    str1 = 0
    str2 =0
    str3 = 0
    if card1 in cardStrength:
        str1 = cardStrength[card1]
    if card2 in cardStrength:
        str2 = cardStrength[card2]
    if card3 in cardStrength:
        str3 = cardStrength[card3]
    val1 = str1 + syn(card1)
    val2 = str2 + syn(card2)
    val3 = str3 + syn(card3)
    card = card1
    
    if(val1 >= val2 and val1 >= val3):
        print("You should take" + card1)
    elif(val2 >= val1 and val2 >= val3):
        print("You should take" + card2)
        card = card2
    else:
        print("You should take" + card3)
        card = card3
    my_mage_label = tk.Label(textFrame,image =images[card]).grid(row = 0  ,column = 1,sticky='ws',padx=5, pady=5)

   
    
#displays the card involved with the max block and shows the value
def showDef():
    clearAll()

    val = maxDef()
    dmg = tk.Text(textFrame,height=0,width=2)
    dmg.configure(bg='red')
    
    dmg.insert(tk.END,val)
    dmg["state"] =DISABLED
    dmg.grid(row =0, column = 0)
    temp = deck

# while(True):
    
#     print(MaxAtk())
#     print(states)




   # w = Scrollbar(root,orient='vertical')
    

    # card1 = input("Enter Choice 1")
     
    # card2 = input("Enter Choice 2")
    # card3 = input("Enter Choice 3")
    # selection = [card1,card2,card3]
    # val1 = cardStrength[card1][Act-1] + syn(card1)
    # val2 = cardStrength[card2][Act-1] + syn(card2)
    # val3 = cardStrength[card3][Act-1] + syn(card3)
    # showSelection(selection)
    # if(val1 >= val2 and val1 >= val3):
    #     print("You should take" + card1)
    # elif(val2 >= val1 and val2 >= val3):
    #     print("You should take" + card2)
    # else:
    #     print("You should take" + card3)
    
    # card = input("What card did you take?")
    # deck.append(card)

clearAll()
root.mainloop()