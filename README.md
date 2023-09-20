# SecretGiftExchangeGenerator
Generates assignments for Secret Santa gift exchange




Approach
This script uses a graph based approach to assign giftors to recipients. Giftors
are assigned recipients randomly from a list of viable recipients. If this
assignment leads to an unsolvable situation, backtracking is used to try further
permutations.

1. Each participant has a list of viable gift recipients, created by adding all 
participants then removing themselves and invalid assignments. 
2. The algorithm selects the participant with the least amount of valid 
recipients as giftor to begin assignments.
3. A recipient is chosen at random from the giftors list of viable recipients. 
That recipient is removed from the giftors viable list.
4. The giftor and its viable recipient list are pushed onto stacks, needed in
case backtracking is required.
5. A new giftor is selected by: 
If the recipient of the last gift has already given a gift, then a giftor is 
selected at random from the remaining pool. 
Otherwise the recipient is selected as the next giftor.
6. 3-5 are repeated until all participants have been assigned a giftor resulting
in a valid solution and jumps to (), or the current giftor runs out viable 
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
