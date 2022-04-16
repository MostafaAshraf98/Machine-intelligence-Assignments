def count_duplicates(text: str) -> list(tuple((str, int))):
    '''
    This function takes a text then detects duplicates and  
    it should ONLY return duplicates and their number of occurencesses in the form of list if tuples 
    '''
    output: list(tuple((str, int))) = []
    # TODO: ADD YOUR CODE HERE
    d = dict()
    for letter in text:
        letter = letter.lower()
        if d.get(letter, 'default') == 'default':  # If this letter does not occur before
            d[letter] = 1
        else:
            d[letter] += 1

    for key, value in d.items():
        if value != 1:
            output.append((key, value))

    return output
