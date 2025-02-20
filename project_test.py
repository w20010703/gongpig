from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify
import random
import json
import os

def get_cards_function(get_cards, player_get_card):

	if get_cards[player_get_card] != []:
		get_num = []
		get_flower = ""
		get_num_flower = get_cards[player_get_card]

		for i in range(len(get_num_flower)):
			if str(get_num_flower[i][1]) == "14":
				get_num_flower[i][1] = "1"

			get_num.append(str(get_num_flower[i][1]))
			get_flower += str(get_num_flower[i][0])

		get_num_card = ",".join(get_num)

	else:
		get_num_card = 0
		get_flower = "nothing"

	return get_num_card, get_flower

def all_players_get_card(get_cards, player):

	players_get_cards = []

	if player == 3:
		players_get_cards.append(get_cards.get("player1_get_cards"))
		players_get_cards.append(get_cards.get("player2_get_cards"))
		players_get_cards.append(get_cards.get("player3_get_cards"))
		
	elif player == 4:
		players_get_cards.append(get_cards.get("player1_get_cards"))
		players_get_cards.append(get_cards.get("player2_get_cards"))
		players_get_cards.append(get_cards.get("player3_get_cards"))
		players_get_cards.append(get_cards.get("player4_get_cards"))

	elif player == 5:
		players_get_cards.append(get_cards.get("player1_get_cards"))
		players_get_cards.append(get_cards.get("player2_get_cards"))
		players_get_cards.append(get_cards.get("player3_get_cards"))
		players_get_cards.append(get_cards.get("player4_get_cards"))
		players_get_cards.append(get_cards.get("player5_get_cards"))

	return players_get_cards

def is_legal(first_card, card_ready_to_play , player_cards ):
    """
    To see if the card the player played is legal.\n
    In the game, if you still have card that share the same suit\n
    with the card the first player played, you shoudn't play the \n
    card with different suit.\n
    \n
    input:\n
    first_card: the card the first player played, ex: ["c",3]\n
    card_ready_to_play: the card the following player want to  play,\n
    ex: ["c",3]\n
    player_cards: the list of cards the following player owns\n 
    \n
    return True or False (legal or ilegal)
    """  

    if first_card[0] == card_ready_to_play[0]:
        return True
    else:
        for i in range(len(player_cards)):
            if player_cards[i][0] == first_card[0]:
                return False
        else:
            return True


def pig_to_sheep_check(players_get_cards):
	for player in players_get_cards:
		heart_count = 0
		for card in player:
			if card[0] == 'h':
				heart_count += 1
		if heart_count == 13:
			return True
	return False

def count_points(get_cards, player_id, player, players_get_cards):

	cards_points = {
	    'h,14' : -50,
	    'h,2' : -2,
	    'h,3' : -3,
	    'h,4' : -10,
	    'h,5' : -5,
	    'h,6' : -6,
	    'h,7' : -7,
	    'h,8' : -8,
	    'h,9' : -9,
	    'h,10' : -10,
	    'h,11' : -20,
	    'h,12' : -30,
	    'h,13' : -40,
	    's,12' : -100,
	    'd,11' : 100,
	}

	player_get_cards = get_cards.get(player_id)


	total_point = 0

	if player_get_cards == []:
		return 0
	if len(player_get_cards) == 16:
		return 1000
	if player_get_cards == [['c',10]]:
		return 50
	if pig_to_sheep_check(players_get_cards) == True:
		cards_points['s,12'] = 100
		cards_points['d,11'] = -100

		heart_count = 0
		for card in player_get_cards:
			if card[0] == 'h':
				heart_count += 1
		if heart_count == 13:
			total_point = 400

		for i in range(len(player_get_cards)):
			player_get_cards[i] = player_get_cards[i][0]+','+str(player_get_cards[i][1])
		if 'c,10' in player_get_cards:
			player_get_cards.remove('c,10')
			for card in player_get_cards:
				total_point += int(cards_points[card])
			return total_point*2
		else: 
			for card in player_get_cards:
				total_point += int(cards_points[card])
			return total_point

	elif pig_to_sheep_check(players_get_cards) == False:
		if player_get_cards == []:
			return 0
		if len(player_get_cards) == 16:
			return 1000
		
		if player_get_cards == [['c',10]]:
			return 50
		
		for i in range(len(player_get_cards)):
			player_get_cards[i] = player_get_cards[i][0]+','+str(player_get_cards[i][1])
		if 'c,10' in player_get_cards:
			player_get_cards.remove('c,10')
			for card in player_get_cards:
				total_point += int(cards_points[card])
			return total_point*2
		else: 
			for card in player_get_cards:
				total_point += int(cards_points[card])
			return total_point

