# SecretGiftExchangeGenerator
Generates assignments for Secret Santa gift exchange. Requires Python 3, a 
participant list in csv, and can accomodate an optional csv to predefine not 
allowed assignments.

How to run:
From a terminal located in the \SecretGiftExchangeGenerator directory run:<br />
Python SecretGift.py [participant.csv] [invalidAssignments.csv] -optional

For example: <br />
Python SecretGift.py test_data_small.csv test_invalidAssignments_small.csv

File Formats: <br />
[participant.csv]: A comma-separated values file with no empty lines. Format is
    First Name,Last Name,Email Address and the first line of the file must 
    reflect this as a header. 

    For example:
        First Name,Last Name,Email Address
        James,Smith,JamesSmith@gmail.com
        Christopher,Anderson,ChristopherAnderson@gmail.com
        Ronald,Clark,RonaldClark@gmail.com
        Mary,Wright,MaryWright@gmail.com
        .....
    
[invalidAssignments.csv]: An optional comma-separated values file with no empty
    lines. Format is Secret Giftor,Recipient and the first line of the file must
    reflect this as a header. Enter the emails of the giftor and recipient
    combination that is not allowed. 

    For example:
        Secret Giftor,Recipient
        JamesSmith@gmail.com,MichelleJohnson@gmail.com
        AnthonyLopez@gmail.com,PatriciaPerez@gmail.com
        CharlesGonzalez@yahoo.com,StevenEvans@yahoo.com
        ...

    Note that these invalid assignments are one directional. To define a pairing
    where neither participant can gift to eachother, make 2 entries.
   
    For example:
        ...
        JamesSmith@gmail.com,MichelleJohnson@gmail.com
        MichelleJohnson@gmail.com,JamesSmith@gmail.com
        ...

Approach:
This script uses a graph based approach to assign giftors to recipients. Giftors
are assigned recipients randomly from a list of viable recipients. If this
assignment leads to an unsolvable situation, backtracking is used to try further
permutations.

1. Each participant has a list of viable gift recipients, created by adding all 
participants then removing themselves and invalid assignments. 
2. The algorithm selects the participant with the least amount of valid 
recipients as the first giftor to begin assignments.
3. A recipient is chosen at random from the giftor's list of viable recipients. 
That recipient is removed from the giftors viable list.
4. The giftor and its viable recipient list are pushed onto stacks, needed in
case backtracking is required.
5. A new giftor is selected by: 
If the recipient of the last gift has already given a gift, then a giftor is 
selected at random from the remaining pool. 
Otherwise the recipient is selected as the next giftor.
6. 3-5 are repeated until all participants have been assigned a giftor resulting
in a valid solution and jump (9), or the current giftor runs out viable 
recipients. 
7. If the current giftor has runs out of viable recipients, the previous giftor
and their untried recipients are popped from the stack and a new permutation is
built by jumping back to 3.
8. If the stack of giftors is empty and the giftor has no remaining possible
recipients, then there is no valid set of assignments for the given participants
and the given constraints.
9. The result of algorithm is displayed to the user, either notifying the 
participants of their assignments or displaying that no valid solution was 
found.
