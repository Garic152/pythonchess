#Milestone III Documentation

##Refactoring and improvements

-Implemented numpy for several evaluation functions
-Replaced deepcopy with pickle to temporarely copy the board
-Fixed wrong check and checkmate moves
-Optimized and removed lots of unnecessary board copies
-Overall cleanup of the code

###Comments

Even though not as much as expected, implementing numpy to cut out many ressource intensive for loops in our evaluate function saved quite some time for generating moves.
After also replacing deepcopy with pickle, we were able to almost 20x the speed of our move generation, which was a great achievement.
After refactoring make_move(), we fixed a lot of illegal moves. Unfortunately, we haven't been able to determine why the engine still generates 197,742 out of 197,281 moves at depth 3.
Improving the alphabeta search increased the search speed, but didn't have as big of an impact as the move copy refactoring did.

##New implementations

-Move sorting
-Null-move heuristic
-time-management