def find_player_id(user_id):
	"""
	find player id
	input: player's order to play card
	output: player id (call dictionary to get their cards)
	"""

	if user_id == 0:
		player_id = "player_1"
	elif user_id == 1:
		player_id = "player_2"
	elif user_id == 2:
		player_id = "player_3"
	elif user_id == 3:
		player_id = "player_4"
	elif user_id == 4:
		player_id = "player_5"

	return player_id

def find_card_num(poker_card_server):
	"""
	find out the number of poker cards
	input: dictionary of the poker cards (to find out how many players are in the game)
	output: the number of cards that the player will get
	"""

	player = len(poker_card_server)

	if player == 4:
		card_num = 17
	elif player == 5:
		card_num = 13
	else:
		card_num = 10

	return card_num

def get_players_id(player, user_id):
	"""
	to get other players id which then can display their cards on the table
	input: the number of players, the user's id
	output: other players id
	"""

	if player == 3:
		if user_id + 2 < player:
			one_id = user_id + 1
			two_id = user_id + 2

		elif user_id + 1 < player:
			one_id = user_id + 1
			two_id = 0

		else:
			one_id = 0
			two_id = 1

		return one_id, two_id

	elif player == 4:
		if user_id + 3 < player:
			one_id = user_id + 1
			three_id = user_id + 2
			two_id = user_id + 3

		elif user_id + 2 < player:
			one_id = user_id + 1
			three_id = user_id + 2
			two_id = 0

		elif user_id + 1 < player:
			one_id = user_id + 1
			three_id = 0
			two_id = 1

		else:
			one_id = 0
			three_id = 1
			two_id = 2

		return one_id, two_id, three_id


	elif player == 5:
		if user_id + 4 < player:
			one_id = user_id + 1
			four_id = user_id +2
			three_id = user_id + 3
			two_id = user_id + 4

		elif user_id + 3 < player:
			one_id = user_id + 1
			four_id = user_id +2
			three_id = user_id + 3
			two_id = 0

		elif user_id + 2 < player:
			one_id = user_id + 1
			four_id = user_id +2
			three_id = 0
			two_id = 1

		elif user_id + 1 < player:
			one_id = user_id + 1
			four_id = 0
			three_id = 1
			two_id = 2

		else:
			one_id = 0
			four_id = 1
			three_id = 2
			two_id = 3

		return one_id, two_id, three_id, four_id

def get_the_card(first_player,cards):
	'''
	After every round, determine which player should get the cards and 
	which cards should be taken (exclude cards that are no scores).

	input : the player who played the first card / 
			the cards played on the table after this round
	'''
	cards_with_score = []
	for i in range(13):
		cards_with_score.append(['h', i+2])
	cards_with_score.append(['s',12])
	cards_with_score.append(['d',11])
	cards_with_score.append(['c',10])

	with open('temp/poker_init.json', 'r') as file:
		poker_card_server = json.load(file)

	if len(cards) == 3:
		player1 = poker_card_server.get("player_1")
		player2 = poker_card_server.get("player_2")
		player3 = poker_card_server.get("player_3")
		player_order = [player1,player2,player3]

	elif len(cards) == 4:
		player1 = poker_card_server.get("player_1")
		player2 = poker_card_server.get("player_2")
		player3 = poker_card_server.get("player_3")
		player4 = poker_card_server.get("player_4")
		player_order = [player1,player2,player3,player4]

	elif len(cards) == 5:
		player1 = poker_card_server.get("player_1")
		player2 = poker_card_server.get("player_2")
		player3 = poker_card_server.get("player_3")
		player4 = poker_card_server.get("player_4")
		player5 = poker_card_server.get("player_5")
		player_order = [player1,player2,player3,player4,player5]

	player_order = player_order[first_player-1:]+player_order[:first_player-1]

	cards_played = []
	for n in range(len(cards)):
		cards_played.append(player_order[n][cards[n]])

	cards_player_gets = []
	max_number = 0
	max_number_player = first_player

	for i in cards_played:
		if i in cards_with_score:
			cards_player_gets.append(i)

		if i[0] == cards_played[0][0]:
			if i[1] > max_number:
				max_number = i[1]
				max_number_player = first_player + cards_played.index(i)

	if max_number_player > len(cards_played):
		max_number_player -= len(cards_played)

	with open('temp/get_cards.json', 'r') as file:
		get_cards = json.load(file)

	if max_number_player == 1:
		get_cards.get("player1_get_cards").extend(cards_player_gets)
	elif max_number_player == 2:
		get_cards.get("player2_get_cards").extend(cards_player_gets)
	elif max_number_player == 3:
		get_cards.get("player3_get_cards").extend(cards_player_gets)
	elif max_number_player == 4:
		get_cards.get("player4_get_cards").extend(cards_player_gets)
	elif max_number_player == 5:
		get_cards.get("player5_get_cards").extend(cards_player_gets)

	with open('temp/get_cards.json', 'w') as file:
		json.dump(get_cards, file)

	return max_number_player

