from google.colab import output
import string
import time
def get_word():
  secret_word = input('Guessing player must look away.\nNow give me your secret word!\n')
  if ' ' in secret_word:
    print(f"Sorry, \"{secret_word}\" can't have spaces!")
    return None
  else:
    secret_word = secret_word.upper()
    return secret_word

def check_letter(word, hash_word, counter):
  output.clear()
  if counter == 5:
    print(case5)
  if counter == 4:
    print(case4)
  if counter == 3:
    print(case3)
  if counter == 2:
    print(case2)
  if counter == 1:
    print(case1)
  if counter == 0:
    print(case0)
  print(hash_word)
  letter = input('Pick a letter:\n')
  letter = letter.upper()
  letter = letter[0]
  if letter not in string.ascii_uppercase:
    letter = input('Sorry, try again:\n')
  if letter in word:
    for i in range(len(word)):
      if letter == word[i]:
        hash_word[i] = letter
    if hash_word == word:
      print('WINNER!')
      return hash_word, counter
    return hash_word, counter
  else:
    print(f"WRONG! Number of mistakes left: {counter}")
    counter -= 1
    time.sleep(1.5)
    return hash_word, counter

word = None
counter = 5
case0 = """
  _______
  |     |
  |     O
  |    /|\\
  |    / 
  |
  |______"""
case1 = """
  _______
  |     |
  |     O
  |    /|\\
  |     
  |
  |______"""
case2 = """
  _______
  |     |
  |     O
  |    /|
  |     
  |
  |______"""
case3 = """
  _______
  |     |
  |     O
  |     |
  |     
  |
  |______"""
case4 = """
  _______
  |     |
  |     O
  |     
  |     
  |
  |______"""
case5 = """
  _______
  |     |
  |     
  |     
  |     
  |
  |______"""
while word == None:
  word = list(get_word())
output.clear()
hash_word = ['-' for letter in word]
print('Ready!\n', case5, '\n',''.join(hash_word))
while (counter >= 0) & (hash_word != word):
  hash_word, counter = check_letter(word, hash_word, counter)
if hash_word == word:
  None
if counter < 0:
  output.clear()
  print("""
  _______
  |     |
  |     O
  |    /|\\
  |    / \\
  |
  |______ 
  
  YOU'VE BEEN HANGED!""")