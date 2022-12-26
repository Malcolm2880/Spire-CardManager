import tkinter as tk
from PIL import ImageTk, Image
from tkinter import Scrollbar, Listbox, Frame,Canvas,Label,ttk,Text,DISABLED,END,NORMAL
import glob

root = tk.Tk()
root.title("test")
# container = ttk.Frame(root)
# canvas = tk.Canvas(container)
# scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
# scrollable_frame = ttk.Frame(canvas)

# scrollable_frame.bind(
#     "<Configure>",
#     lambda e: canvas.configure(
#         scrollregion=canvas.bbox("all")
#     )
# )

# canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
# canvas.configure(yscrollcommand=scrollbar.set)



buttonFrame = Frame(root)
buttonFrame.grid(row=0,column=0,sticky='n')
cardFrame = Frame(root)
cardFrame.grid(row = 0, column = 1, sticky='w')

textFrame = Frame(root)
textFrame.grid(row =1, column = 1,sticky='s')


text= Label(cardFrame)
#myscrollbar=Scrollbar(cardFrame,orient="vertical")
#myscrollbar.grid(row=1,column=0)

#canvas=Canvas(frame)
images = dict({"Strike": 1, "Defend": 2, "Survivor": 3, "Neutrialize": 4}) 

image1 = Image.open("Defend.png")
image1 =  image1.resize((339, 437))

render = ImageTk.PhotoImage(image1)


#my_image_label = tk.Label(image =render).grid(row = 1 ,column = 0)
render2 = ImageTk.PhotoImage(Image.open("Strike.png"))
image2 = Image.open("Strike.png")
image2 =  image2.resize((339, 437))

render2 = ImageTk.PhotoImage(image2)



#my_image_label = tk.Label(image =render2).grid(row = 1 ,column = 1)

image3 = Image.open("Bash.png")
image3 =  image3.resize((339, 437))

render3 = ImageTk.PhotoImage(image3)


image4 = Image.open("Buttons/Deck.png")


render4 = ImageTk.PhotoImage(image4)


red = Image.open("Buttons/Red.png")


render5 = ImageTk.PhotoImage(red)


red = Image.open("Buttons/Blue.png")


render6 = ImageTk.PhotoImage(red)

red = Image.open("Buttons/Green.png")


render7 = ImageTk.PhotoImage(red)

red = Image.open("Buttons/Dexterity.png")
red = red.resize((60,60))

render8 = ImageTk.PhotoImage(red)

red = Image.open("Buttons/Strength.png")
red = red.resize((60,60))

render9 = ImageTk.PhotoImage(red)

#my_image_label = tk.Label(image =render3).grid(row = 1 ,column = 1)


images = dict({"Defend": render, "Strike": render2, "Bash": render3, "Deck" : render4, "Red" : render5, "Blue" : render6, "Green" : render7, "Dex" : render8, "Str" : render9}) 

count=8

allCards =  []


for x in glob.glob("*.png"):
    my_image = Image.open(x)
    my_image = my_image.resize((339, 437))  
    name = x.rsplit('.')[0]
    red = ImageTk.PhotoImage(my_image)
    images[name]=red
    allCards.append(name)

print(images) 




root.geometry('800x800')
def showDmg():
    global cardFrame
    clear()
    val = MaxAtk()
    dmg = tk.Text(textFrame,height=0,width=2)
    
    print(val)
    dmg.grid(row =0, column = 0)
   # dmg["state"]=NORMAL
    dmg.insert(tk.END,val)
    #dmg["state"]=DISABLED
    dmg.grid(row =0, column = 0)
    #temp = deck

def maxDef():
    draw = deck.copy()
    state = []
    man = 0
    vul = 0
    vulMin = 0
    play = list()
    atk = 0
    for x in draw:
        if cards[x][2] > 0:
                play.append(x)
                man = man + cards[x][0]
                print(play)
    diff = man - mana
    play = removeLowestDefs(play,diff)
    print(play)
    clearButtons()
    showCards(play,False)
    return totalDef(play)