def diliver_cards(player):
	"""
	This is a function to deliver poker cards depending on the number\n
	 of players who play the game.\n
	 input = number of players\n
	If player = 3 , delete club2 from 52 cards\n
	If player = 5 , delete club2 and club3 from 52 cards\n

	club spade heart diamond
	"""
	cards = list()
	for i in range(13):
		cards.append(['c', i+2]) 
	for i in range(13):
		cards.append(['s', i+2]) 
	for i in range(13):
		cards.append(['h', i+2]) 
	for i in range(13):
		cards.append(['d', i+2]) 


	if player == 3:
		del(cards[0])
	elif player == 5:
		del(cards[0])
		del(cards[0])

	random.shuffle(cards)
	if player == 3:
		player1 = []
		player2 = []
		player3 = []
		player1_get_cards = []
		player2_get_cards = []
		player3_get_cards = []
		for i in range(17):
			player1.append(cards.pop(0))
		for i in range(17):
			player2.append(cards.pop(0))
		for i in range(17):
			player3.append(cards.pop(0))
		player_cards = {'player_1' : player1, 'player_2' : player2, 'player_3' : player3}
		return player_cards

	elif player == 4:
		player1 = []
		player2 = []
		player3 = []
		player4 = []
		player1_get_cards = []
		player2_get_cards = []
		player3_get_cards = []
		player4_get_cards = []
		for i in range(13):
			player1.append(cards.pop(0))
		for i in range(13):
			player2.append(cards.pop(0))
		for i in range(13):
			player3.append(cards.pop(0))
		for i in range(13):
			player4.append(cards.pop(0))
		player_cards = {'player_1' : player1, 'player_2' : player2, 'player_3' : player3, 'player_4' : player4}
		return player_cards

	elif player == 5:
		player1 = []
		player2 = []
		player3 = []
		player4 = []
		player5 = []
		player1_get_cards = []
		player2_get_cards = []
		player3_get_cards = []
		player4_get_cards = []
		player5_get_cards = []
		for i in range(10):
			player1.append(cards.pop(0))
		for i in range(10):
			player2.append(cards.pop(0))
		for i in range(10):
			player3.append(cards.pop(0))
		for i in range(10):
			player4.append(cards.pop(0))
		for i in range(10):
			player5.append(cards.pop(0))

		player_cards = {'player_1' : player1, 'player_2' : player2, 'player_3' : player3, 'player_4' : player4, 'player_5' : player5}
		return player_cards






# server
# FLOWERS_FOLDER = os.path.join('static', 'flower')

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = FLOWERS_FOLDER

# @app.route('/')
@app.route('/admin/')
def admin():
	"""
	admin page (go to page => test.html)
	enter your username, password, and the number of players that are going to play the game
	"""
	return render_template("test.html")

