from handEvaluator import *
from pokerUI import *
import variables
import random
import sys
import time

#global variables

image_dir = "Images/"
png = ".png"
pot = 0
game = 1
round = ["Preflop","Flop","Turn","River"]
buy_in = 50
blind = 5

#skip_game variable
skip_game = 0

#variables to handle FOLD case
PLAYER1 = 0
PLAYER2 = 0
BOT = 0

p1_money = p2_money = bot_money = buy_in

deck = cards
popped_cards = []

#setup UI
app = QtGui.QApplication(sys.argv)
# MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow(app)
ui.setupUi(app)
ui.show()

#shuffle cards
def shuffle () :
	random.shuffle(deck)

#skip game ?
def skipGame () :

	global skip_game
	global pot
	global game
	global deck
	global popped_cards

	if([PLAYER1,PLAYER2,BOT].count(2) is 2) :
		if(PLAYER1 is not 2) :
			global p1_money
			p1_money += pot
			pot = 0
		elif(PLAYER2 is not 2) :
			global p2_money
			p2_money += pot
			pot = 0
		else :
			global bot_money
			bot_money += pot
			pot = 0

		ui.p1Money(app,str(p1_money))
		ui.p2Money(app,str(p2_money))
		ui.BotMoney(app,str(bot_money))

		ui.PotMoney(app,str(pot))

		app.processEvents()

		time.sleep(2)

		print "GAME ", game, "IS OVER"
		deck = deck + popped_cards
		game = game + 1
		print len(deck),"**"
		skip_game = 1

	return skip_game

def card_checker(player_cards,community_cards) :

	high_card = highCard(player_cards)

	if royalFlush(player_cards+community_cards) is "yes" :
		return 1,royalFlush(player_cards+community_cards), high_card
	elif len(straightFlush(player_cards+community_cards)) is not 0 :
		print 2,straightFlush(player_cards+community_cards), high_card
	elif len(fourOfAKind(player_cards+community_cards)) is not 0 :
		return 3,fourOfAKind(player_cards+community_cards), high_card
	elif len(fullHouse(player_cards+community_cards)) is not 0:
		return 4,fullHouse(player_cards+community_cards), high_card
	elif len(flush(player_cards+community_cards)) is not 0 :
		return 5,flush(player_cards+community_cards), high_card
	elif len(straight(player_cards+community_cards)) is not 0 :
		return 6,straight(player_cards+community_cards), high_card
	elif len(threeOfAKind(player_cards+community_cards)) is not 0 :
		return 7,threeOfAKind(player_cards+community_cards), high_card
	elif len(twoPair(player_cards+community_cards)) is not 0 :
		return 8,twoPair(player_cards+community_cards), high_card
	elif len(onePair(player_cards+community_cards)) is not 0 :
		return 9,onePair(player_cards+community_cards), high_card
	else :
		return 10,[],high_card


#GAME deciding who won
def winner(player1_cards,player2_cards,bot_cards,community_cards) :
	print "CHECKING WHO WON THE GAME ",game

	#player 1
	best_hand_1 = card_checker(player1_cards,community_cards)[0]
	best_card_1 = card_checker(player1_cards,community_cards)[1]
	high_card_1 = card_checker(player1_cards,community_cards)[2]

	#player 2
	best_hand_2 = card_checker(player2_cards,community_cards)[0]
	best_card_2 = card_checker(player2_cards,community_cards)[1]
	high_card_2 = card_checker(player2_cards,community_cards)[2]

	#bot
	best_hand_3 = card_checker(bot_cards,community_cards)[0]
	best_card_3 = card_checker(bot_cards,community_cards)[1]
	high_card_3 = card_checker(bot_cards,community_cards)[2]

	print PLAYER1, PLAYER2, BOT
	# if(best_hand_1 < best_hand_2 and best_hand_1 < best_hand_3)	q2






#checking what card bot has
def bot(bot_cards,community_cards) :
	print "CHECKING IF BOT HAS SOMETHING"

	best_hand = card_checker(bot_cards,community_cards)[0]
	best_card = card_checker(bot_cards,community_cards)[1]
	high_card = card_checker(bot_cards,community_cards)[2]

	print best_hand, best_card , high_card



