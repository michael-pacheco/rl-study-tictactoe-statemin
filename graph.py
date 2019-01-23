import numpy as np
import plotly.plotly as py
import plotly
import plotly.graph_objs as go

#used for avg rwd over time graphing
class Graph():

	y1 = []
	y2 = []
	iterations = 1000000
	def graph(self):
		
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