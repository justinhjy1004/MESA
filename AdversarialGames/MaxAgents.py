from mesa import Agent
import random

class MaxRandomAgent(Agent):
    def __init__(self, id, model):

        ## Apparently this is always needed
        super().__init__(id, model)

        ## Every agent has access to the model, bad design, I know, but I am lazy :( 
        self.model_state = model
        ## Unique ID, based on integer
        self.id = id

        ## This is the list of "others" ID to choose from
        N = self.model_state.num_agents
        others = list(range(0,N))
        others.remove(self.id)
        ## It is the belief that an agent is GOOD
        beliefs = [1] *  (N - 1)
        
        self.belief = dict(zip(others, beliefs))

    ## DO NOT CHANGE
    def select_from_belief(self):

        ## For conversion to a valid probability distribution
        normalizing_constant = sum(list(self.belief.values()))
        
        ## If the agent does not trust anyone, then
        if normalizing_constant == 0:
            ## No one was chosen
            return -1
        
        else:

            ## Tell model that someone is going to be chosen
            self.model_state.chose = True
            selection_probability = [b / normalizing_constant for b in self.belief.values()]
            # Using random.choices() for a single selection
            selected_item = random.choices(list(self.belief.keys()), weights=selection_probability, k=1)[0]

            return selected_item
    
    def choose(self):

        # Implementation of choose action
        if self.model_state.check_whose_turn() == self.id:

            choice = self.select_from_belief()
            self.model_state.chosen.append(choice)
            
        else:
            ## You don't choose
            return

    
    def vote(self):

        current_vote = -1
        
        ## if someone is chosen
        if self.model_state.check_who_was_chosen() != -1:

            ## TODO: Change this
            chooser = self.model_state.check_whose_turn()
            chosen = self.model_state.check_who_was_chosen()

            belief_chooser, belief_chosen = None, None

            ## If you are the chooser
            if chooser == self.id:
                current_vote = 1
            ## If you are the chosen
            elif chosen == self.id:
                current_vote = 1
            ## If you are neither
            else:
                current_vote = 1

        ## if nobody was chosen
        else: 
            
            current_vote = -1

        ## update the model state
        self.model_state.votes_round.append(current_vote)
        
    
    def act(self):
        
        ## what if no one was chosen, then no action
        if self.model_state.check_who_was_chosen() == -1:
            ## then the chooser tosses a coin
            return

        if not self.model_state.check_vote_pass():
            ## then the chooser tosses a coin
            return 

        ## action for chooser 
        if self.id == self.model_state.check_whose_turn():

            action = 1
            self.model_state.action_round[0] = action

        ## action for chosen
        elif self.id == self.model_state.check_who_was_chosen():

            action = 1
            self.model_state.action_round[1] = action

        else:
            ## If I am neither
            return
    
    ## DO NOT CHANGE 
    def outcome(self):
        if self.id == 0:
            self.model_state.outcome_determination()
    ## DO NOT CHANGE

    def update(self):

        current_outcome = self.model_state.check_outcome_current_round()

        if current_outcome == 1:
            return
        else: 
            return
        

class MaxGrimTriggerAgent(Agent):
    def __init__(self, id, model):

        ## Apparently this is always needed
        super().__init__(id, model)

        ## Every agent has access to the model, bad design, I know, but I am lazy :( 
        self.model_state = model
        ## Unique ID, based on integer
        self.id = id

        ## This is the list of "others" ID to choose from
        N = self.model_state.num_agents
        others = list(range(0,N))
        others.remove(self.id)
        ## It is the belief that an agent is GOOD
        beliefs = [1] *  (N - 1)
        
        self.belief = dict(zip(others, beliefs))

    ## DO NOT CHANGE
    def select_from_belief(self):

        ## For conversion to a valid probability distribution
        normalizing_constant = sum(list(self.belief.values()))
        
        ## If the agent does not trust anyone, then
        if normalizing_constant == 0:
            ## No one was chosen
            return -1
        
        else:

            ## Tell model that someone is going to be chosen
            self.model_state.chose = True
            selection_probability = [b / normalizing_constant for b in self.belief.values()]
            # Using random.choices() for a single selection
            selected_item = random.choices(list(self.belief.keys()), weights=selection_probability, k=1)[0]

            return selected_item
    
    def choose(self):

        # Implementation of choose action
        if self.model_state.check_whose_turn() == self.id:

            choice = self.select_from_belief()
            self.model_state.chosen.append(choice)
            
        else:
            ## You don't choose
            return

    
    def vote(self):

        current_vote = -1
        
        ## if someone is chosen
        if self.model_state.check_who_was_chosen() != -1:

            ## TODO: Change this
            chooser = self.model_state.check_whose_turn()
            chosen = self.model_state.check_who_was_chosen()

            ## If you are the chooser
            if chooser == self.id:
                current_vote = 1
            ## If you are the chosen
            elif chosen == self.id:
                if self.belief[chooser] != 1:
                    current_vote = 0
                else:
                    current_vote = 1
            ## If you are neither
            else:
                if self.belief[chooser] != 1:
                    current_vote = 0
                elif self.belief[chosen] != 1:
                    current_vote = 0
                else:
                    current_vote = 1

        ## if nobody was chosen
        else: 
            
            current_vote = -1

        ## update the model state
        self.model_state.votes_round.append(current_vote)
        
    
    def act(self):
        
        ## what if no one was chosen, then no action
        if self.model_state.check_who_was_chosen() == -1:
            ## then the chooser tosses a coin
            return

        if not self.model_state.check_vote_pass():
            ## then the chooser tosses a coin
            return 

        ## action for chooser 
        if self.id == self.model_state.check_whose_turn():

            action = 1
            self.model_state.action_round[0] = action

        ## action for chosen
        elif self.id == self.model_state.check_who_was_chosen():

            action = 1
            self.model_state.action_round[1] = action

        else:
            ## If I am neither
            return

    ## DO NOT CHANGE 
    def outcome(self):
        if self.id == 0:
            self.model_state.outcome_determination()
    ## DO NOT CHANGE

    def update(self):

        current_outcome = self.model_state.check_outcome_current_round()

        if not self.model_state.check_vote_pass():

            return

        if current_outcome == 1:

            return
        
        else: 

            chooser = self.model_state.check_whose_turn()
            chosen  = self.model_state.check_who_was_chosen() 

            if chooser != self.id:
                self.belief[chooser] = 0
            
            if chosen != self.id:
                self.belief[chosen] = 0

            return

