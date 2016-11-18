1. Ryan Louie and Margo Crawford, Gentrification

2. Gentrification or community transition is a divisive issue in cities across the country. While higher income residents entering a neighborhood can lead to a revitalized economy and more amenities, many are concerned that the original residents don’t reap the benefits, because they are displaced by higher rents. Our project will focus on balancing an increase in creative, knowledge based industry in a city with minimal displacement of long term residents. We will refine and expand on a model of creativity in cities (Ammar Malik et al.) to predict the effects of housing development with subsidized housing on the makeup of a neighborhood being gentrified. 

3. 
	* Ammar Malik et al. Exploring Creativity and Urban Development with Agent-Based Modeling Journal	of Artificial Societies and Social Simulation 18	(2) 12 <http://jasss.soc.surrey.ac.uk/18/2/12.html>

	 For developing cities, attracting creative individuals or those who bring about knowledge-based economies is a highly desired outcome.  An ABM of a city and its citizens is developed. The environment is a 2D grid described by land use, neighborhoods, creative space, and rent. The agents have attributes like income, education, tolerance, and creativity.  They used survey data from a developing city in Pakistan, as well as analysis of overhead map imagery in order to estimate proportions of different attributes in the environment and population. 

	* Torrens, P. M. and Nara, A.  Modeling Gentrification Dynamics: a Hybrid Approach Comput., Environ. and Urban Systems 31 http://www.sciencedirect.com/science/article/pii/S0198971506000718

	 This paper creates a model for cities with both “static” automata, like markets,  and “mobile” automata, like people. It explores the markets over time for different neighborhood makeups. The paper mostly focused on building the model as opposed to producing a lot of results, and there are a lot of parameters, but it is a cool hybrid of cellular automata and multi-agent systems, and their results showed that introducing gentrifiers and gentrifiable properties affects property values more than either in isolation.

	* S. Brown. Beyond Gentrification: Strategies for Guiding the Conversation and Redirecting the Outcomes of Community Transition A paper submitted to Harvard’s Joint Center for Housing Studies and NeighborWorks America July 2014 

	 This paper does not come from the complexity literature.  Its insights comes from case studies and interviews of residents of areas that has experienced community transition: Jamaica Plain in Boston and Columbia Heights in DC. 

4. 
	We originally planned to reproduce the results of the NetLogo model. However, our project has diverged a bit as we are now focusing on the effects of subsidizing on displacement of original residents and creative value of areas, which isn’t covered in that model. We still used it as a reference, but we are measuring different things than they were so we haven’t replicated anything.

	The first experiment that we ran was on the effect of subsidization on rate of displacement of agents. This question shows if our tweaks in the model have a positive effect on low income agents. Since one of our main objectives is to investigate ways to keep low income residents in their homes, this is a vital result. 

	The second experiment was how the level of subsidization effects the displacement of residents. The renters who qualify for subsidized housing pay some fraction of the market value in rent, and we’d like to know how much that percentage can be while still being effective at preventing displacement.

	The third experiment was how subsidization effects the creativity value of cells. In the NetLogo model, we observed a lot of clustering of creative agents in certain cells. Since creative agents earn more, they may live in squares that low creative agents can’t afford. We’d like to know if and how adding subsidized housing changes the distribution of creativity.

5. 
	Question: Does subsidization affect the rate of displacement of original renters? We started by giving some renters 50% subsidization on their housing.

	Methodology: The model takes in an optional input of percentage of agents who get subsidized housing. Then, the lowest income residents are given subsidized housing, which means that they pay a below market rate, 50% of the rate by default. Since agents move when they can't afford rent, we thought there would be less movement when we subsidized more agents. To see the difference, we assigned the subsidized housing percentage to 10%. Two graphs are shown below, both showing displacement over time for cities with and without subsidized housing. They were normalized by subtracting the initial values, because some runs of the model randomly assign more poor agents to high rent patches, so the displacement in the first time step is very high.

	Results: The results graphs are shown below.

	![](imgs/normalized_displacement_1.png) | ![](imgs/normalized_displacement_2.png)

	Interpretation: Results for several trials have not shown a conclusive trend in rate of displacement, although we would need to perform many trials and get quantitative data on the slopes (probably through linear regression) to see if there is a more subtle difference in rates. 

	Question: Does different levels of subsidization affect the outcomes of displacement in neighborhoods?  

	Methodology: We tried by giving renters who get subsidized housing different levels of subsidization. Those agents paid 25, 50, or 75% of the market rate in rent. We then observed the displacement over time.

	Results: The results showed that the model wasn’t very sensitive to the change in subsidisation rate. Shown here are graphs for different random seeds, which show that the slopes are pretty inconclusive. 

	![](imgs/subsidisation_rates.png) | ![](imgs/subsidisation_rates_2.png)
	:--------------------------------:|:-----------------------------------:
	![](imgs/subsidisation_rate_3.png)| ![](imgs/subsidisation_rate_4.png)

	Question: How does subsidization affect the diffusion of creativity in a city?  
	Methodology:  The two settings we compared for subsidization was 0% of the population and 50% of the population being on 50% subsidization on their rent.  For the metric of creavity spread in a city, we used the % of residential cells that are “creative spaces”, defined as having X number of creative agents living in the cell.  

	The city I used was a 10 by 10 grid, with the average rent starting at 12000 currency units and the population of agents totaling 1000.  The number of individuals required to label a cell as creative was just 3.

	Results: Below is several graphs, where a city is initialized with particular agents.  Then the scenario is played through for 50 timesteps. 

	Intepretation: Note that these are across multiple trials.  Since the distribution of agents across the residential cells is random, we can expect the percent of creative space to also be random

	Visually, I might suppose that on average, a unsubidized policy results in a higher increase in % of creative space.  However, over 4 trials, that claim cannot be concluded.

	In addition, the graph for subsidized agents has a smaller variation.  This corresponds to smaller changes in the percent of creative spaces per time step.  This could be correlated to less movement of agents around, which shuffle the distributions of creative people over creative space.

	Question: Do more agents move when there is no subsidized housing?  

	It would make sense, that with subsidization, more agents are happy and are not being displaced by rent hikes.  This would also explain the reduced variation in the percent of creative space graphs, discussed above.

	Results:

	The number of agents moving per timestep, over 50 time steps.  There is intense moving at the beginning, due to the fact that probably many poor agents are initialized in regions where rent is high.  

	In the subsidized case, there is a monotonic trend towards moving less and less.  It approaches a steady steate quickly.

	For unsubidized, however, we can see that movement starts to increase near timestep 15, and continues to increase.  This might relate to creative value and thus rental prices over time, which would make the environment more pressured to move for individuals.

	Interestingly, we can look at both how movement of people are viewed in a city as well as the effect on changes in the percentage of creative space. Below, subsidization provides a benefit in both regards. Again, disclaimer that this is one trial and the numbers are no way indicative of a larger trend.  The sensitvity to randomness is something we aim to fix in the model in order to study these policy decisions better.

	change in % of creative space in unsubsidized city: -1.6 %

	change in % of creative space in 50% subsidized city: 3.0 %










