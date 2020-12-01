import os
from time import sleep
import random

# service of game's progress and its display    
    
def progress_service(word, guessed_letters):
    return [letter if (str.lower(letter) in guessed_letters or letter == " ")  else "_" for letter in word]



def progress_display(progress):
    return " ".join(progress)


def used_letters_display(guessed_set, missed_set):
    return " ".join(guessed_set | missed_set)


# service of getting user's input and its validation

def input_validate(user_input):
    return (str.isalpha(user_input) and len(user_input) == 1)

def user_guess(user_input):
    return check_guess(user_input) if input_validate(user_input) == True else user_guess(input("Please, provide one of latin alphabet letters: "))

    if input_validate(user_input) == True:
        return check_guess(user_input)
    else:
        user_guess(input("Please, provide one of latin alphabet letters: "))

# control of user's answer

def check_guess(user_input):
    if user_input in already_guessed_letters | already_tryed_letters: return repeat_service()
    
    elif user_input not in word_to_guess: return failure_service(user_input)
    
    else: success_service(user_input)


# Responds for user's shots

def repeat_service():
    
    clear()
    print(f"You've tryed this one already. Try letter other from those:\n{used_letters_display(already_tryed_letters, already_guessed_letters)}\n")
    sleep(2)

    return None

def failure_service(user_input):
    already_tryed_letters.add(user_input)
    
    global lives 
    lives -= 1
    
    clear()
    print("This one is not in word")
    print(f"\nAlready used letters: \n{used_letters_display(already_tryed_letters, already_guessed_letters)}\n")
    sleep(2)

    return False

def success_service(user_input):
    already_guessed_letters.add(user_input)
    
    clear()
    print("Good shot!")
    sleep(2)

    return True

def win_execution(answer):
    print(f"Congratulations, you guessed the answer, which is: {answer}")



# service of hangman's ascii graphics; its, and game's display

def load_hangman_graphic():
    hangman_file = open("hangman_ascii.txt", "r")
    content = eval(hangman_file.read())
    hangman_file.close()
    content.reverse()
    return content

def graphic_service(hangman_list, lives):
    if lives == 7: return hangman_list
    elif lives == 6: return [hangman_list[0]] + hangman_list[2:]
    elif lives == 5: return [hangman_list[0]] + hangman_list[3:]
    elif lives == 4: return [hangman_list[0]] + hangman_list[4:]
    elif lives == 3: return [hangman_list[0], hangman_list[3], hangman_list[4], hangman_list[7]]

def graphic_display(graphics_list, lives_left):
    return graphics_list[lives_left]

def game_display(progress_display, lives, graphic_display):
    return f"{graphic_display}\nLIVES LEFT: {lives}\nCurrent state of word:\n{progress_display}\n\n"



# service of: loading and processing words file; separation of categories; extracting elements by length for difficulty setting purposes

def load_words_file():
    try:
        with open("countries-and-capitals.txt", "r") as file_object:
            return file_object.read()
    except:
        print('Some error occured')


def list_words_string(words_string):
    list_of_pairs = words_string.split("\n")
    list_of_splitted_pairs = [pair.split(" | ") for pair in list_of_pairs if bool(pair) != False]
    return list_of_splitted_pairs


def list_countries(list_of_splitted_pairs):
    return [element[0] for element in list_of_splitted_pairs]


def list_capitals(list_of_splitted_pairs):
    return [element[1] for element in list_of_splitted_pairs]

def extract_elements_by_difficulty(list_of_words, difficulty):
    if difficulty == 0:
        return [word for word in list_of_words if len(word) <= 5]

    elif difficulty == 1:
        return [word for word in list_of_words if (len(word) > 5 and len(word) <= 7)]

    elif difficulty == 2:
        return [word for word in list_of_words if (len(word) > 7 and len(word) <= 9)]
    
    elif difficulty == 3:
        return [word for word in list_of_words if (len(word) > 9 and len(word) <= 12)]
    
    else:
        return [word for word in list_of_words if len(word) > 12]


# drawning a random word from argument's list

def get_random(list_of_words):
    drawn_number = random.randrange(0,len(list_of_words))
    return list_of_words[drawn_number]


