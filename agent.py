from enum import Enum
import numpy as np
from collections import Counter
import random, sys, time

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