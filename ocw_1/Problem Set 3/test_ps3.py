from ps3 import *

#
# Test code
#

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

def get_word_score(word, n):
    # convert user input to lower case
    word = word.lower()
    
    # handle null inputs
    if len(word) == 0:
        word_score = 0
        return word_score
    
    # the first component is equal to the sum of the individual letter scores
    comp1 = 0
    for letter in word:
        comp1 += SCRABBLE_LETTER_VALUES[letter]
    
    # the second component is equal to the larger of 1, or
    # 7*wordlen - 3*(n-wordlen), 
    # where wordlen is the length of the word and n is the hand length when the word was played
    comp2 = 1
    if (7*(len(word)) - 3*(n-(len(word)))) > 1:
        comp2 = 7*(len(word)) - 3*(n-(len(word)))

    # the total word score is equal to the product of both components
    word_score = comp1 * comp2
    return word_score


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()
    word = word.lower()
    for letter in word:
        # if statement to check if the hand contained the letter to avoid negative values
        if new_hand.get(letter, 0) > 0:
            new_hand[letter] = new_hand.get(letter, 0) - 1  # decrement the key value of the letter
    return new_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    # establish the initial variable values
    valid = False
    in_list = False
    has_letters = True
    
    #convert the word to lower case prior to comparison with wordlist
    word = word.lower()  
    
    # determine if the word contains the * wildcard
    wildcard_location = word.find('*')
    if wildcard_location == -1:  # find() defaults to -1 if the character is not found in the string
        
        # check to determine if the user supplied word is in the list of valid words
        for item in word_list:
            if word == item:
                in_list = True
                continue  # if the word exists in the list, there is no need to keep iterating through the list
    
    # if the wildcard character is in the word, check to see if substituting other vowels in its place
    # results in a valid word
    else:
        for vowel in VOWELS:
            #splice the word up to the wildcard with each vowel and the rtemainder of the word after the wildcard
            wild_word = word[:wildcard_location] + vowel + word[wildcard_location+1:]
            
            #check if new word is in wordlist using same logic as above
            for item in word_list:
                if wild_word == item:
                    in_list = True
                    continue  # if the word exists in the list, there is no need to keep iterating through the list
    
    # convert the user supplied word to a dictionary for comparison purposes with the existing hand
    word_dict = get_frequency_dict(word.lower())
    
    # confirm each letter in the submitted word is available in the player's hand in sufficient quantity
    for letter in word_dict:
        if word_dict.get(letter, 0) > hand.get(letter, 0):
            has_letters = False

    # check to confirm both conditions of a valid word were met:
    # 1)the word was in the list and 2)the hand contained all needed letters
    if in_list and has_letters:
        valid = True
    print(in_list)
    return valid


def test_get_word_score():
    """
    Unit test for get_word_score
    """
    failure=False
    # dictionary of words and scores
    words = {("", 7):0, ("it", 7):2, ("was", 7):54, ("weed", 6):176,
             ("scored", 7):351, ("WaYbILl", 7):735, ("Outgnaw", 7):539,
             ("fork", 7):209, ("FORK", 4):308}
    for (word, n) in words.keys():
        score = get_word_score(word, n)
        if score != words[(word, n)]:
            print("FAILURE: test_get_word_score()")
            print("\tExpected", words[(word, n)], "points but got '" + \
                  str(score) + "' for word '" + word + "', n=" + str(n))
            failure=True
    if not failure:
        print("SUCCESS: test_get_word_score()")

# end of test_get_word_score


