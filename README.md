<h2>
	A reinforcement learning agent that learns to play tic tac toe.
	<br>
	<br>
	Tic Tac Toe has many actions that are equivalent because of the symmetric properties of the board being a square. The actions under consideration require the board to possess one of the following two properties:
	<br>
	<ol>
		<li>
			Board is empty
		</li>
		<li>
			The first action of the first player is in the middle of the board, (1, 1).
		</li>
	</ol>
	<br>
	If one of those properties hold, the following actions in each set are equivalent, as the board can be rotated to achieve any of the other states as a result of any of the equivalent actions:
	<br>
	<ol>
		<li>
			([0, 0], [0, 2], [2, 0], [2, 2])
		</li>
		<li>
			([0, 1], [1, 0], [1, 2], [2, 1])
		</li>
	</ol>
	<br>
	Using this idea we can remove a considerable amount from the state space, and actually limit the first (and potentially the second) set of actions for each player to 3 (and 2 if the first player chose to mark the middle of the board, respectively).
	<br>
	<br>
	The main goal of this was to compare two agents (time of execution, size of state space, win rate, number of draws, etc): one where its state space was not minimized using this idea, and one where its state space was not - to see how impactful this minimization could potentially be on the agent's average reward over time.
	<br>
	<br>
	The following graph is a result of the comparison of the two agents during 1,000,000 games played (Agent 1 using the minimized action space).
	<img src="Avg Reward Over Time.png">
</h2>

<h2>Requirements: (Python 3x)</h2>
<ul>
  <li>
    Numpy 
  </li>
</ul>