@app.route('/admin/', methods=["GET","POST"])
def admin_page():
	"""
	admin page
	shuffle card and init some data

	(if post => go in the function)
	write the data:
	shuffle card and save the poker cards dictionary into this function (this file will not be changed in the game) => poker_init.json
	shuffle card and save the poker cards dictionary into this function => poker.json
	find out how many players already logged in => player_id.json
	cards that played in one round => play_card.json
	save the order of players that played card => players_id.json
	save the cards that players played => players_card.json
	save the cards flower that players played => players_flower.json
	save the cards that each player get => get_cards.json

	(if attempted_username and attempted_password is correct)
	redirect to login page (player.html)
	"""
	error = ''
	try:

		if request.method == "POST":

			attempted_username = request.form['admin_username']
			attempted_password = request.form['admin_password']

			player = request.form['num']

			g_username = attempted_username
			g_password = attempted_password

			poker_card_server = diliver_cards(int(player))

			poker_card_server["player_1"].sort(key = lambda x:(x[0], x[1]))
			poker_card_server["player_2"].sort(key = lambda x:(x[0], x[1]))
			poker_card_server["player_3"].sort(key = lambda x:(x[0], x[1]))

			if player == "4":
				poker_card_server["player_4"].sort(key = lambda x:(x[0], x[1]))

			elif player == "5":
				poker_card_server["player_4"].sort(key = lambda x:(x[0], x[1]))
				poker_card_server["player_5"].sort(key = lambda x:(x[0], x[1]))
				

			poker_card_server["play_card_player_id"] = "0"
			play_card = []
			players_id = []
			players_card =[]
			players_flower = ""
			player_id_name = {}

			with open('temp/poker_init.json', 'w') as file:
				json.dump(poker_card_server, file)

			with open('temp/poker.json', 'w') as file:
				json.dump(poker_card_server, file)

			with open('temp/player_id.json', 'w') as file:
				json.dump(player, file)

			with open('temp/play_card.json', 'w') as file:
				json.dump(play_card, file)

			with open('temp/players_id.json', 'w') as file:
				json.dump(players_id, file)

			with open('temp/players_card.json', 'w') as file:
				json.dump(players_card, file)

			with open('temp/players_flower.json', 'w') as file:
				json.dump(players_flower, file)

			with open('temp/player_id_name.json', 'w') as file:
				json.dump(player_id_name, file)

			get_cards = {}
			total_point = {}

			get_cards["player1_get_cards"] = []
			get_cards["player2_get_cards"] = []
			get_cards["player3_get_cards"] = []
			get_cards["player4_get_cards"] = []
			get_cards["player5_get_cards"] = []

			with open('temp/get_cards.json', 'w') as file:
				json.dump(get_cards, file)

			with open('temp/total_point.json', 'w') as file:
				json.dump(total_point, file)

			if attempted_username == "admin" and attempted_password == "password":
				
				return redirect(url_for('login'))
			else:
				error = "Invalid credentials. Try Again."

		return render_template("test.html", error = error)

	except Exception as e:
		
		return render_template("test.html", error = error)




@app.route('/login/')
def login():
	"""
	login page (go to page => player.html)
	enter your username, password
	"""
	return render_template('player.html')

@app.route('/login/', methods=["GET","POST"])
def login_page():
	"""
	login page
	(if post => go in the function)
	find out the order that you are going to play the card

	(if attempted_username and attempted_password is correct)
	redirect to your own gongpig page (gongpig.html)
	"""
	error = ''
	try:
		
		if request.method == "POST":

			with open('temp/player_id.json', 'r') as file:
				player = int(json.load(file))

			with open('temp/player_id_name.json', 'r') as file:
				player_id_name = json.load(file)

			attempted_username = request.form['username']
			attempted_password = request.form['password']
			g_username = attempted_username
			g_password = attempted_password
			

			if attempted_username == "julia" and attempted_password == "password":

				player -= 1
				player_id_name[player] = attempted_username

				with open('temp/player_id.json', 'w') as file:
					json.dump(player, file)

				with open('temp/player_id_name.json', 'w') as file:
					json.dump(player_id_name, file)

				return redirect(url_for('gongpig', user_id = player))

			elif attempted_username == "sophie" and attempted_password == "password":

				player -= 1
				player_id_name[player] = attempted_username

				with open('temp/player_id.json', 'w') as file:
					json.dump(player, file)

				with open('temp/player_id_name.json', 'w') as file:
					json.dump(player_id_name, file)
				
				return redirect(url_for('gongpig', user_id = player))

			elif attempted_username == "lyc" and attempted_password == "password":

				player -= 1
				player_id_name[player] = attempted_username

				with open('temp/player_id.json', 'w') as file:
					json.dump(player, file)

				with open('temp/player_id_name.json', 'w') as file:
					json.dump(player_id_name, file)
				
				return redirect(url_for('gongpig', user_id = player))

			elif attempted_username == "eva" and attempted_password == "password":

				player -= 1
				player_id_name[player] = attempted_username

				with open('temp/player_id.json', 'w') as file:
					json.dump(player, file)

				with open('temp/player_id_name.json', 'w') as file:
					json.dump(player_id_name, file)
				
				return redirect(url_for('gongpig', user_id = player))

			elif attempted_username == "player_5" and attempted_password == "password":

				player -= 1
				player_id_name[player] = attempted_username

				with open('temp/player_id.json', 'w') as file:
					json.dump(player, file)

				with open('temp/player_id_name.json', 'w') as file:
					json.dump(player_id_name, file)

				return redirect(url_for('gongpig', user_id = player))
				
			else:
				error = "Invalid credentials. Try Again."

		return render_template("player.html", error = error)



	except Exception as e:

		return render_template("player.html", error = error)

