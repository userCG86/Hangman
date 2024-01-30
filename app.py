import streamlit as st
import random
import string
import requests
from img import case

@st.cache_data
def get_word_list():
    listy = st.empty()
    listy.write("Getting list")
    response = requests.get("https://raw.githubusercontent.com/userCG86/Hangman/main/list_of_words.txt?token=GHSAT0AAAAAACCWVZJHWCA3QOADW4HVMOGKZDMX44Q")
    if response.status_code == 200:
        listy.empty()
        return response.content.decode()
    else:
        f"Warning! Error in loading word list: {response.status_code}"

def get_word():
    player_input = st.empty()
    secret_word = player_input.text_input('Guessing player must look away.\nNow give me your secret word!', key="secret").upper()
    for letter in secret_word:
        if (letter not in string.ascii_uppercase):
            st.write(f"Out of bounds, Partner. Stick to A-Z, no special characters, diacritics, or other funny business.")
            return ''
    return secret_word

def get_random_word(all_words):
    return random.choice(all_words.split('\n'))

def game_state(hash_word, counter, guesses):
    game_state = st.empty()
    with game_state.container():
        st.write(f"The secret word is {hash_word}")
        st.text(case[counter])
        st.write(f"Used letters: {''.join(sorted(list(guesses)))}")

def guess_letter(word, hash_word, counter, guesses):
    
    player_guess = st.empty()
    with player_guess.container():
        game_state(hash_word, counter, guesses)
        letter = st.text_input('Pick a letter:\n', key="letter_pick", placeholder=None, max_chars=1)
    try:
        letter = letter.upper()
        letter = letter[0]
    except:
        return hash_word, counter, guesses

    if letter not in string.ascii_uppercase:
        f"Out of bounds, Partner. Stick to A-Z, no special characters, diacritics, or other funny business."
        letter = ''

    elif letter in guesses:
        f"Whoa there, Partner! You already guessed {letter}. Don't throw away your chances."
        letter = ''

    elif letter in word:
        f"YES! {letter} is in the secret word."
        for i in range(len(word)):
            if letter == word[i]:
                hash_word = hash_word[:i] + letter + hash_word[i+1:]
    else:
        f"WRONG! Number of mistakes left: {counter}"
        counter -= 1

    guesses += letter
    with player_guess.container():
        game_state(hash_word, counter, guesses)

    return hash_word, counter, guesses

def start_game(all_words):
    players = st.empty()
    counter = 5
    guesses = ''
    word = ''
    with players.container():
        n_players = st.selectbox("Alright, Partner. How many players this time?", ["None", "Single player", "Multiplayer"])
        if n_players == "Multiplayer":
            word = get_word()
        elif n_players == "Single player":
            word = get_random_word(all_words)

    if word != '':
        hash_word = '-'*len(word)
        players.empty()
        return counter, guesses, word, hash_word
    else:
        return 5, '', '', ''
      
    


    
    
if "words" not in st.session_state:
    st.session_state.words = {}
placeholder = st.empty()
param = True
all_words = get_word_list()
if len(st.session_state.words) == 0 or st.session_state.words["word"] == '':
    with placeholder.container():
        counter, guesses, word, hash_word = start_game(all_words) 
        st.session_state.words["counter"] = counter
        st.session_state.words["guesses"] = guesses
        st.session_state.words["word"] = word
        st.session_state.words["hash_word"] = hash_word

if st.session_state.words["word"] != '':
    with placeholder.container():
        st.session_state.words["hash_word"], st.session_state.words["counter"], st.session_state.words["guesses"] = guess_letter(st.session_state.words["word"], st.session_state.words["hash_word"], st.session_state.words["counter"], st.session_state.words["guesses"])
        st.button("Reset", key="reset")
    if st.session_state.words["hash_word"] == st.session_state.words["word"]:
        placeholder.empty()
        with placeholder.container():
            st.text(case[st.session_state.words["counter"]])
            f'WINNER! The secret word was {st.session_state.words["word"]}'
    elif st.session_state.words["counter"] < 0:
        placeholder.empty()
        with placeholder.container():
            st.text(case[st.session_state.words["counter"]])
            f'The secret word was {st.session_state.words["word"]}'        
    if st.session_state.reset:
        st.session_state.clear()
        st.rerun()
