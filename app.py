import streamlit as st
from img import case
from src_st import get_word_list, start_game, guess_letter

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