#player1 decisions
def player1(round,PLAYER1) :
	value = 0
	print "PLAYER1 is playing" , round
	if round is "Preflop" :
		value = blind
		global p1_money
		p1_money = p1_money - blind
		print p1_money
	elif round is not "Preflop" and PLAYER1 is 2 :
		pass
	elif round is not "Preflop" and PLAYER1 is not 2 :
		#stuff need to be done here
		time.sleep(0.1)
		app.processEvents()
		while(variables.P1CALLCHECK is 0 and variables.P1BETRAISE is 0 and variables.P1FOLD is 0 and variables.STOP is 0) :
			time.sleep(0.1)
			app.processEvents()
		if(variables.STOP is 1) :
			return value,PLAYER1
		if(variables.P1FOLD is 1) :
			PLAYER1 = 2
			variables.P1FOLD = 0
		elif(variables.P1BETRAISE is 1) :
			value = int(ui.player1bet.text())
			print value
			p1_money = p1_money - value
			print p1_money
			variables.P1BETRAISE = 0
		else :
			#take into account the different rounds
			if round is "Flop" :
				value = max(flop) - flop[0]
			elif round is "Turn" :
				value = max(turn) - turn[0]
			else :
				value = max(river) - river[0]
			print value
			p1_money = p1_money - value
			print p1_money
			variables.P1CALLCHECK = 0

	return value,PLAYER1

#player1 decisions
def player2(round,PLAYER2) :
	print "PLAYER2 is playing"
	value = 0
	if PLAYER2 is 2 :
		pass
	else :
		# app.processEvents()';'
		time.sleep(0.1)
		app.processEvents()
		while(variables.P2CALLCHECK is 0 and variables.P2BETRAISE is 0 and variables.P2FOLD is 0 and variables.STOP is 0) :
			time.sleep(0.1)
			app.processEvents()
		if(variables.STOP is 1) :
			return value,PLAYER2
		if(variables.P2FOLD is 1) :
			PLAYER2 = 2
			variables.P2FOLD = 0
		elif(variables.P2BETRAISE is 1) :
			value = int(ui.player2bet.text())
			print value
			global p2_money
			p2_money = p2_money - value
			print p2_money
			variables.P2BETRAISE = 0
		else :
			#take into account the different rounds
			if round is "Preflop" :
				value = max(preflop) - preflop[1]
			elif round is "Flop" :
				value = max(flop) - flop[1]
			elif round is "Turn" :
				value = max(turn) - turn[1]
			else :
				value = max(river) - river[1]
			print value
			p2_money = p2_money - value
			print p2_money
			variables.P2CALLCHECK = 0

	return value,PLAYER2



print "GAME IS GONNA START NOW"

