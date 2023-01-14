# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        for _ in range(self.iterations):
            update_values_dict = self.values.copy()

            # get Q_values for each possible s_prime
            for state in self.mdp.getStates():
                Q_values = [float('-inf')]
                terminal_state = self.mdp.isTerminal(state)  # boolean

                # Terminal states have 0 value.
                if terminal_state:
                    update_values_dict[state] = 0

                else:
                    legal_actions = self.mdp.getPossibleActions(state)

                    for action in legal_actions:
                        Q_values.append(self.getQValue(state, action))

                    # update value function at state s to largest Q_value
                    update_values_dict[state] = max(Q_values)

            self.values = update_values_dict

        # Write value iteration code here
        "*** YOUR CODE HERE ***"


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        transition_states = self.mdp.getTransitionStatesAndProbs(state, action)  # [(s_prime, prob), ...]
        q_values = []
        for next_state, prob in possible_next_states:
            r = self.mdp.getReward(state, action, next_state)
            gamma = self.discount * self.values[next_state]
            q = prob * (r+gamma)
            q_values.append(q)
        return sum(q_values)

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)

        if len(actions) == 0:
            return None

        actions_qvals = []  # [(action, qval) ... ]

        for action in legal_actions:
            qval = self.getQValue(state, action)
            actions_qvals.append((action, qval))

        action_with_best_qval = max(actions_qvals, key=lambda x: x[1])[0]
        return action_with_best_qval


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
