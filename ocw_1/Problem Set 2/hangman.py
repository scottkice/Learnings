# MIT Course 6.001, Problem Set 2, hangman.py
# Name: Scott Kice
# Collaborators: none

# Hangman Game
# -----------------------------------

import random
import string

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)



# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        match = False
        for character in letters_guessed:
            if letter == character:
                match = True
        if match != True:
            break
    return match



def is_guess_correct(secret_word, guess):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    guess: the user-entered guess
    returns: boolean, True if the user's guess is in the secret word;
      False otherwise
    '''
    match = False
    for letter in secret_word:
        if letter == guess:
            match = True
    return match



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is attempting to guess
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word_chain = ""
    for letter in secret_word:
        match = False
        for character in letters_guessed:
            if letter == character:
                match = True
                word_chain += letter
                break
        if match != True:
            word_chain += "_ "
    # if the last letter has yet to be guessed, strip the trailing space to make it more presentable
    if word_chain[-1] == " ":
        word_chain = word_chain.rstrip(word_chain[-1])
    return word_chain



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ""
    for i in range(26):
        match = False
        for character in letters_guessed:
            if string.ascii_lowercase[i] == character:
                match = True
                break
        if match != True:    
            available_letters += string.ascii_lowercase[i]
    return available_letters



def get_user_guess():
    '''
    function will display the number of guesses remaining, the available letters, and solicit their guess
    determine whether the error checking for the user-entered information should happen in this function or another
    returns: user supplied guess
    '''
    print("You have " + str(num_guesses) + " guesses left.")
    print("Available letters: " + get_available_letters(letters_guessed))
    guess = input("Please guess a letter:")
    return guess



def validate_guess(guess):
    '''
    function will check to confirm that the user-supplied guess is a valid alphabetical character and whether or not the letter
    has already been guessed.  If the guess is not valid, decrement the # of warnings (if there are no warnings remaining, 
    decrement the # of guesses)
    guess: string, the user-supplied guess
    returns: boolean, True if the user supplied guess is an alphabetical character which has not already been guessed; False otherwise
    '''
    valid = True
    
    # check to confirm the user has entered only one character
    if len(guess) > 1:
        print("Valid guesses are only one letter.")
        valid = False
    
    # check to confirm the user has entered a valid alphabetical character
    if not str.isalpha(guess):
        print("Oops! That is not a valid letter.")
        valid = False
    
    # check to see if the entered letter has already been guessed
    match = False
    for letter in letters_guessed:
        if letter == guess:
            match = True
    if match == True:
        valid = False
        print("That letter has already been guessed.")

    # if the guess was not valid, decrement the number of warnings and alert the user
    if not valid:
        global num_warnings
        global num_guesses
        if num_warnings > 0:
            num_warnings -= 1
            print("You have " + str(num_warnings) + " warnings left:" + get_guessed_word(secret_word, letters_guessed))
            print("-------------")

        # if the user is out of warnings, decrement the number of guesses
        else:
            num_guesses -= 1
            print("You are out of warnings and lose 1 guess for the invalid input.")
            
            # check for losing game
            if num_guesses == 0:
                print("Sorry, you ran out of guesses. The word was " + secret_word + ".")
    return valid



# this is the harder version of the game which does not include the option to input * and view the remaining word possibilities
# by choosing which function to call below (hangman or hangman_with_hints), you can select which version is played
def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # make sure the global variables to be used within the function are specified
    global letters_guessed
    global num_guesses
    global correct_guesses
    
    # welcome message for the player
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    print("Guessing an incorrect consonant will cost you one guess.  Guessing an incorrect vowel will cost two guesses.")
    print("-------------")
    
    # comment out the below line once finished testing
    # print(secret_word)
    
    # create a while loop to iterate until the number of guesses has been depleted
    while num_guesses > 0:

        # solicit the user guess
        guess = get_user_guess()
        valid_guess = validate_guess(guess)

        # add the newly guessed letter to the list of guessed letters
        if valid_guess:
            letters_guessed += str.lower(guess)

            if is_guess_correct(secret_word, guess):
                correct_guesses += 1
                print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
                print("------------")

                # check to see if the entire word has been guessed
                if is_word_guessed(secret_word, letters_guessed):
                    print("Congratulations, you won!")
                    print("Your total score for this game is: " + str(correct_guesses*num_guesses))
                    num_guesses = 0

            # handle incorrect guesses and decrement the number of guesses
            else:
                num_guesses -= 1

                # if the incorrect guess was a vowel, decrement the additional guess
                if guess in vowels:
                    num_guesses -= 1

                print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
                print("------------")

                # check for losing game
                if num_guesses == 0:
                    print("Sorry, you ran out of guesses. The word was " + secret_word + ".")    



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    complete_match = True
    trimmed = my_word.replace(" ","")
    if len(trimmed) != len(other_word):
        complete_match = False
        return complete_match
    for char in range(0, len(trimmed)):
        if trimmed[char] != "_":
            if trimmed[char] != other_word[char]:
                complete_match = False
                return complete_match
        else:
            if other_word[char] in trimmed:
                complete_match = False
                return complete_match
    return complete_match



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    print("Possible word matches are: ")
    
    # initialize a counter to track whether any valid matches were found
    count = 0
    
    # go through the wordlist and search for words matching the pattern of my_word
    for i in range(0, len(wordlist)):
        if match_with_gaps(my_word, wordlist[i]):
            count += 1
            print(wordlist[i], end=" ")
    # since the potential matches were all printed on one line, this will ensure the next text printed will start on a new line
    if count > 0:
        print("")
        print("-------------")
    if count == 0:
        print("No matches found")
    return



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    # make sure the global variables to be used within the function are specified
    global letters_guessed
    global num_guesses
    global correct_guesses
    
    # welcome message for the player
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    print("Guessing an incorrect consonant will cost you one guess.  Guessing an incorrect vowel will cost two guesses.")
    print("To view all possible word matches, enter *")
    print("-------------")
    
    # comment out the below line once finished testing
    # print(secret_word)
    
    # create a while loop to iterate until the number of guesses has been depleted
    while num_guesses > 0:

        # solicit the user guess
        guess = get_user_guess()
        
        # check for the asterisk which should show the potential matches for the word
        if guess == "*":
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue

        valid_guess = validate_guess(guess)

        # add the newly guessed letter to the list of guessed letters
        if valid_guess:
            letters_guessed += str.lower(guess)

            if is_guess_correct(secret_word, guess):
                correct_guesses += 1
                print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
                print("------------")

                # check to see if the entire word has been guessed
                if is_word_guessed(secret_word, letters_guessed):
                    print("Congratulations, you won!")
                    print("Your total score for this game is: " + str(correct_guesses*num_guesses))
                    num_guesses = 0

            # handle incorrect guesses and decrement the number of guesses
            else:
                num_guesses -= 1

                # if the incorrect guess was a vowel, decrement the additional guess
                if guess in vowels:
                    num_guesses -= 1

                print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
                print("------------")

                # check for losing game
                if num_guesses == 0:
                    print("Sorry, you ran out of guesses. The word was " + secret_word + ".")    



if __name__ == "__main__":

    # player begins the game with 6 guesses and 3 warnings
    num_guesses = 6
    num_warnings = 3
    
    # initialize a variable to track the guessed letters
    letters_guessed = ""
    
    # variable to count the number of correctly guessed letters for use in scoring 
    # (will be equal to the # of unique letters in the word)
    correct_guesses = 0
    
    # create the list of vowels so incorrectly guessed vowels can be accounted for later
    vowels = ["a", "e", "i", "o", "u"]
    
    # To play the harder version of the game (without hints),
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To play the easier version of the game (with hints),
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