def test_update_hand():
    """
    Unit test for update_hand
    """
    # test 1
    handOrig = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
    handCopy = handOrig.copy()
    word = "quail"

    hand2 = update_hand(handCopy, word)
    expected_hand1 = {'l':1, 'm':1}
    expected_hand2 = {'a':0, 'q':0, 'l':1, 'm':1, 'u':0, 'i':0}
    if hand2 != expected_hand1 and hand2 != expected_hand2:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")
        print("\tReturned: ", hand2, "\n\t-- but expected:", expected_hand1, "or", expected_hand2)

        return # exit function
    if handCopy != handOrig:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")
        print("\tOriginal hand was", handOrig)
        print("\tbut implementation of update_hand mutated the original hand!")
        print("\tNow the hand looks like this:", handCopy)
        
        return # exit function
        
    # test 2
    handOrig = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
    handCopy = handOrig.copy()
    word = "Evil"

    hand2 = update_hand(handCopy, word)
    expected_hand1 = {'v':1, 'n':1, 'l':1}
    expected_hand2 = {'e':0, 'v':1, 'n':1, 'i':0, 'l':1}
    if hand2 != expected_hand1 and hand2 != expected_hand2:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")        
        print("\tReturned: ", hand2, "\n\t-- but expected:", expected_hand1, "or", expected_hand2)

        return # exit function

    if handCopy != handOrig:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")
        print("\tOriginal hand was", handOrig)
        print("\tbut implementation of update_hand mutated the original hand!")
        print("\tNow the hand looks like this:", handCopy)
        
        return # exit function

    # test 3
    handOrig = {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    handCopy = handOrig.copy()
    word = "HELLO"

    hand2 = update_hand(handCopy, word)
    expected_hand1 = {}
    expected_hand2 = {'h': 0, 'e': 0, 'l': 0, 'o': 0}
    if hand2 != expected_hand1 and hand2 != expected_hand2:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")                
        print("\tReturned: ", hand2, "\n\t-- but expected:", expected_hand1, "or", expected_hand2)
        
        return # exit function

    if handCopy != handOrig:
        print("FAILURE: test_update_hand('"+ word +"', " + str(handOrig) + ")")
        print("\tOriginal hand was", handOrig)
        print("\tbut implementation of update_hand mutated the original hand!")
        print("\tNow the hand looks like this:", handCopy)
        
        return # exit function

    print("SUCCESS: test_update_hand()")

# end of test_update_hand

def test_is_valid_word(word_list):
    """
    Unit test for is_valid_word
    """
    failure=False
    # test 1
    word = "hello"
    handOrig = get_frequency_dict(word)
    handCopy = handOrig.copy()

    if not is_valid_word(word, handCopy, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected True, but got False for word: '" + word + "' and hand:", handOrig)

        failure = True

    # Test a second time to see if word_list or hand has been modified
    if not is_valid_word(word, handCopy, word_list):
        print("FAILURE: test_is_valid_word()")

        if handCopy != handOrig:
            print("\tTesting word", word, "for a second time - be sure you're not modifying hand.")
            print("\tAt this point, hand ought to be", handOrig, "but it is", handCopy)

        else:
            print("\tTesting word", word, "for a second time - have you modified word_list?")
            wordInWL = word in word_list
            print("The word", word, "should be in word_list - is it?", wordInWL)

        print("\tExpected True, but got False for word: '" + word + "' and hand:", handCopy)

        failure = True


    # test 2
    hand = {'r': 1, 'a': 3, 'p': 2, 'e': 1, 't': 1, 'u':1}
    word = "Rapture"

    if  is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)

        failure = True        

    # test 3
    hand = {'n': 1, 'h': 1, 'o': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
    word = "honey"

    if  not is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected True, but got False for word: '"+ word +"' and hand:", hand)

        failure = True                        

    # test 4
    hand = {'r': 1, 'a': 3, 'p': 2, 't': 1, 'u':2}
    word = "honey"

    if  is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)
        
        failure = True

    # test 5
    hand = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
    word = "EVIL"
    
    if  not is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected True, but got False for word: '" + word + "' and hand:", hand)
        
        failure = True
        
    # test 6
    word = "Even"

    if  is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word()")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)
        print("\t(If this is the only failure, make sure is_valid_word() isn't mutating its inputs)")        
        
        failure = True        

    if not failure:
        print("SUCCESS: test_is_valid_word()")

# end of test_is_valid_word

def test_wildcard(word_list):
    """
    Unit test for is_valid_word
    """
    failure=False

    # test 1
    hand = {'a': 1, 'r': 1, 'e': 1, 'j': 2, 'm': 1, '*': 1}
    word = "e*m"

    if is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word() with wildcards")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)

        failure = True

    # test 2
    hand = {'n': 1, 'h': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
    word = "honey"

    if is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word() with wildcards")
        print("\tExpected False, but got True for word: '"+ word +"' and hand:", hand)

        failure = True

    # test 3
    hand = {'n': 1, 'h': 1, '*': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
    word = "h*ney"

    if not is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word() with wildcards")
        print("\tExpected True, but got False for word: '"+ word +"' and hand:", hand)

        failure = True

    # test 4
    hand = {'c': 1, 'o': 1, '*': 1, 'w': 1, 's':1, 'z':1, 'y': 2}
    word = "c*wz"

    if is_valid_word(word, hand, word_list):
        print("FAILURE: test_is_valid_word() with wildcards")
        print("\tExpected False, but got True for word: '"+ word +"' and hand:", hand)

        failure = True    

    # dictionary of words and scores WITH wildcards
    words = {("h*ney", 7):290, ("c*ws", 6):176, ("wa*ls", 7):203}
    for (word, n) in words.keys():
        score = get_word_score(word, n)
        if score != words[(word, n)]:
            print("FAILURE: test_get_word_score() with wildcards")
            print("\tExpected", words[(word, n)], "points but got '" + \
                  str(score) + "' for word '" + word + "', n=" + str(n))
            failure=True      

    if not failure:
        print("SUCCESS: test_wildcard()")


word_list = load_words()
print("----------------------------------------------------------------------")
print("Testing get_word_score...")
test_get_word_score()
print("----------------------------------------------------------------------")
print("Testing update_hand...")
test_update_hand()
print("----------------------------------------------------------------------")
print("Testing is_valid_word...")
test_is_valid_word(word_list)
print("----------------------------------------------------------------------")
print("Testing wildcards...")
test_wildcard(word_list)
print("All done!")