def totalDef(deckVar):
    draw = deckVar.copy()
    state = []
    man = 0
    vul = 0
    vulMin = 0
    play = list()
    defe = 0
    for x in draw:
        if cards[x][2] > 0:
                play.append(x)
                man = man + cards[x][0]
                defe = defe + cards[x][2]
    return defe

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
        #print("Target: " + str(target))

        for y in hand:
            hand.remove(y)
            proc = hand.copy()
            target = target - cards[y][0]
           # print("SubTarget: " + str(target))
            temp = removeLowestDefs(proc,target)
            #print(temp)
            if totalDef(temp) > min:
                min = totalDef(temp)
                #print("ret set")
                ret = temp
               # print(ret)
            hand.insert(counter,y)
            counter = counter +1
            target = target + cards[y][0]
        
        
        target = target - cards[name][0]
        
        #print(ret)
        return ret



def MaxAtk():

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

def getOrElse(x, y):
  return x if x is not None else y


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
            #check if applies vul
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

def cost(play):
    val = 0
    for y in play:
        val = val + cards[y][0]
    return val
states = set()
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
        #print("Target: " + str(target))

        for y in hand:
            hand.remove(y)
            proc = hand.copy()
            target = target - cards[y][0]
           # print("SubTarget: " + str(target))
            temp = removeLowestAtks(proc,target)
            #print(temp)
            if totalAtk(temp) > min:
                min = totalAtk(temp)
                #print("ret set")
                ret = temp
               # print(ret)
            hand.insert(counter,y)
            counter = counter +1
            target = target + cards[y][0]
        
        
        target = target - cards[name][0]
        
        #print(ret)
        return ret



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

deck = ["Bash","Strike","Strike","Strike","Strike","Strike","Defend","Defend","Defend","Defend","Defend"]
mana = 3
Act = 1

cards = dict({"Strike": [1,6,0,0],"Defend": [1,0,5,0], 
"Bash" : [2,8,0,.5], "Perfected Strike" : [2,16,0,0], "Dropkick" : [1,5,0,0], "Uppercut" : [2,13,0,.5], 
"Anger" : [0,4,0,0], "Body Slam" : [1,0,0,0], "Clash" : [0,14,0,0], "Cleave" : [1,8,0,0], "Clothesline" : [2,13,0,1], "Headbutt" : [1,8,0,0], 
"Heavy Blade" : [2,12,0,0], "Iron Wave" : [1,5,5,0], "Sword Boomerang" : [1,9,0,0], "Wild Strike" : [1,12,0,0], "SearingBlow" : [2,12,0,0],
"BloodforBlood": [4,18,0,0], "Carnage" : [2,20,0,0],  "Rampage" : [1,8,0,0], "SeverSoul" : [2,16,0,0], "Whirlwind" : [1,5,0,0], "Pummel" : [1,8,0,0],
"Hemokinesis" : [1,15,0,0], "RecklessCharge" : [0,7,0,0], "Feed" : [1,10,0,0], "Reaper" : [1,4,0,0], "FiendFire" : [1,7,0,0], "Bludgeon" : [3,32,0,0],
"Immolate" : [2,21,0,0]})
cardAtk = dict({"Strike": 1, "Defend": 2, "Survivor": 3, "Neutrialize": 4}) 
cardStrength = dict({"Strike": [1,0,0], "Defend": [2,2,2], "Bash": [3,3,3], "Perfected Strike" : [4,3,2], "Dropkick" : [2,3,4], "Uppercut" : [3,4,5]}) 
synergy = dict({"Bash" : [], "Perfected Strike" : ["Strike"], "Dropkick" : ["Bash","Thunderclap","Uppercut"],"Dropkick" : [],"Uppercut" : []})
counterSyn = dict({"Clash" : ["Defend"] })
#works


scrollDist = 0
def clear():
    global cardFrame
    cardFrame.destroy()
    cardFrame = Frame(root)
    cardFrame.grid(row = 0, column = 1, sticky='w')

def clearButtons():
    global buttonFrame
    buttonFrame.destroy()
    buttonFrame = Frame(root)
    buttonFrame.grid(row = 0, column = 0, sticky='n')
    imgBtn = tk.Button(buttonFrame, image=images["Deck"], command=showDeck).grid(row=0,column=0,sticky ='nw')
        
    select1 = tk.Button(buttonFrame, image=images["Red"], command=lambda: showSelection(1)).grid(row=1,column=0,sticky ='s')
    select2 = tk.Button(buttonFrame, image=images["Blue"], command=lambda: showSelection(2)).grid(row=2,column=0,sticky ='s')
    select3 = tk.Button(buttonFrame, image=images["Green"], command=lambda: showSelection(3)).grid(row=3,column=0,sticky ='s')


    Evaluate = tk.Button(buttonFrame ,image=images["Str"], command=showDmg).grid(row=6,column=0,sticky ='s')
    EvaluateDef = tk.Button(buttonFrame ,image=images["Dex"], command=showDef).grid(row=7,column=0,sticky ='s')
    Take =  tk.Button(buttonFrame ,image=images["Red"], command=evaluateSelections).grid(row=8,column=0,sticky ='s')

