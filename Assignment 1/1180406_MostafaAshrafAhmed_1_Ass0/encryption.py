from typing import List


def check_and_extract_key(message: str, cyphered: str) -> int:
    '''
    This function takes a Message and possible cyphered,
    first check if cyphered is encrypted from  Message, 
    then extract the key used in encryption and return it 
    NOTE KEY MUST BE POSITIVE
    if cyphered is NOT encrypted from  Message return -1
    '''
    key: int
    # TODO: ADD YOUR CODE HERE
    if len(message) != len(cyphered):
        return -1
    message = message.lower()
    cyphered = cyphered.lower()
    key = ord(cyphered[0])-ord(message[0]) if ord(cyphered[0]) >= ord(message[0]
                                                                      ) else 1 + ord(cyphered[0])-ord('a') + ord('z') - ord(message[0])
    for i in range(1, len(message)):
        expectedAscii = ord('a') + (ord(message[i]) + key) % (ord('z')+1) if (
            ord(message[i])+key) > ord('z') else ord(message[i]) + key
        expectedChar = chr(expectedAscii)
        if expectedChar == cyphered[i]:
            continue
        else:
            return -1

    return key
