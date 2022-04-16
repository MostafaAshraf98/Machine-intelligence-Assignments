
def check_bracket_sequence(sequence: str) -> bool:
    '''
    This function takes a sequence of brackets and return true if the sequence can be fixed within at most one step
    and return false otherwise   
    '''
    can_be_fixed: bool
    # TODO: ADD YOUR CODE HERE
    if len(sequence) == 0:
        return True
    if len(sequence) % 2 != 0:
        return False

    numberOfCurrentOpen = 0
    foundClosedWithoutOpen = False
    for bracket in sequence:
        if bracket == '(':
            numberOfCurrentOpen += 1
        else:
            if numberOfCurrentOpen == 0:
                if foundClosedWithoutOpen == True:
                    return False
                else:
                    foundClosedWithoutOpen = True
            else:
                numberOfCurrentOpen -= 1

    if (numberOfCurrentOpen == 1 and foundClosedWithoutOpen == True) or (numberOfCurrentOpen == 0 and foundClosedWithoutOpen == False):
        can_be_fixed = True
    else:
        can_be_fixed = False

    return can_be_fixed
