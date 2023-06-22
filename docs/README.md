# Milestone III Documentation

## Refactoring and improvements

- Implemented numpy for several evaluation functions
- Replaced deepcopy with pickle to temporarely copy the board
- Fixed wrong check and checkmate moves
- Optimized and removed lots of unnecessary board copies
- Overall cleanup of the code

### Comments
Cleaning up the code helped us a lot with refactoring and some debugging. The cleanup mainly included removing lots of unnecessary comments, code for testing purposes or even code which didn't serve any purpose anymore.

Even though not as much as expected, implementing numpy to cut out many ressource intensive `for` loops in our evaluate function saved quite some time for generating moves.
We achieved this by passing the `board` class into the evaluation function and then converting the board list into a numpy array. This allowed us to remove the `for` loops and replace them with array masks and calculations.

After also replacing `deepcopy` with `pickle`, we were able to almost 20x the speed of our move generation, which was a great achievement. More detailed speed comparisons will be shown later in the documentation. 

After refactoring our `make_move()` function we fixed a lot of illegal moves. Unfortunately, we haven't been able to determine why the engine still generates **197,742/197,281** moves at depth 3. We will hopefully be able to fix this in the last milestone.

We also did some smaller refactoring in the `alphabeta.py` search. This increased the search speed, but didn't have as big of an impact as the move copy refactoring did.

## New implementations

- Move sorting
- Null-move heuristic
- time-management

### Comments
With the implementation of move sorting, we were able to reduce the total tree size when doing the alpha beta search. This slightly improved the search speed and didn't have any impact on the move decision itself.

Adding the null-move heuristic increased the speed quite a lot. Although we had some trouble adding it to the existing code it should now work properly. It would have been easier if we would have used it from the beginning.

We now finally included a working time-management which unfortunately isn't that helpful because our alpha-beta algorithm uses depth first search. When the time limit is reached not all of the first moves in the tree have been evaluated yet.

## Benchmark
