from enum import Enum
import numpy as np
from collections import Counter
import random, sys, plotly, time

class Game:
	def __init__(self):
		self.board = [
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0]
		]
		self.wins = [0, 0]
		self.draws = 0
		self.moves = 0
		self.turn = False
		self.win = False
		self.starting_actions =  [[2, 0], [2, 1], [1, 1]]

	class Player(Enum):
		ONE = 'X'
		TWO = 'O'
		
	class Reward(Enum):
		MOVE = 1
		FAILED = -5 #a failed move
		WIN = 500
		LOSE = -500
		DRAW = -100
	
	class GameError(Exception):
		pass

	class MoveError(GameError):
		pass
		
	def check_oob(self, coord_1, coord_2):
		if coord_1 >= len(self.board) or coord_1 < 0: 
			raise self.MoveError('First coordinate given is out of bounds. Please retry.')
		elif coord_2 >= len(self.board[0]) or coord_2 < 0:
			raise self.MoveError('Second coordinate given is out of bounds. Please retry.')
	
	def check_occupied(self, coord_1, coord_2):
		if self.board[coord_1][coord_2] != 0:
			raise self.MoveError('Given coordinates are already occupied by a player. Please retry.')
			
	def get_player(self, player):
		if(player==0):
			return self.Player.ONE
		elif(player==1):
			return self.Player.TWO
		else:
			pass
			
	def player_move(self, player, coord_1, coord_2):
		try:
			self.check_oob(coord_1, coord_2)
			self.check_occupied(coord_1, coord_2)
			self.board[coord_1][coord_2] = self.get_player(player).value
		except self.MoveError as ex:
			return 0
		return 1

	def get_board(self):
		return self.board
		
	def print_board(self):
		print(np.array(self.get_board()))
		
	def reset(self):
		self.board = [
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0]
		]
		self.moves = 0
		self.turn = False
		self.win = False
		
	def check_win(self):
		combinations = []
		diag = []
		diag_2 = []
		for i in range(len(self.board)):
			combinations.append(self.board[i]) # all rows
			combinations.append(list(np.transpose(self.board[:])[i])) # all columns
			diag_2.append(self.board[i][np.abs(i-2)]) #top right to bottom left
			diag.append(self.board[i][i]) #top left to botom right
		combinations.append(diag)
		combinations.append(diag_2)
	
		for to_check in combinations:
			if Counter(to_check)['X'] == 3:
				self.wins[0] += 1
				return 0
			elif Counter(to_check)['O'] == 3:
				self.wins[1] += 1
				return 1
			else:
				continue
		return -1
		
	def play_humans(self):
		while not self.win:
			self.print_board()
			print(len(self.get_actions()))
			player = ''
			if self.moves % 2 == 0: #player 1
				player = self.Player.ONE
			else:
				player = self.Player.TWO
			coords = input('Enter coordinates to place your move into (eg 2, 3)')
			coords = [int(coords.split(', ')[0]), int(coords.split(', ')[1])]
			try:
				self.player_move(player, coords[0], coords[1])
			except Exception as ex:
				print(ex)
				continue
			if not self.turn:
				self.flip(coords[0], coords[1])
			self.moves+=1
			if self.check_win() != -1:
				print('Wins: %s' % self.wins)
				print('New game')
				self.reset()
			if self.moves >= 9:
				print('Draw')
				print('New game')
				self.reset()
		self.reset()
		
	def get_actions(self):
		#if both players have acted or board has already turned, return all possible actions, else return starting actions
		if self.moves > 1 or self.turn:
			actions = []
			for i in range(len(self.board)):
				for j in range(len(self.board[i])):
					actions.append([i, j])
		else:
			actions = self.starting_actions
		return actions
		
	def determine_flip(self, coord_1, coord_2):
		#if they didnt choose mid pt and their action was in the starting actions
		if [int(coord_1), int(coord_2)] != [1, 1] and [int(coord_1), int(coord_2)] in self.starting_actions:
			self.turn = True
		
	#return only the possible list of actions (spaces that aren't occupied)
	def get_possible_actions(self):
		actions = []
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j] == 0:
					actions.append([i, j])
		return actions
		
	#return the positions of the board in string format for state
	def get_state(self):
		return ''.join([''.join(str(i) for i in self.board[j]) for j in range(len(self.board))])

	def flip(self, coord_1, coord_2):
		if (coord_1 == 0 and coord_2 == 0) or (coord_1 == 0 and coord_2 == 1):
			self.board = list(np.flipud(np.array(self.board)))
		elif coord_1 == 1 and coord_2 == 0:
			self.board = list(np.rot90(np.array(self.board), 1))
		elif coord_1 == 0 and coord_2 == 2:
			self.board = list(np.rot90(np.array(self.board), 2))
		elif (coord_1 == 2 and coord_2 == 2) or (coord_1 == 1 and coord_2 == 2):
			self.board = list(np.rot90(np.array(self.board), 3))
		self.turn = True
		
	def check_draw(self):
		if self.moves >= 9:
			#print('Draw')
			#self.print_board()
			self.draws += 1
			return 1
		return 0
					
	def play_agents(self, flip_or_not, iterations = None):
		agent_1 = Agent()
		agent_2 = Agent()
		#iterations = 1000000

		start = time.time()
		for i in range(iterations):
			if flip_or_not:
				self.turn = True
			while self.check_win() == -1 and self.check_draw() == 0:
				
				#Player 1
				agent_1_action = agent_1.get_next_action(self)
				previous_state = self.get_state()
				
				#while agent fails to perform a successful move
				while self.player_move(0, int(agent_1_action[0]), int(agent_1_action[1])) == 0:
					agent_1.update_function(self, previous_state, agent_1_action, self.Reward.FAILED.value) #penalize it
					agent_1_action = agent_1.get_next_action(self) #select a new action
				self.moves+=1
				
				#if the board has not turned yet, turn it
				if not self.turn:
					self.determine_flip(int(agent_1_action[0]), int(agent_1_action[1]))
				
				#first check for a win... - only p1 can win here
				if(self.check_win() != -1):
					agent_1.update_function(self, previous_state, agent_1_action, self.Reward.WIN.value)
					self.reset()
					agent_1.update_reward_data(i)
					break
					
				#then check for a draw...
				elif self.check_draw() == 1: 
					agent_1.update_function(self, previous_state, agent_1_action, self.Reward.DRAW.value)
					self.reset()
					agent_1.update_reward_data(i)
					break
				agent_1.update_function(self, previous_state, agent_1_action, 1) #update values in q table
				
				#Player 2
				previous_state = self.get_state() #reset previous_state to the state now - before p2 move for p2
				agent_2_action = agent_2.randomize_action(self)
				while self.player_move(1, int(agent_2_action[0]), int(agent_2_action[1])) == 0: #while it fails...
					agent_2_action = agent_2.randomize_action(self)
					
				self.moves+=1
					
				#if the board has not turned yet, turn it
				if not self.turn:
					self.determine_flip(int(agent_2_action[0]), int(agent_2_action[1]))
				
					
				
				if(self.check_win() != -1): #first check for a win... - only p2 can win here
					agent_1.update_function(self, previous_state, agent_1_action, self.Reward.LOSE.value)
					agent_1.update_reward_data(i)
					self.reset()
					break
				elif self.check_draw() == 1: #then check for a draw...
					agent_1.update_function(self, previous_state, agent_1_action, self.Reward.DRAW.value)
					agent_1.update_reward_data( i)
					self.reset()
					break
			#reduce epsilon/exploration after 500k iteraitons every 15k iterations, and start printing out what iteration its on 
			if i is not 0 and i >= 500000 and i % 15000 == 0 :
				#print(i)
				if agent_1.epsilon > 0.05:
					agent_1.epsilon -= 0.01
			#check for draw/win for P2 in while loop condition
				
		end = time.time()
		print('Time to complete %s iterations: %.2f' % (str(iterations), round(end-start, 2)))
		print('Total wins: %s' % (str(self.wins)))
		print('Win rate excluding draws: %.2f' % (((self.wins[0]/(iterations-self.draws))*100)))
		print('Win rate including draws: %.2f' % (((self.wins[0]/(iterations))*100)))
		print('Size of Q Table: %s' % (len(agent_1.q_table)))
		print('Values for first state: %s' % (agent_1.q_table['000000000']))
		print('Draws: %s' % (str(self.draws)))
		print('Draws: %.2f ' % (((self.draws/iterations)*100)))
		return agent_1.reward_data
		#agent_1.get_avg_reward(iterations)
		
	'''
		Currently unfinished, need to modify the way the dictionary is updated when agent 2 discovers new states - key errors.
	'''
	def play_rl_agents(self, flip_or_not, iterations = None):
		agent_1 = Agent()
		agent_2 = Agent()
		iterations = 1000000 if iterations is None else iterations

		start = time.time()
		for i in range(iterations):
			if flip_or_not:
				self.turn = True
			while self.check_win() == -1 and self.check_draw() == 0:
				
				#Player 1
				agent_1_action = agent_1.get_next_action(self)
				previous_state = self.get_state()
				
				#while agent fails to perform a successful move
				while self.player_move(0, int(agent_1_action[0]), int(agent_1_action[1])) == 0:
					agent_1.update_function_uniq(self, previous_state, agent_1_action, self.Reward.FAILED.value, 1) #penalize it
					agent_1_action = agent_1.get_next_action(self) #select a new action
				self.moves+=1
				
				#if the board has not turned yet, turn it
				if not self.turn:
					self.determine_flip(int(agent_1_action[0]), int(agent_1_action[1]))
				
				#first check for a win... - only P1 can win here
				if(self.check_win() != -1):
					agent_1.update_function_uniq(self, previous_state, agent_1_action, self.Reward.WIN.value, 1)
					agent_2.update_function_uniq(self, previous_state, agent_2_action, self.Reward.LOSE.value, 2)
					
					agent_1.update_reward_data(i)
					agent_2.update_reward_data(i)
					
					self.reset()
					break
					
				#then check for a draw...
				elif self.check_draw() == 1: 
					agent_1.update_function_uniq(self, previous_state, agent_1_action, self.Reward.DRAW.value, 1)
					agent_2.update_function_uniq(self, previous_state, agent_2_action, self.Reward.DRAW.value, 2)
					
					agent_1.update_reward_data(i)
					agent_2.update_reward_data(i)
					
					self.reset()
					break
				agent_1.update_function_uniq(self, previous_state, agent_1_action, self.Reward.MOVE.value, 1) #update values in q table
				
				#Player 2
				agent_2_action = agent_2.get_next_action(self)
				previous_state = self.get_state()
				
				#while agent fails to perform a successful move
				while self.player_move(0, int(agent_2_action[0]), int(agent_2_action[1])) == 0:
					agent_2.update_function_uniq(self, previous_state, agent_2_action, self.Reward.FAILED.value, 2) #penalize it
					agent_2_action = agent_2.get_next_action(self) #select a new action
				self.moves+=1
				
				#if the board has not turned yet, turn it
				if not self.turn:
					self.determine_flip(int(agent_2_action[0]), int(agent_2_action[1]))
				
				#first check for a win... - only P2 can win here
				if(self.check_win() != -1):
					agent_2.update_function_uniq(self, previous_state, agent_2_action, self.Reward.WIN.value, 2)
					agent_1.update_function_uniq(self, previous_state, agent_1_action, self.Reward.LOSE.value, 1)
					
					agent_2.update_reward_data(i)
					agent_1.update_reward_data(i)
					
					self.reset()
					break
					
				#then check for a draw...
				elif self.check_draw() == 1: 
					agent_2.update_function_uniq(self, previous_state, agent_2_action, self.Reward.DRAW.value, 2)
					agent_1.update_function_uniq(self, previous_state, agent_1_action, self.Reward.DRAW.value, 1)
					
					agent_2.update_reward_data(i)
					agent_1.update_reward_data(i)
					
					self.reset()
					break
				agent_2.update_function_uniq(self, previous_state, agent_2_action, self.Reward.MOVE.value, 2) #update values in q table
				

			#reduce epsilon/exploration after x iteraitons every z iterations, and start printing out what iteration its on 
			if i is not 0 and i >= 500000 and i % 15000 == 0 :
				#print(i)
				if agent_1.epsilon > 0.05:
					agent_1.epsilon -= 0.01
				if agent_2.epsilon > 0.05:
					agent_2.epsilon -= 0.01
				
		end = time.time()
		print('Time to complete %s iterations: %.2f' % (str(iterations), round(end-start, 2)))
		print('Total wins: %s' % (str(self.wins)))
		print('Win rate excluding draws: %.2f' % (((self.wins[0]/(iterations-self.draws))*100)))
		print('Win rate including draws: %.2f' % (((self.wins[0]/(iterations))*100)))
		print('Size of Q Table: %s' % (len(agent_1.q_table)))
		print('Values for first state: %s' % (agent_1.q_table['000000000']))
		print('Draws: %s' % (str(self.draws)))
		print('Draws: %.2f ' % (((self.draws/iterations)*100)))
		return agent_1.reward_data
		#agent_1.get_avg_reward(iterations)
		