while (variables.STOP is 0) :

	#set initial UI and variables at the start of each game
	round_name = 0        # to update the game round

	skip_game = 0

	PLAYER1 = 0
	PLAYER2 = 0
	BOT = 0

	pot = 0

	bot_cards = []
	player1_cards = []
	player2_cards = []
	community_cards = []

	ui.cc1(app,image_dir+"facedown"+png)
	ui.cc2(app,image_dir+"facedown"+png)
	ui.cc3(app,image_dir+"facedown"+png)
	ui.cc4(app,image_dir+"facedown"+png)
	ui.cc5(app,image_dir+"facedown"+png)
	ui.p1c1(app,image_dir+"facedown"+png)
	ui.p1c2(app,image_dir+"facedown"+png)
	ui.p2c1(app,image_dir+"facedown"+png)
	ui.p2c2(app,image_dir+"facedown"+png)
	ui.bc1(app,image_dir+"facedown"+png)
	ui.bc2(app,image_dir+"facedown"+png)

	ui.p1OptionsHideShow(app,True);
	ui.p2OptionsHideShow(app,False);

	ui.p1Money(app,str(p1_money))
	ui.p2Money(app,str(p2_money))
	ui.BotMoney(app,str(bot_money))

	ui.PotMoney(app,str(pot))

	shuffle()
	popped_cards = []

	ui.GameNumber(app,str(game))
	ui.NameOfRound(app,round[round_name])

	pop = deck.pop()
	popped_cards.append(pop)
	player1_cards.append(pop)
	ui.p1c1(app,image_dir+pop+png)

	pop = deck.pop()
	popped_cards.append(pop)
	player1_cards.append(pop)
	ui.p1c2(app,image_dir+pop+png)

	pop = deck.pop()
	popped_cards.append(pop)
	player2_cards.append(pop)
	ui.p2c1(app,image_dir+pop+png)

	pop = deck.pop()
	popped_cards.append(pop)
	player2_cards.append(pop)
	ui.p2c2(app,image_dir+pop+png)

	pop = deck.pop()
	popped_cards.append(pop)
	bot_cards.append(pop)
	ui.bc1(app,image_dir+pop+png)

	pop = deck.pop()
	popped_cards.append(pop)
	bot_cards.append(pop)
	ui.bc2(app,image_dir+pop+png)

	app.processEvents()

	preflop = [blind,0,0]

	#variables to handle some cases -> one bot folds other bot should know, handling call/check and bet/raise
	flag = 0
	callCheck = -1     #to handle bigger case of call/check and bet/raise...presently it isnt taken into account

	while(True) :

		if(flag == 0) :
			ui.setP1Opt(app,0)

		else :
			ui.setP1Opt(app,1)

		ui.p1OptionsHideShow(app,True)
		ui.p2OptionsHideShow(app,False)

		if(skipGame() is 1) :
			break

		val,PLAYER1 = player1(round[round_name],PLAYER1)

		if(variables.STOP is 1) :
			break

		ui.p1Money(app,str(p1_money))
		ui.player1bet.setText("")

		pot += val
		ui.PotMoney(app,str(pot))

		app.processEvents()

		ui.p1OptionsHideShow(app,False)
		ui.p2OptionsHideShow(app,True)

		if(flag==0) :
			flag = 1
			callCheck = 0

		ui.setP2Opt(app,callCheck)

		app.processEvents()

		if(skipGame() is 1) :
			break

		val,PLAYER2 = player2(round[round_name],PLAYER2)

		if(variables.STOP is 1) :
			break

		preflop[1] = val

		pot += val
		ui.PotMoney(app,str(pot))

		ui.p2Money(app,str(p2_money))
		ui.player2bet.setText("")
		print preflop

		ui.p1OptionsHideShow(app,False)
		ui.p2OptionsHideShow(app,False)

		if(skipGame() is 1) :
			break

		ui.BotPlays(app,"Bot is thinking..")

		app.processEvents()

		time.sleep(3)

		ui.BotPlays(app,"")
		break

		# bot()

	if(variables.STOP is 1) :
		break

	if(skip_game is 1) :
		continue


	round_name = round_name + 1
	ui.NameOfRound(app,round[round_name])

	pop = deck.pop()
	popped_cards.append(pop)
	community_cards.append(pop)
	ui.cc1(app,image_dir+pop+png)

	pop = deck.pop()
	popped_cards.append(pop)
	community_cards.append(pop)
	ui.cc2(app,image_dir+pop+png)

	pop = deck.pop()
	popped_cards.append(pop)
	community_cards.append(pop)
	ui.cc3(app,image_dir+pop+png)

	app.processEvents()

	print PLAYER1 , PLAYER2


	flop = [0]*3

	while(True) :


		ui.setP1Opt(app,1)

		ui.p1OptionsHideShow(app,True)
		ui.p2OptionsHideShow(app,False)

		if(skipGame() is 1) :
			break

		val,PLAYER1 = player1(round[round_name],PLAYER1)

		if(variables.STOP is 1) :
			break

		pot += val
		ui.PotMoney(app,str(pot))

		flop[0] = val

		ui.p1Money(app,str(p1_money))
		ui.player1bet.setText("")

		app.processEvents()

		ui.p1OptionsHideShow(app,False);
		ui.p2OptionsHideShow(app,True);

		ui.setP2Opt(app,1)

		app.processEvents()

		if(skipGame() is 1) :
			break

		val,PLAYER2 = player2(round[round_name],PLAYER2)

		if(variables.STOP is 1) :
			break

		pot += val
		ui.PotMoney(app,str(pot))

		flop[1] = val

		ui.p2Money(app,str(p2_money))
		ui.player2bet.setText("")
		print flop

		ui.p1OptionsHideShow(app,False)
		ui.p2OptionsHideShow(app,False)

		if(skipGame() is 1) :
			break

		ui.BotPlays(app,"Bot is thinking..")

		app.processEvents()

		time.sleep(3)

		bot(bot_cards,community_cards)

		ui.BotPlays(app,"")
		break



	if(variables.STOP is 1) :
		break

	if(skip_game is 1) :
		continue

	#
	#
	round_name = round_name + 1
	ui.NameOfRound(app,round[round_name])

	pop = deck.pop()
	popped_cards.append(pop)
	community_cards.append(pop)
	ui.cc4(app,image_dir+pop+png)

	app.processEvents()

	print PLAYER1 , PLAYER2

	turn = [0]*3
	#
	while(True) :
		ui.setP1Opt(app,1)

		ui.p1OptionsHideShow(app,True)
		ui.p2OptionsHideShow(app,False)

		if(skipGame() is 1) :
			break

		val,PLAYER1 = player1(round[round_name],PLAYER1)

		if(variables.STOP is 1) :
			break

		pot += val
		ui.PotMoney(app,str(pot))

		turn[0] = val

		ui.p1Money(app,str(p1_money))
		ui.player1bet.setText("")

		app.processEvents()

		ui.p1OptionsHideShow(app,False)
		ui.p2OptionsHideShow(app,True)

		ui.setP2Opt(app,1)

		app.processEvents()

		if(skipGame() is 1) :
			break

		val,PLAYER2 = player2(round[round_name],PLAYER2)

		if(variables.STOP is 1) :
			break

		pot += val
		ui.PotMoney(app,str(pot))

		turn[1] = val

		ui.p2Money(app,str(p2_money))
		ui.player2bet.setText("")
		print turn

		ui.p1OptionsHideShow(app,False)
		ui.p2OptionsHideShow(app,False)

		if(skipGame() is 1) :
			break

		ui.BotPlays(app,"Bot is thinking..")

		app.processEvents()

		time.sleep(3)

		bot(bot_cards,community_cards)

		ui.BotPlays(app,"")
		break



	if(variables.STOP is 1) :
		break

	if(skip_game is 1) :
		continue



	print PLAYER1 , PLAYER2
