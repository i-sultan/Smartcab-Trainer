import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.possible_actions = ['forward', 'left', 'right', None]
        self.possible_weights = [0, 0, 0, 0]
        self.Qvalues = {}
        self.initialQvalue = 10
        self.Qiterations = {}
		# Constants
        self.alpha = 1 #learning rate, will decrease with iterations
        self.gamma = .1 #discount factor

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (self.next_waypoint, inputs['light'], inputs['oncoming'], inputs['left'], inputs['right'])
        
        # TODO: Select action according to your policy
        #action = random.choice(['forward', 'left', 'right', None])
        #action = self.next_waypoint
        
		# Select policy randomly according to Q value of each action
        for index, action in enumerate(self.possible_actions):
            self.possible_weights[index] = self.Qvalues.setdefault((self.state,action), self.initialQvalue)

        action = self.possible_actions[self.possible_weights.index(max(self.possible_weights))]
        iterations = self.Qiterations.setdefault((self.state,action), 1)
        self.Qiterations[(self.state,action)] += 1

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        # Find s' 
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        self.state_prime = (self.next_waypoint, inputs['light'], inputs['oncoming'], inputs['left'], inputs['right'])

        # Pick max_a' Q[s',a']
        for index, action_prime in enumerate(self.possible_actions):
            self.possible_weights[index] = self.Qvalues.setdefault((self.state_prime,action_prime), self.initialQvalue)
        self.maxQ_new = max(self.possible_weights)

		# Update Q[s,a]
        self.alpha = 1.0/iterations
        self.Qvalues[(self.state,action)] += self.alpha * (reward + self.gamma * self.maxQ_new - self.Qvalues[(self.state,action)])

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

        print "iterations = {}".format(iterations)

        if iterations == 50:
            with open("Qvalues_Log.txt", "w") as text_file:
                for (sa,value) in self.Qiterations.items():
                   text_file.write("sa = {}, value = {}, iteration = {} \n".format(sa, self.Qvalues[sa], value))

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
	
	#e.set_primary_agent(a, enforce_deadline=False)
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=1.0)  # reduce update_delay to speed up simulation
    sim.run(n_trials=10)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