class Agent():
	def __init__(self):
		self.wins = [0]
		self.q_table = dict()
		self.q_table_2 = dict()
		self.total_rewards = 0
		self.epsilon = 0.25
		self.ALPHA = 0.1
		self.GAMMA = 0.1
		self.reward_data = []
		

	
	def update_reward_data(self, iterations):
		try:
			self.reward_data.append(self.total_rewards/iterations)
		except ZeroDivisionError as ex:
			self.reward_data.append(0)
	
	def update_function(self, game_object, previous_state, action, reward):
		self.total_rewards += reward
		action = str(action[0])+str(action[1])
		current_state = self.get_state(game_object)
		next_optimal_action = self.get_optimal_action(game_object)[0]
		q_table = self.q_table
		
		if current_state not in q_table:
			q_table[current_state] = {}
		if next_optimal_action not in self.q_table[current_state]:
			q_table[current_state][next_optimal_action] = 0
		if action not in self.q_table[current_state]:
			q_table[current_state][action] = 0

		q_table[previous_state][action] = q_table[previous_state][action] + self.ALPHA*(reward + self.GAMMA*(q_table[current_state][next_optimal_action] - q_table[previous_state][action]))
	
	def update_function_uniq(self, game_object, previous_state, action, reward, agent):
		self.total_rewards += reward
		action = str(action[0])+str(action[1])
		current_state = self.get_state(game_object)
		next_optimal_action = self.get_optimal_action(game_object)[0]
		if agent==1:
			q_table = self.q_table
		else:
			q_table = self.q_table_2
		
		if current_state not in q_table:
			q_table[current_state] = {}
		if next_optimal_action not in self.q_table[current_state]:
			q_table[current_state][next_optimal_action] = 0
		if action not in self.q_table[current_state]:
			q_table[current_state][action] = 0

		q_table[previous_state][action] = q_table[previous_state][action] + self.ALPHA*(reward + self.GAMMA*(q_table[current_state][next_optimal_action] - q_table[previous_state][action]))
		
	
	def get_actions(self, game_object):
		return game_object.get_actions()
		
	def get_state(self, game_object):
		return game_object.get_state()
		
	def get_next_action(self, game_object):
		action = None
		randomizer = random.random()
		#print('Randomizer: %s' % (randomizer))
		if randomizer <= self.epsilon:
			#print('Epsilon action')
			action = self.randomize_action(game_object)
		else:
			#print('Optimal action')
			action = self.get_optimal_action(game_object)[0]
		if action is not None:
			return action
		
	def randomize_action(self, game_object):
		current_state = self.get_state(game_object)
		possible_actions = self.get_actions(game_object)
		q_table = self.q_table
		
		random_action = random.choice([x for x in range(len(possible_actions))]) #choose a random index from the list of all actions
		random_action = possible_actions[random_action] #use the random index to retrieve the actual action
		random_action = ''.join([str(coord) for coord in random_action]) #convert to string for qtable access
		
		if current_state not in q_table:
			q_table[current_state] = {}
			q_table[current_state][random_action] = 0
		elif random_action not in q_table[current_state]:
			q_table[current_state][random_action] = 0
			
		return random_action
		
	#get best action from q table in current state
	def get_optimal_action(self, game_object):
		current_state = self.get_state(game_object)
		q_table = self.q_table
		if current_state not in self.q_table:
			q_table[current_state] = {}
			q_table[current_state][self.randomize_action(game_object)] = 0 #get a random action and initialize its return to 0
		optimal_action = sorted(q_table[current_state].items(), key=lambda q_items: q_items[1], reverse=True)[0]
		return optimal_action#return the max value
		
		
	def get_optimal_action_qval(self, game_object):
		optimal_action_value = sorted(self.q_table[self.get_state(game_object)].items(), key=lambda dictValue: dictValue[1])[0]
		return optimal_action_value #return the max value
		
		
	def get_avg_reward(self, iterations):
		import plotly.plotly as py
		import plotly
		import plotly.graph_objs as go
		print(self.total_rewards/iterations)
		line = go.Scatter(
			y=self.reward_data,
			x=[i for i in range(iterations)]
		)
		data =[line]
		plotly.offline.plot(data, filename='Average Reward Over Time.png')
		
