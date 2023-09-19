"""
Generates secret gift exchange assignments from a given csv file, with the option to exclude specific assignments with inclusion of a seperate csv.
Formats available in the README

__author__ = "David Carrie" <david.carrie@gmail.com>

"""

import sys
import csv
import random

class SecretGift:
    
    class DFG:
        def __init__(self, pList, invList):
            self.adj = []
            self.emails = []
            for entry in pList:
                self.adj.append([])
            for i in range(len(self.adj)):
                for j in range(len(self.adj)):
                    self.adj[i].append(pList[j][2])
           
           
            for i in range(len(self.adj)):
                self.adj[i].remove(pList[i][2])
                self.emails.append(pList[i][2])
            
            if invList != None:
                for entry in invList:
                    if entry[0] in self.emails and entry[1] in self.adj[self.emails.index(entry[0])]:
                        self.adj[self.emails.index(entry[0])].remove(entry[1])
            self.assignments = {}
            self.hasGift = [False]*len(self.emails)
            

        def generateExchange(self):
            #Initialize stacks for backtracking
            stackGiftors = []
            stackAdj = []

            #Select giftor with fewest amount of possible recepients 
            minLength = len(self.emails)
            ind = -1
            for i in range(len(self.adj)):
                if len(self.adj[i]) < minLength:
                    ind = i
                    minLength = len(self.adj[i])

            #Push starting giftor to stacks
            stackGiftors.append(ind)
            stackAdj.append(self.adj[ind].copy())
            self.assignments[self.emails[ind]] = ""
            
        
            while stackGiftors:
                
                giftor = stackGiftors.pop()
                curAdj = stackAdj.pop()
                assignment = self.assignments.pop(self.emails[giftor])

                if assignment != "":
                    self.hasGift[self.emails.index(assignment)] = False
    
                
                        
                while len(curAdj) > 0:
                    #Pick recipient for giftor
                    recipient = random.randint(0, len(curAdj)-1)
                    #Remove recipient from possible choices of giftor
                    recipientNum = self.emails.index(curAdj[recipient])
                    curAdj.remove(curAdj[recipient])
                    #Push giftor and remaining choices to stack, in case backtracking is required
                    stackGiftors.append(giftor)
                    stackAdj.append(curAdj)
                    #Update state
                    self.assignments[self.emails[giftor]] = self.emails[recipientNum]
                    self.hasGift[recipientNum] = True
                    if False not in self.hasGift:
                        return True
                    
                    
                    #Get next Giftor
                    if self.emails[recipientNum] in self.assignments.keys():
                        #If recipient has already given a gift, pick new beigging of chain
                        tmp = []
                        for i in range (len(self.hasGift)):
                            if self.hasGift[i] == False:
                                tmp.append(i)
                        giftor = tmp[random.randint(0, len(tmp)-1)]
                    else:
                        #Else new giftor is recipient
                        giftor = recipientNum

                    #Set choices for giftor's recipient    
                    curAdj = self.adj[giftor]
                    tmp = []
                    for entry in curAdj:
                        if self.hasGift[self.emails.index(entry)] == False:
                            tmp.append(entry)
                            
                    curAdj = tmp

            return False    
           
            
            

    def __init__(self, participantList: str, invalidList: str) ->None:
        self.participants = self.getParticipantList(participantList)
        if (invalidList != ""):
            self.invalid = self.getInvalidAssignments(invalidList)
        else:
            self.invalid = None
        self.sortRemoveDups()
        dfg = self.DFG(self.participants, self.invalid)

        res = dfg.generateExchange()

        
        
        if res:
            #All gifts assigned
            #self.notifyGiftors(dfg.assignments)
            print("All gifts assigned")
            print(dfg.assignments)
        else:
            #No solution found
            print("No solution found")
        
        

    def sortRemoveDups(self):
        
        ls = []
        tmp = []
        for entry in self.participants:
            if entry[2] not in tmp:
                tmp.append(entry[2])
                ls.append(entry)
        ls.sort(key = lambda x: x[2])
        self.participants = ls
    
    def notifyGiftors(self, assignments: dict ) -> None:
        for giftor in assignments:
            print("Notifying ", giftor, "that he is assigned to get a gift for ", self.participants[self.emails.index(assignments[giftor])][1], self.participants[self.emails.index(assignments[giftor])][2])


    def getParticipantList(self, participantList: str) -> list[list]:
        fName = "./"+participantList
        pList = []
        with open(fName, 'r') as file:
            csvr = csv.reader(file)
            headers = next(csvr, 'None')
            correctHeaders = ["First Name", "Last Name", "Email Address"]
            if (headers != correctHeaders):
                print("Invalid format for participantList, see README for more information.")
                exit()
            for row in csvr:
                pList.append(row)
        return pList

    def getInvalidAssignments(self, invalidList: str) -> list[list]:
        fName = "./"+invalidList
        invList = []
        with open(fName, 'r') as file:
            csvr = csv.reader(file)
            headers = next(csvr, 'None')
            correctHeaders = ["Secret Giftor", "Recipient"]
            if (headers != correctHeaders):
                print("Invalid format for Invalid Assignments, see README for more information.")
                exit()
            for row in csvr:
                invList.append(row)
        return invList

def main():
    args = sys.argv
    
    
    if len(args) == 1:
        print("Error, please specify a file with participants. See README for more information.")
    if len(args) == 2:
       sg = SecretGift(args[1], "")
    else: 
       sg = SecretGift(args[1], args[2])

if __name__ == "__main__":
    main()