notDeck = False




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

def showDeck():
    clear()
    clearButtons()
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
        imgBtn = tk.Button(buttonFrame, image=images["Deck"], command=lambda: scrollUp(True,-1)).grid(row=4,column=0,sticky ='s')
    imgBtn = tk.Button(buttonFrame, image=images["Deck"], command=lambda: scrollDown(True,-1)).grid(row=5,column=0,sticky ='s')

def showCards(cards,disable):
    clear()
    clearButtons()
    dc = cards.copy()
    counter = 1
    rows = 0
    total = scrollDist * 10
    size = len(dc) + total
    cardCount = 0
   # mylist = Listbox(frame, yscrollcommand = w.set).grid(row = 2,column=7, sticky = 'ns')
    for d in dc:
       # if cardCount >= total and cardCount <= len(dc) and not disable:
        my_mage_label = tk.Label(cardFrame,image =images[d]).grid(row = rows  ,column = counter,sticky='ws',padx=5, pady=5)
   
        counter = counter +1
        if counter >= 6:
            rows = rows +1
            counter = 1
        cardCount = cardCount + 1
def showSelection(num):
    clear()
    clearButtons()
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
            my_mage_label = tk.Button(cardFrame,image =images[d], command=lambda d = d: selectCard(d,num)).grid(row = rows ,column = counter)
            counter = counter +1
            if counter >= 6:
                rows = rows +1
                counter = 1
        
    if printed >= 10:
        imgBtn = tk.Button(buttonFrame, image=images["Deck"], command=lambda: scrollUp(False,num)).grid(row=4,column=0,sticky ='s')
    imgBtn = tk.Button(buttonFrame, image=images["Deck"], command=lambda: scrollDown(False,num)).grid(row=5,column=0,sticky ='s')

card1=''
card2=''
card3=''
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

def evaluateSelections():
    global card1,card2,card3
    cards = [card1,card2,card3]
    showCards(cards,False)
    val1 = cardStrength[card1][Act-1] + syn(card1)
    val2 = cardStrength[card2][Act-1] + syn(card2)
    val3 = cardStrength[card3][Act-1] + syn(card3)
    #showSelection(selection)
    card = card1
    
    if(val1 >= val2 and val1 >= val3):
        print("You should take" + card1)
    elif(val2 >= val1 and val2 >= val3):
        print("You should take" + card2)
        card = card2
    else:
        print("You should take" + card3)
        card = card3
    choice = tk.Text(textFrame,height=10,width=20)
    choice.insert(tk.END,"You should take" + card)
    choice["state"]=DISABLED
    choice.grid(row=0,column=0)
    




def showDef():
    clear()
    val = maxDef()
    dmg = tk.Text(textFrame,height=0,width=2)
   
    
    dmg.insert(tk.END,val)
    dmg["state"] =DISABLED
    dmg.grid(row =0, column = 0)
    temp = deck

# while(True):
    
#     print(MaxAtk())
#     print(states)
imgBtn = tk.Button(buttonFrame, image=images["Deck"], command=showDeck).grid(row=0,column=0,sticky ='nw')
        
select1 = tk.Button(buttonFrame, image=images["Red"], command=lambda: showSelection(1)).grid(row=1,column=0,sticky ='s')
select2 = tk.Button(buttonFrame, image=images["Blue"], command=lambda: showSelection(2)).grid(row=2,column=0,sticky ='s')
select3 = tk.Button(buttonFrame, image=images["Green"], command=lambda: showSelection(3)).grid(row=3,column=0,sticky ='s')


Evaluate = tk.Button(buttonFrame ,image=images["Str"], command=showDmg).grid(row=6,column=0,sticky ='s')
EvaluateDef = tk.Button(buttonFrame ,image=images["Dex"], command=showDef).grid(row=7,column=0,sticky ='s')



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


root.mainloop()
