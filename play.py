from tictactoe import Game
from agent import Agent
import graph

tests = int(input("Enter a number for number of tests: "))
num_of_iterations = int(input("Enter a number for amount of games to be played: "))
#grapher = Graph()
print("Playing %s games %s times...\n" % (num_of_iterations, tests)) 
for j in range(tests):
	print('Test number: %d\n\n' % (j+1))
	board = Game()
	board.play_agents(False, num_of_iterations)
	#grapher.y1 = board.play_agents(False, num_of_iterations)
	print("_______________________________\n")
	#play without turns
	board = Game()
	board.play_agents(True, num_of_iterations)
	#grapher.y2 = board.play_agents(False, num_of_iterations)
	print("______________________________________________________________\n")
#grapher.graph()