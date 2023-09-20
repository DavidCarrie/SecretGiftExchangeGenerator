"""
Generates secret gift exchange assignments from a given csv file, with the 
option to exclude specific assignments with the inclusion of a seperate csv.
Calls GraphApproach to generate assignments.
Formats available in the README

__author__ = "David Carrie" <david.carrie@gmail.com>

"""

import sys
import csv
import GraphApproach

class SecretGift:
    """
    Facilitates secret gift exchange assignments from given participants with
    optional invalid pairings 
    """
    
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
        # Dictionary to store assignments
        self.assignments = {}
        
        
    def generateGiftExchange(self) -> bool:
        """
        Attempts to generate valid scecret gift exchange assignments. Currently
        uses the GraphApproach.

        Returns
        -------
        res: bool
            True if a solution was found, false otherwise
        """
        # Create required class for solution and generate assignments
        seGift = GraphApproach.GraphApproach(self.participants, self.invalid)
        self.assignments = seGift.assignments
        res = seGift.generateExchange()
        
        return res
    
    def notifyGiftors(self,) -> None:
        """
        Notifies participants of their gift assignments

        """    
        for giftor in self.assignments:
            print("Notifying", giftor, \
                  "that they are assigned to get a gift for",\
                    self.participants[self.assignments[giftor]][0],\
                        self.participants[self.assignments[giftor]][1])
            


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
       # Both files names were given, ignores possible extra arguments
       sg = SecretGift(args[1], args[2])
       
    # Generate assignments
    outcome = sg.generateGiftExchange()

    # If generation was succesful notify recipients, otherwise notify user
    # of failure.   
    if outcome:
        print("All gifts assigned")
        sg.notifyGiftors()
    else:
        print("No solution found")

if __name__ == "__main__":
    main()