'''
#used for avg rwd over time graphing
class Graph():

	y1 = []
	y2 = []
	iterations = 1000000
	def graph(self):
		import plotly.plotly as py
		import plotly
		import plotly.graph_objs as go
		line = go.Scatter(
			y=self.y1,
			x=[i for i in range(self.iterations)],
			name = 'Agent 1',

		)
		line2 = go.Scatter(
			y=self.y2,
			x=[i for i in range(self.iterations)],
			name = 'Agent 2',
		)
		
		data =[line, line2]
		layout= {
			'title': "Average Reward Over Time",
			'xaxis': {
				'title': "Time (s)"
			},
			'yaxis': {
				'title': "Average Reward"
			}
		}
		plotly.offline.plot(data, layout, filename='Average Reward Over Time')
'''
	
tests = int(input("Enter a number for number of tests: "))
num_of_iterations = int(input("Enter a number for amount of games to be played: "))
#grapher = Graph()
print("Playing %s games %s times...\n" % (num_of_iterations, tests)) 
for j in range(tests):
	board = Game()
	board.play_agents(False, num_of_iterations)
	#grapher.y1 = board.play_agents(False, num_of_iterations)
	#play without turns
	board = Game()
	board.play_agents(True, num_of_iterations)
	#grapher.y2 = board.play_agents(False, num_of_iterations)
	print("_______________________________\n")
#grapher.graph()