# Main menu with features of categories, predefined or custom difficulty choices

def main_menu():
    print("Welcome in Hangman Game!")
    
    list_of_category = category_picker()
    list_of_difficulty, lives_ammount = difficulty_picker(list_of_category)
    
    play(get_random(list_of_difficulty), lives_ammount)

def category_picker():
    words_list = list_words_string(load_words_file())
    while True:
        print("""Please choose the category, by inputting the correct number:

        1 - countries
        2 - capitals
        3 - mixed\n""")
        user_choice = input("Your pick: ")
        
        
        if user_choice == "1": return  list_countries(words_list)
        
        elif user_choice == "2": return list_capitals(words_list)
        
        elif user_choice == "3": return list_countries(words_list) + list_capitals(words_list)
        
        else:
            incorrect_input_notification()
            continue

def difficulty_picker(list_of_words):
    while True:
        
        print("Type in 1 to choose one of predefined difficulties, 0 to set custom level.\n")
        user_choice = input("Your choice: ")
        
        if user_choice not in ["0", "1"]:
            incorrect_input_notification()
            continue
        
        
        elif int(user_choice) == 1:
            return predefined_difficulties(list_of_words)
        
        else:
            return custom_difficulty(list_of_words)

def set_difficulty():
     while True:
        print("""Choose one of difficulty:
        0 - very easy (7 lives, length of word: <= 5
        1 - easy (6 lives, length of word: between 6 and 7
        2 - medium (5 lives, length of word between 8 and 9
        3 - hard (4 lives, length of word: between 10 and 12
        4 - very hard (3 lives, length of word: > 12\n""")        
        user_choice = input("Your pick: ")
        
        if user_choice not in ["0", "1", "2", "3", "4"]:
            incorrect_input_notification()
            continue
        return int(user_choice)

def predefined_difficulties(list_of_words):
        users_difficulty = set_difficulty()

        list_of_difficulty = extract_elements_by_difficulty(list_of_words, users_difficulty)
        
        return list_of_difficulty, 7 - users_difficulty

def set_lives_ammount():
    while True:
        lives_choice = input("Choose number of lives (3 - 7): ")
        
        if lives_choice not in ["3","4", "5", "6", "7"]:
            incorrect_input_notification()
            continue
        
        return int(lives_choice)

def set_words_length():
    while True:        
        print("""Choose one length level:
        0 - length of word: <= 5)
        1 - length of word: between 6 and 7
        2 - length of word: between 8 and 9
        3 - length of word: between 10 and 12
        4 - length of word: > 12\n""")
        word_len_choice = input("Your pick: ")

        if word_len_choice not in ["0", "1", "2", "3", "4"]:
            incorrect_input_notification()
            continue
        
        return int(word_len_choice)

def custom_difficulty(list_of_words):
    lives_ammount = set_lives_ammount()
    words_length_ammount = set_words_length()
    
    
    list_of_difficulty = extract_elements_by_difficulty(list_of_words, words_length_ammount)
    return list_of_difficulty, lives_ammount


def incorrect_input_notification():
    print("incorrect input, provide correct one.")
    sleep(2)

def clear():
   _ = os.system('clear')



def play(word, lives_ammount):
    
    global word_to_guess 
    word_to_guess = str.lower(word)
    
    global lives 
    lives = lives_ammount
     
    global already_tryed_letters
    already_tryed_letters= set()
    
    global already_guessed_letters
    already_guessed_letters = set()
    
    hangman_graphics = graphic_service(load_hangman_graphic(), lives_ammount)
    print("Witaj w grze hangman \n\n")
    while True:
        progress = progress_service(word, already_guessed_letters)
        
        if str.lower("".join(progress)) == word_to_guess: 
            win_execution(word)
            break

        print(game_display(progress_display(progress), lives, graphic_display(hangman_graphics, lives)))
        
        users_letter = str.lower(input("Type in a letter: "))
        
        if users_letter == "quit": 
            print("thank you for your time")
            break
        
        guess = user_guess(users_letter)
        
        if lives == 0:
            print("No more lifes. Game is over")
            print(graphic_display(hangman_graphics, lives))
            print(f"The word to guess was: {word}")
            break


if __name__ == "__main__":
     main_menu()