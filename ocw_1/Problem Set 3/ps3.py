# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Scott Kice
# Collaborators : none
# Time spent    : 

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
SUBSTITUTIONS = 1
REPLAYS = 1

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
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


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).
    
    This version has been modified to replace one of the VOWELS
    with a wildcard character '*'.  The number of total CONSONANTS
    should remain unchanged.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    # ensure every hand has a wildcard '*' 
    hand['*'] = 1
    num_vowels = (int(math.ceil(n / 3))-1)  # reduce the number of VOWELS by 1 to account for the *

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels+1, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
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

#
# Problem #3: Test word validity
#
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
    return valid

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    hand_list = ""
    # iterate through each instance of a letter and create a list (without spaces) for the purpose of measuring the length
    for letter in hand.keys():
        for j in range(hand[letter]):
             hand_list += letter
    return len(hand_list)


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    # Keep track of the total hand score
    hand_score = 0
    
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
        # Display the hand 
        print("Current hand:", end = ' ')
        display_hand(hand)
        
        # Ask user for input
        word = input("Enter word, or \"!!\" ""to indicate that you are finished:")
        
        # If the input is two exclamation points:
        if word == "!!":
            
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not two exclamation points):
        else:     

            # If the word is valid:
            if is_valid_word(word, hand, word_list):
                
                # Tell the user how many points the word earned,
                # and the updated total score
                hand_score += get_word_score(word, calculate_handlen(hand))
                print('"' + word + '"' + " earned " + str(get_word_score(word, calculate_handlen(hand))) + " points. Total: " + str(hand_score) + " points")
                # print a blank line for legibility
                print()
                
            # Otherwise (the word is not valid):
            else:  
                # Reject invalid word (print a message)
                print("That is not a valid word. Please choose another word.")
                # Insert blank line for legibility
                print()
                
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)

    # Game is over (user entered '!!' or ran out of letters), so tell user the total score
    # also, let the user know when the game was ended due to lack of letters in hand
    if calculate_handlen(hand) == 0:
        print("Ran out of letters.")
    
    # Return the total score as result of function
    print("Total score for this hand: " + str(hand_score) + " points")
    
    # print a line of dashes for legibility
    print("----------")
    
    return hand_score
    
    

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provides a letter not in the hand, the hand should remain the same.
    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    # Make a list of available replacement letters. Start with the full lowercase alphabet and
    # eliminate letters which already exist in the hand
    avail_letters = string.ascii_lowercase
    for i in avail_letters:
        if i in hand:
            avail_letters = avail_letters.replace(i, "")
    
    # create a new hand as a copy of the existing hand and then replace the selected letter with a randonly chosen replacement
    new_hand = hand.copy()
    if letter in new_hand:
        new_hand[random.choice(avail_letters)] = new_hand.pop(letter)

    return new_hand
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitute option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    global SUBSTITUTIONS
    global REPLAYS
    
    # Initiate a variable to track the cumulative score across multiple rounds
    cum_score = 0
    
    # Create a dictionary to track scores for each game
    game_scores = {}
    
    # Ask the user how many hands/rounds they wish to play
    # Use error handling to ensure an appropriate response
    while True:
        try:
            num_hands = int(input("Enter total number of hands to play:"))
        except ValueError:
            print("Sorry, I didn't understand that. Please enter an integer value.")
            continue
        else:
            break
            
    # Iterate through the number of hands selected
    game = 1
    while game in range(1, num_hands+1):
    
        # Deal the initial hand
        hand = deal_hand(HAND_SIZE)

        # Display the initial hand
        print("Current hand: ", end = '')
        display_hand(hand)

        # Allow user to elect to substitute a letter assuming they still have valid substitutions remaining
        # if the user enters anything other than "yes" as they were instructed, they will forfeit the opportunity to substitute
        if SUBSTITUTIONS > 0:
            substitution = input("Would you like to substitute a letter? Enter yes or no:")
            if substitution == "yes":
                
                # decrement the global variable SUBSTITUTIONS
                SUBSTITUTIONS -= 1
                
                # solicit the letter to be replaced and substitute the letter in the hand
                sub_letter = input("Which letter would you like to replace?")
                hand = substitute_hand(hand, sub_letter)
        
        # print a blank line for legibility
        print()
        
        # play the hand and receive the hand score as a dictionary value
        game_scores[game] = play_hand(hand, word_list)
        
        # ask user if they wish to replay the hand
        # if the user enters anything other than "yes" as they were instructed, they will forfeit the opportunity to replay
        if REPLAYS > 0:
            replay = input("Would you like to replay the hand? Enter yes or no:")
            if replay == "yes":
                
                # decrement the global variable REPLAYS
                REPLAYS -= 1
                
                # allow the player to play the same hand again for a second score
                second_score = play_hand(hand, word_list)
                
                # if the second score is higher, replace the game score in the game_scores dictionary
                if second_score > game_scores[game]:
                    game_scores[game] = second_score
        
        # increment the game count
        game += 1
    
    # add together the scores from each hand and display the cumulative score
    for score in game_scores:
        cum_score += game_scores[score]
    print("Total score over all hands: " + str(cum_score))
    
#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
