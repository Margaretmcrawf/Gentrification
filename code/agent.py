"""This is the agent class for our Gentrification/Creativity model."""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import scipy.special as sps

class Agent:

	def __init__(self, education=False):
		"""NetLogo code that determines creativity/income relationship:

		 assign creativity (assume creatives have a little more income, but high creatives have much more)
    	ask n-of (count turtles with [new = 1] / 10)  turtles with [new = 1]   ;; 10% of pop is medium creative people
       		[set creative 1 set creative-m 1 set creative-h 0 set creative-l 0 set income (income * 1.02)]  
    	ask n-of (count turtles with [new = 1] * (%PopHighCreative / 100)) turtles with [new = 1];; user specifies percent high creative - % of high creative assigned below
         	[set creative 1 set creative-h 1 set creative-l 0 set creative-m 0 set income (income * 1.03)]  """

		self.creativity = np.random.choice([1,5,10], p=[0.8, 0.1, 0.1]) # 1 is low, 5 is medium, 10 is high
		self.education = education # is the person educated? May be used to adjust income in future

		#determine initial income, which is a random value in a gamma dist. 
		shape = 5 #centered at 50,000 subject to change
		self.income = round(np.random.gamma(shape)*10000)

		if self.creativity == 5:
			self.income *= 1.1
		elif self.creativity == 10:
			self.income *= 1.5

	def is_satisfied(self, rent):
		# returns whether the agent is satisfied, based on whether it can afford rent,
		#and some other things. Rent is determined by the cell, and is passed in.
		if rent > self.income/4:
			return False
		else:
			return True

a = Agent(education=True)
print(a.creativity)
print(a.income)

