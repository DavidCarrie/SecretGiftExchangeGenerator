"""
Generates secret gift exchange assignments from a given csv file, with the 
option to exclude specific assignments with the inclusion of a seperate csv.
Formats available in the README

__author__ = "David Carrie" <david.carrie@gmail.com>

"""

import sys
import csv
import random

class SecretGift:
    """
    Facilitates secret gift exchange assignments from given participants with
    optional invalid pairings 
    """
    
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

            return False    
           
            
            

    def __init__(self, participantList: str, invalidList: str) ->None:
        """
        Constructs necessary attributes for the Secret Exchange object
        and generates assignments.
        Parameters
        ----------
        participantList : str
            Filename where the participant list can be found.
        invalidList: str 
            Filename where the invalid list can be found.
        """
        # Retrieve participant data from file
        self.participants = self.getParticipantDict(participantList)
        # If invalid list was supplied retrieve data from file
        if (invalidList != ""):
            self.invalid = self.getInvalidAssignments(invalidList)
        else:
            self.invalid = None
        
        # Create required class for solution and generate assignments
        seGift = self.GraphApproach(self.participants, self.invalid)
        res = seGift.generateExchange()
        
        # If generation was succesful notify recipients, otherwise notify user
        # of failure.
        if res:
            print("All gifts assigned")
            self.notifyGiftors(seGift.assignments)
        else:
            print("No solution found")
    
    def notifyGiftors(self, assignments: dict) -> None:
        """
        Notifies participants of their gift assignments

        Parameters
        ----------
        assignments : dict{key: str, value: str}
            Dictionary of gift assignments, key is giftors email and value is
            recipient email.
        
        Returns
        -------
        None
        """    
        for giftor in assignments:
            print("Notifying", giftor, \
                  "that they are assigned to get a gift for",\
                    self.participants[assignments[giftor]][0],\
                        self.participants[assignments[giftor]][1])
            


    def getParticipantDict(self, participantList: str) -> dict:
        """
        Gets secret gift exchange partipant data from csv file and creates a 
        dictionary of particpants

        Parameters
        ----------
        particpantList : str
            string containing the file name of  the csv containing 
            participantList.
        
        Returns
        -------
        pDict: dict {key: str, value: list[str, str]}
            Dictionary of participants, key is participant email and value is
            a list containing participant's first and last name.
        """   
        # Set variables for file loading and participant dictionary
        fName = "./"+participantList
        pDict = {}

        # Open file
        with open(fName, 'r') as file:
            csvr = csv.reader(file)
            headers = next(csvr, 'None')
            # Check for correct headers, report error on invalid format
            correctHeaders = ["First Name", "Last Name", "Email Address"]
            if (headers != correctHeaders):
                print("Incorrect format for participantList",\
                    "see README for more information.")
                exit()
            # Add entries of file into dictionary
            for row in csvr:
                if len(row) != 3:
                    print("Incorrect format for participantList",\
                    "see README for more information.")
                    exit()
                pDict[row[2]] = [row[0], row[1]]
        return pDict

    def getInvalidAssignments(self, invalidList: str) -> list[str, str]:
        """
        Gets secret gift exchange invalid data from csv file and 
        creates list of invalid giftor and recipient pairs.

        Parameters
        ----------
        invalidList : str
            string containing file name of csv containing invalid ordered pairs
        
        Returns
        -------
        invList: list [str, str]
            list of invalid pair for gift exchange, first string entry is the 
            giftor's email the second is the recipient's email.
        """ 

         # Set variables for file loading and invalid ordered pairings list
        fName = "./"+invalidList
        invList = []
        # Open file
        with open(fName, 'r') as file:
            csvr = csv.reader(file)
            headers = next(csvr, 'None')
            # Check for correct headers, report error on invalid format
            correctHeaders = ["Secret Giftor", "Recipient"]
            if (headers != correctHeaders):
                print("Incorrect format for Invalid Assignments",\
                      "see README for more information.")
                exit()
            # Add entries of file into list, checking if entry format
            for row in csvr:
                if len(row) != 2:
                    print("Incorrect format for Invalid Assignments",\
                    "see README for more information.")
                    exit()
                invList.append(row)
        return invList

def main():
    """
        Generates secret santa gift exchange assignments if possible from given
        arguments.

    Arguments
    ---------
    argument [1]: Filename of participant list
    argument [2]: Filename of invalid pairings list (optional)            
    """
    args = sys.argv
    
    if len(args) == 1:
        # No arguments supplied
        print("Error, please specify a file with participants.",\
              "See README for more information.")
    
    if len(args) == 2:
       # No invalid pairings filename given
       sg = SecretGift(args[1], "")
    else: 
       # Both files names were given
       sg = SecretGift(args[1], args[2])

if __name__ == "__main__":
    main()