#
	#
	round_name = round_name + 1
	ui.NameOfRound(app,round[round_name])

	pop = deck.pop()
	popped_cards.append(pop)
	community_cards.append(pop)
	ui.cc5(app,image_dir+pop+png)

	app.processEvents()
	#
	river = [0] * 3
	#
	while(True) :
		ui.setP1Opt(app,1)

		ui.p1OptionsHideShow(app,True)
		ui.p2OptionsHideShow(app,False)

		if(skipGame() is 1) :
			break

		val,PLAYER1 = player1(round[round_name],PLAYER1)

		if(variables.STOP is 1) :
			break

		pot += val
		ui.PotMoney(app,str(pot))

		river[0] = val

		ui.p1Money(app,str(p1_money))
		ui.player1bet.setText("")

		app.processEvents()

		ui.p1OptionsHideShow(app,False)
		ui.p2OptionsHideShow(app,True)

		ui.setP2Opt(app,1)

		app.processEvents()

		if(skipGame() is 1) :
			break

		val,PLAYER2 = player2(round[round_name],PLAYER2)

		if(variables.STOP is 1) :
			break

		pot += val
		ui.PotMoney(app,str(pot))

		river[1] = val

		ui.p2Money(app,str(p2_money))
		ui.player2bet.setText("")
		print river

		ui.p1OptionsHideShow(app,False)
		ui.p2OptionsHideShow(app,False)

		if(skipGame() is 1) :
			break

		ui.BotPlays(app,"Bot is thinking..")

		app.processEvents()

		time.sleep(3)

		bot(bot_cards , community_cards)

		ui.BotPlays(app," ")
		break


	if(variables.STOP is 1) :
		break

	if(skip_game is 1) :
		continue
	#
	winner(player1_cards,player2_cards,bot_cards,community_cards)

	app.processEvents()


	time.sleep(2)

	print "GAME ", game, "IS OVER"
	deck = deck + popped_cards
	game = game + 1

print "GAME ENDED BY USER"

if variables.STOP is 1 :
	sys.exit(app.exec_())
