from collections import deque

finalState = "www eee"
initialState = "eee www"
visited = {initialState}

route = []

# generates the next feasible states for the current states.
def getNextState(currentState):
    newStates = []
    blankPosition = currentState.index(' ')

    # Shifting right rabbit ('w') to the left spot
    if blankPosition != len(currentState) - 1:
        temp = currentState.copy()

        if currentState[blankPosition + 1] == 'w':
            # Swapping the things
            temp[blankPosition] = currentState[blankPosition + 1]
            temp[blankPosition + 1] = ' '

            tempString = "".join(temp)

            if not tempString in visited:
                newStates.append(tempString)
                visited.add(tempString)

        # Jumping right rabbit ('w') to the left spot
        if blankPosition != len(currentState) - 2 and currentState[blankPosition + 2] == 'w':
            # Avoiding duplication
            if currentState[blankPosition + 1] != currentState[blankPosition + 2]:
                temp = currentState.copy()
                temp[blankPosition] = currentState[blankPosition + 2]
                temp[blankPosition + 2] = ' '

                tempString = "".join(temp)

                if not tempString in visited:
                    newStates.append(tempString)
                    visited.add(tempString)

    # Shifting left rabbit ('e') to the right spot
    if blankPosition != 0:
        if currentState[blankPosition - 1] == 'e':
            temp = currentState.copy()

            # Swapping the things
            temp[blankPosition] = currentState[blankPosition - 1]
            temp[blankPosition - 1] = ' '

            tempString = "".join(temp)

            if not tempString in visited:
                newStates.append(tempString)
                visited.add(tempString)

        # Jumping left rabbit ('e') to the right spot
        if blankPosition != 1 and currentState[blankPosition - 2] == 'e':
            # Avoiding duplication
            if currentState[blankPosition - 1] != currentState[blankPosition - 2]:
                temp = currentState.copy()
                temp[blankPosition] = currentState[blankPosition - 2]
                temp[blankPosition - 2] = ' '

                tempString = "".join(temp)

                if not tempString in visited:
                    newStates.append(tempString)
                    visited.add(tempString)

    return newStates

def bfs(initialState):
    queue = deque([(initialState, [initialState])])

    while queue:
        currentState, currentRoute = queue.popleft()

        if currentState == finalState:
            return currentRoute

        nextState = getNextState(list(currentState))

        for state in nextState:
            queue.append((state, currentRoute + [state]))

    return None

result = bfs(initialState)

if result:
    for r in result:
        print("[" + r + "]")
else:
    print("Not possible")
