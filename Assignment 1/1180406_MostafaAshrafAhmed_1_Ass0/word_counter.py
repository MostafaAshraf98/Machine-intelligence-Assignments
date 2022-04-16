
def count_occurrences(filePath: str, word: str) -> int:
    '''
    This function takes a filePath
    It should return number of occurrences for a given word in this file"  
    '''
    occurrences: int = 0
    # TODO: ADD YOUR CODE HERE
    word = word.lower()

    with open(filePath, 'r') as file:
        # reading each line
        for line in file:

            # reading each word
            for w in line.split():
                w = w.replace(',', '')
                w = w.replace('.', '')

                if word == w.lower():
                    occurrences += 1
                v = w.split('-')
                if len(v) > 1:
                    for w1 in v:
                        if word == w1.lower():
                            occurrences += 1

                v = w.split('/')
                if len(v) > 1:
                    for w1 in v:
                        if word == w1.lower():
                            occurrences += 1

                v = w.split(':')
                if len(v) > 1:
                    for w1 in v:
                        if word == w1.lower():
                            occurrences += 1

    return occurrences
