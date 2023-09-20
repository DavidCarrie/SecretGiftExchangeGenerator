"""
Generates assignments for secret gift exhange using a graph approach, used by
SecretGift.py

__author__ = "David Carrie" <david.carrie@gmail.com>

"""

import random

class GraphApproach:
    """
    Graph based approach for generating secret gift exchange assignments
    """
    def __init__(self, pDict: dict, invList: list) -> None:
        """
        Constructs necessary attributes for the GraphApproach object

        Parameters
        ----------
            pDict : (dict{key:str, value:[str, str]}) 
                Dictionary with the emails of participants as keys and 
                their first and last names as values.
            invList : List[str, str] 
                List of invalid giftor email and recipient email 
                pairings.
        """
        # Create list of emails
        self.emails = list(pDict.keys())
            
        # Initialize dictionary for assignments. Key is string with giftor 
        # email, value is string with recipient email.
        self.assignments = {}

        # List of each participiant indicicating if they have been assigned 
        # a giftor.
        self.hasGift = [False]*len(self.emails)

        # Create list of possible recipients for each participant
        self.adj = []
        for a in range(len(self.emails)):
            self.adj.append([])
            for e in pDict.keys():
                if e != self.emails[a]:
                    self.adj[a].append(e)
            
        # Remove invalid assignments from possible recipients
        if invList != None:
            for entry in invList:
                if entry[0] in self.emails and entry[1] in \
                    self.adj[self.emails.index(entry[0])]:
                    self.adj[self.emails.index(entry[0])].remove(entry[1])


    def generateExchange(self) -> bool:
        """
        Generates giftor and recipient pairings for gift exchange

        Returns
        -------
            bool: True if valid assignments were found with given 
                constaints (optional), False if no solution was found.
        """
        #Initialize stacks for backtracking
        stackGiftors = []
        stackAdj = []

        # Select giftor with fewest amount of possible recepients as first
        # giftor. 
        minLength = len(self.emails)
        ind = -1
        for i in range(len(self.adj)):
            if len(self.adj[i]) < minLength:
                ind = i
                minLength = len(self.adj[i])

        # Push starting giftor to stacks
        stackGiftors.append(ind)
        stackAdj.append(self.adj[ind].copy())
        self.assignments[self.emails[ind]] = ""
            
         # Loop until all permuations have been tried
        while stackGiftors:
                
            # Backtracking/first run retrieve giftor and possible recipients
            giftor = stackGiftors.pop()
            curAdj = stackAdj.pop()

            # Reset recipient status if applicable
            assignment = self.assignments.pop(self.emails[giftor])
            if assignment != "":
                self.hasGift[self.emails.index(assignment)] = False
    
                
            # Loop until all possible recipients have been tried for current
            # giftor.        
            while len(curAdj) > 0:
                # Pick recipient for giftor
                recipient = random.randint(0, len(curAdj)-1)
                # Remove recipient from possible choices of giftor
                recipientNum = self.emails.index(curAdj[recipient])
                curAdj.remove(curAdj[recipient])
                # Push giftor and remaining choices to stack, in case 
                # backtracking is required.
                stackGiftors.append(giftor)
                stackAdj.append(curAdj)
                # Update assignemnts and recipient state
                self.assignments[self.emails[giftor]] \
                    = self.emails[recipientNum]
                self.hasGift[recipientNum] = True

                # If all participants have been assigned a giftor, succesful
                # assignments have been generated.
                if False not in self.hasGift:
                    return True
                    
                    
                # Get next Giftor
                if self.emails[recipientNum] in self.assignments.keys():
                    # If recipient has already given a gift, pick new 
                    # giftor.
                    tmp = []
                    for i in range (len(self.hasGift)):
                        if self.hasGift[i] == False:
                            tmp.append(i)
                    giftor = tmp[random.randint(0, len(tmp)-1)]
                else:
                    # Else new giftor is previous recipient
                    giftor = recipientNum

                # Set choices for giftor's recipient, removing already
                # assigned participants.    
                tmp = []
                for entry in self.adj[giftor]:
                    if self.hasGift[self.emails.index(entry)] == False:
                        tmp.append(entry)
                            
                curAdj = tmp
        # No further valid permutations of assignments to try, no solution found
        return False