@app.route('/gongpig/')
@app.route('/gongpig/<user_id>')
def gongpig(user_id = None):
	"""
	gongpig page
	the page where you play the game
	"""

	# init players id (it is better to give them a meaningless value for init)
	one_id = 404
	four_id = 404
	three_id = 404
	two_id = 404

	#open poker.json to get your poker cards
	with open('temp/poker.json', 'r') as file:
		poker_card_server = json.load(file)

	#open players_id.json to get players_id
	with open('temp/players_id.json', 'r') as file:
		players_id = json.load(file)

	#open players_card.json to get players_card
	with open('temp/players_card.json', 'r') as file:
		players_card = json.load(file)

	#open players_card.json to get players_flower
	with open('temp/players_flower.json', 'r') as file:
		players_flower = json.load(file)

	#open get_cards.json to get get_cards
	with open('temp/get_cards.json', 'r') as file:
		get_cards = json.load(file)


	one_get_num, one_get_flower = get_cards_function(get_cards, "player1_get_cards")
	two_get_num, two_get_flower = get_cards_function(get_cards, "player2_get_cards")
	three_get_num, three_get_flower = get_cards_function(get_cards, "player3_get_cards")
	four_get_num, four_get_flower = get_cards_function(get_cards, "player4_get_cards")
	five_get_num, five_get_flower = get_cards_function(get_cards, "player5_get_cards")

	#find the number of cards
	card_num = find_card_num(poker_card_server)

	#user's id
	user_id = int(user_id)

	#the total number of players in the game
	player = len(poker_card_server) - 1

	#user's player_id
	player_id = find_player_id(user_id)

	#get players id
	other_players_id = get_players_id(player, user_id)

	if player == 3:
		one_id = other_players_id[0]
		two_id = other_players_id[1]
		
	elif player == 4:
		one_id = other_players_id[0]
		two_id = other_players_id[1]
		three_id = other_players_id[2]

	elif player == 5:
		one_id = other_players_id[0]
		two_id = other_players_id[1]
		three_id = other_players_id[2]
		four_id = other_players_id[3]
		
	#take your cards from dictionary
	gongpig_cards = []
	p_cards = []
	p_flowers = []
	gongpig_cards.append(poker_card_server.get(player_id))

	#set num 14 to 1 (since there is no 14 in poker game)
	for i in range(card_num):
		if str(gongpig_cards[0][i][1]) == "14":
			gongpig_cards[0][i][1] = 1

		p_cards.append(str(gongpig_cards[0][i][1]))
		p_flowers.append(str(gongpig_cards[0][i][0]))
		

	#save it as a string so it can be sent to gongpig.html
	variable = ",".join(p_cards)
	flowers = "".join(p_flowers)

	#write the change back into dictionary
	poker_card_server[player_id] = gongpig_cards[0]
	with open('temp/poker.json', 'w') as file:
		json.dump(poker_card_server, file)

	return render_template('gongpig.html', poker_card_server = variable, flowers = json.dumps(flowers), card_num = card_num, player_num = player, player_id = user_id, one_id = one_id, two_id = two_id, three_id = three_id, four_id = four_id, play_card_player_id = poker_card_server.get("play_card_player_id"), players_id = players_id, players_card = players_card, players_flower = json.dumps(players_flower), one_get_num = one_get_num, one_get_flower = json.dumps(one_get_flower), two_get_num = two_get_num, two_get_flower = json.dumps(two_get_flower), three_get_num = three_get_num, three_get_flower = json.dumps(three_get_flower), four_get_num = four_get_num, four_get_flower = json.dumps(four_get_flower), five_get_num = five_get_num, five_get_flower = json.dumps(five_get_flower))


