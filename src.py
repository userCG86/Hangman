import random
import string
import time
import requests
from IPython.display import clear_output
from img import case

def get_word_list():
  response = requests.get("https://raw.githubusercontent.com/userCG86/Hangman/main/list_of_words.txt?token=GHSAT0AAAAAACCWVZJHWCA3QOADW4HVMOGKZDMX44Q")
  if response.status_code == 200:
      return response.content.decode()
  else:
      print(f"Warning! Error in loading word list: {response.status_code}")

def get_word():
  secret_word = input().upper()
  for letter in secret_word:
    if (letter not in string.ascii_uppercase):
      print(f"Out of bounds, Partner. Stick to A-Z, no special characters, diacritics, or other funny business.")
      return None
  return secret_word

def get_random_word(all_words):
  return random.choice(all_words.split('\n'))

def guess_letter(word, hash_word, counter, guesses):
  letter = input('Pick a letter:\n')
  try:
    letter = letter.upper()
    letter = letter[0]
  except:
    return hash_word, counter, guesses

  if letter not in string.ascii_uppercase:
    print(f"Out of bounds, Partner. Stick to A-Z, no special characters, diacritics, or other funny business.")
    letter = ''

  elif letter in guesses:
    print(f"Whoa there, Partner! You already guessed {letter}. Don't throw away your chances.")
    letter = ''

  elif letter in word:
    print(f"YES! {letter} is in the secret word.")
    for i in range(len(word)):
      if letter == word[i]:
        hash_word = hash_word[:i] + letter + hash_word[i+1:]
  else:
    print(f"WRONG! Number of mistakes left: {counter}")
    counter -= 1

  guesses += letter
  time.sleep(1.5)
  
  return hash_word, counter, guesses

def play_hangman():
  try:
    all_words
  except:
    all_words = get_word_list()
  word = None
  counter = 5
  guesses = ''

  n_players = input("Alright, Partner. How many players this time?\n")
  if n_players.isnumeric() and int(n_players) > 1:
    print('Guessing player must look away.\nNow give me your secret word!')
    while word == None:
      word = get_word()
  else:
    word = get_random_word(all_words)
  hash_word = '-'*len(word)
  
  while (counter >= 0) & (hash_word != word):
    clear_output(wait=False)
    print(f"The secret word is {hash_word}")
    print(case[counter])
    print(f"Used letters: {''.join(sorted(list(guesses)))}")
    hash_word, counter, guesses = guess_letter(word, hash_word, counter, guesses)

  if hash_word == word:
    clear_output(wait=False)
    print(case[counter])
    print(f"WINNER! The secret word was {word}")
  else:
    clear_output(wait=False)
    print(case[-1])
    print(f"The secret word was {word}")