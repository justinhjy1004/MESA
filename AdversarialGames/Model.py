from mesa import Model
from mesa.time import StagedActivation
import random
from math import floor
import pandas

## TODO Write custom data collection method

## TODO Custom batch run methods?

"""

df = pd.DataFrame({'Pairs': model.check_historical_choose_chosen_pairs(), 
                   'Voting': model.check_historical_voting_records(),
                   'Outcome': model.check_outcome(),
                   'Action': model.action_record})

"""

## Figure out how to include "Adversarial Team"

class MyModel(Model):
    def __init__(self, N, coin_toss, prop_aversarial, MaxAgent, MinAgent):
        
        super().__init__()

        assert N > 0, "N must be greater than 0."
        self.num_agents = N

        ## Staged activation to determine which round
        ## And whose turn to be the chooser
        self.schedule = StagedActivation(self, stage_list=["choose", "vote", "act", "update"])
        self.round = 0 
        self.whose_turn = self.round % N

        ## if anyone was chosen
        self.chose = False
        ## who is the chosen, and -1 flags is that no one was
        self.chosen = []

        ## voting record of across the rounds
        self.voting_record = []
        ## voting record of the current round
        self.votes_round = []

        ## Action
        self.action_record = []
        self.action_round = [-1,-1]

        ## Outcome 
        self.outcome = []

        ## Coin Toss for failure
        self.coin_toss = coin_toss

        num_min = floor(prop_aversarial * self.num_agents)
        num_max = self.num_agents - num_min

        agents = ([MinAgent] * num_min) + ([MaxAgent] * num_max)
        random.shuffle(agents)

        # Change this up a little
        for i in range(0, self.num_agents):  # Example: creating 10 agents
            self.schedule.add(agents[i](i, self))

        

    ## CONVENION :: check_* are methods for agents to check certain aspects of the model
    
    """
    CHECKING TURNS and CHOOSER-CHOSEN

    These methods concern the first stage of the model
    where the agents choose or are chosen
    """
    def check_whose_turn(self):
        return self.whose_turn
    
    def check_who_was_chosen(self):
        return self.chosen[self.round]
    
    # check all choose chosen pairs
    def check_historical_choose_chosen_pairs(self):
        
        chooser = [ i % self.num_agents for i in list(range(0, self.round)) ]
        chosen = self.chosen

        choose_chosen_pair = list(zip(chooser, chosen))

        return choose_chosen_pair
    
    """
    CHECKING VOTING

    These methods concern information of voting outcomes
    historical and current
    """
    def check_historical_voting_records(self):
        return self.voting_record
    
    def check_current_voting_record(self):
        return self.votes_round
    
    def check_agent_voting_record(self, agent):
        return [ i[agent] for i in self.voting_record ]
    
    def check_vote_pass(self):

        votes = self.votes_round

        if sum(votes)/len(votes) > 0.5:
            return True
        else:
            return False
    
    """
    CHECKING OUTCOME

    These methods concern information of outcomes
    historical and current
    """
    def check_outcome_current_round(self):
        return self.outcome[-1]
    
    def check_outcome(self):
        return self.outcome
        
    def toss_coin(self):
        # Using random.choices() for a single selection
        toss = random.choices([0,1], weights=[self.coin_toss, 1 - self.coin_toss], k=1)[0]
        return toss
    
    """
    DETERMINE OUTCOME

    Determine Outcomes from Actions
    """
    def outcome_determination(self):
        ## determine which team won in given round
        ## 1 = Good team wins, 0 = Bad team wins
        if self.action_round[0] == 1 and self.action_round[1] == 1:
            self.outcome.append(1)
        elif self.action_round[0] == -1 and self.action_round[1] == -1:
            self.outcome.append(self.toss_coin())
        else:
            self.outcome.append(0)

   
    def step(self):
        self.schedule.step()
        self.round += 1
        
        ## Reset Parameters
        self.whose_turn = self.round % self.num_agents
        self.chose = False
        self.voting_record.append(self.votes_round)
        self.votes_round = []
        self.action_record.append(self.action_round)
        self.action_round = [-1,-1]