@app.route('/play/', methods=["GET","POST"])
def play():
	"""
	play function (still on gongpig.html):
	(if post)
	get the card that you play and return the next player id
	"""
	error =  ''
	try:
		if request.method == "POST":

			#get the input data from gongpig.html
			value = request.get_json()
			del_num = value.get('num')
			play_card_player_id = value.get('id')
			player = value.get('player')

			#open poker.json to get your poker cards
			with open('temp/poker.json', 'r') as file:
				poker_card_server = json.load(file)

			#open play_card.json to save the card that you played in this round
			with open('temp/play_card.json', 'r') as file:
				play_card = json.load(file)

			#open players_id.json to save the id of the player who just play the card
			with open('temp/players_id.json', 'r') as file:
				players_id = json.load(file)

			#open players_card.json to save the card that the player just played
			with open('temp/players_card.json', 'r') as file:
				players_card = json.load(file)

			#open players_flower.json to save the flower that the player just played
			with open('temp/players_flower.json', 'r') as file:
				players_flower = json.load(file)

			#open get_cards.json to get get_cards
			with open('temp/get_cards.json', 'r') as file:
				get_cards = json.load(file)


			#get your poker cards
			gongpig_cards = []
			player_id = find_player_id(play_card_player_id)
			gongpig_cards.append(poker_card_server.get(player_id))

			#append your id and card to players_id and players_card
			players_id.append(play_card_player_id)
			players_card.append(gongpig_cards[0][int(del_num)][1])
			print(gongpig_cards[0][int(del_num)][1])
			players_flower += gongpig_cards[0][int(del_num)][0]

			#if the number of cards in players_card is more than the card that you will play in a round, init players_id and players_card 
			if len(players_id) == player + 1:
				for i in range(len(players_id) - 1):
					del(players_id[0])
					del(players_card[0])

				players_flower = gongpig_cards[0][int(del_num)][0]
				print(players_card)
			print("test")
			print(players_card)


			#save cards into play_card
			play_card.append(int(del_num))

			#save id of the player who first played the card
			if len(play_card) == 1:

				#after the game started, the file don't have any use, so I reused it to save first player information
				with open('temp/player_id.json', 'r') as file:
					first_player = json.load(file)
				first_card = []
				first_player = play_card_player_id + 1
				first_card.append(gongpig_cards[0][int(del_num)])

				with open('temp/player_id.json', 'w') as file:
					json.dump(first_player, file)

				with open('temp/first_card.json', 'w') as file:
					json.dump(first_card, file)

			with open('temp/player_id.json', 'r') as file:
				first_player = json.load(file)

			with open('temp/first_card.json', 'r') as file:
				first_card = json.load(file)
				
			#after a round, to check who won this round and also to get the next player id
			if len(play_card) == int(player):

				with open('temp/player_id.json', 'r') as file:
					first_player = json.load(file)

				value["id"] = get_the_card(first_player, play_card) - 1
				play_card = []

			else:
				if int(play_card_player_id) + 1 < int(player):
					value["id"] = int(play_card_player_id) + 1

				else:
					value["id"] = 0

			#save the next player id in the dictionary
			poker_card_server["play_card_player_id"] = value["id"]

			#change the card that had been played into zero and it will not be used again
			gongpig_cards[0][int(del_num)][1] = "0"
			poker_card_server[player_id] = gongpig_cards[0]

			#write the data into these files
			with open('temp/poker.json', 'w') as file:
				json.dump(poker_card_server, file)

			with open('temp/play_card.json', 'w') as file:
				json.dump(play_card, file)

			with open('temp/players_id.json', 'w') as file:
				json.dump(players_id, file)

			with open('temp/players_card.json', 'w') as file:
				json.dump(players_card, file)

			with open('temp/players_flower.json', 'w') as file:
				json.dump(players_flower, file)

			return value

	except Exception as e:

		return render_template('gongpig.html', error = error)


@app.route('/end_game/', methods=["GET","POST"])
def end_game():

	#open poker.json to get your poker cards
	with open('temp/poker.json', 'r') as file:
		poker_card_server = json.load(file)

	#open get_cards.json to get get_cards
	with open('temp/get_cards.json', 'r') as file:
		get_cards = json.load(file)

	#find the number of cards
	card_num = find_card_num(poker_card_server)

	#the total number of players in the game
	player = len(poker_card_server) - 1


	n = 0
	while n == 0:

		if player == 3:
		
			for i in range(card_num):
				if poker_card_server["player_1"][i][1] != "0":
					n = 1
					break

				if poker_card_server["player_2"][i][1] != "0":
					n = 1
					break

				if poker_card_server["player_3"][i][1] != "0":
					n = 1
					break

		elif player == 4:
		
			for i in range(card_num):
				if poker_card_server["player_1"][i][1] != "0":
					n = 1
					break

				if poker_card_server["player_2"][i][1] != "0":
					n = 1
					break

				if poker_card_server["player_3"][i][1] != "0":
					n = 1
					break

				if poker_card_server["player_4"][i][1] != "0":
					n = 1
					break

		elif player == 5:
		
			for i in range(card_num):
				if poker_card_server["player_1"][i][1] != "0":
					n = 1
					break

				if poker_card_server["player_2"][i][1] != "0":
					n = 1
					break

				if poker_card_server["player_3"][i][1] != "0":
					n = 1
					break

				if poker_card_server["player_4"][i][1] != "0":
					n = 1
					break

				if poker_card_server["player_5"][i][1] != "0":
					n = 1
					break

		if n == 1:
			return "The game isn't end. Please go to the previous page."

		else:
			with open('temp/total_point.json', 'r') as file:
				total_point = json.load(file)

			with open('temp/player_id_name.json', 'r') as file:
				player_id_name = json.load(file)

			players_get_cards = all_players_get_card(get_cards, player)

			if player == 3:

				total_point["0"] = count_points(get_cards, "player1_get_cards", player, players_get_cards)
				total_point["1"] = count_points(get_cards, "player2_get_cards", player, players_get_cards)
				total_point["2"] = count_points(get_cards, "player3_get_cards", player, players_get_cards)
				n = 1

				return render_template('end_game.html', player_1 = player_id_name["0"], player_1_score = total_point["0"], player_2 = player_id_name["1"], player_2_score = total_point["1"], player_3 = player_id_name["2"], player_3_score = total_point["2"])

			elif player == 4:

				total_point["0"] = count_points(get_cards, "player1_get_cards", player, players_get_cards)
				total_point["1"] = count_points(get_cards, "player2_get_cards", player, players_get_cards)
				total_point["2"] = count_points(get_cards, "player3_get_cards", player, players_get_cards)
				total_point["3"] = count_points(get_cards, "player4_get_cards", player, players_get_cards)
				n = 1

				return render_template('end_game.html', player_1 = player_id_name["0"], player_1_score = total_point["0"], player_2 = player_id_name["1"], player_2_score = total_point["1"], player_3 = player_id_name["2"], player_3_score = total_point["2"], player_4 = player_id_name["3"], player_4_score = total_point["3"])

			elif player == 5:

				total_point["0"] = count_points(get_cards, "player1_get_cards", player)
				total_point["1"] = count_points(get_cards, "player2_get_cards", player)
				total_point["2"] = count_points(get_cards, "player3_get_cards", player)
				total_point["3"] = count_points(get_cards, "player4_get_cards", player)
				total_point["4"] = count_points(get_cards, "player5_get_cards", player)
				n = 1

				return render_template('end_game.html', player_1 = player_id_name["0"], player_1_score = total_point["0"], player_2 = player_id_name["1"], player_2_score = total_point["1"], player_3 = player_id_name["2"], player_3_score = total_point["2"], player_4 = player_id_name["3"], player_4_score = total_point["3"], player_5 = player_id_name["4"], player_5_score = total_point["4"])



	return redirect(url_for('admin'))




if __name__ == '__main__':
	app.debug = True
	app.run(host='192.168.0.12')
	# app.run(debug = True, host = "10.122.213.107")
