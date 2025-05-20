
import json
import pandas as pd
import constant as cs
import sqlite3
from time import sleep
from rich.console import Console
from rich.table import Table
import streamlit as st

class Functions: 
        def  edit(DB_PATH):      
                                st.title("Vocabulary Editor")
                                conn = sqlite3.connect(DB_PATH)
                                query = "SELECT * FROM vocabulary"
                                df_result = pd.read_sql(query, conn)  
                                st.write("Current Vocabulary Database:")
                                st.dataframe(df_result) 
        
                                action = st.radio("Choose an action:", ["Add", "Delete", "Update"], horizontal=True)
                                
                                if action == "Add":
                                        with st.form("add_form"):
                                                st.subheader("Add New Word")
                                                unit = st.text_input("Enter unit:")
                                                word = st.text_input("Enter word:")
                                                meaning = st.text_input("Enter meaning:")
                                                submit = st.form_submit_button("Add Word")
                                                
                                                if submit and unit and word and meaning:
                                                        cursor = conn.cursor()
                                                        query = f"SELECT count(*) FROM vocabulary WHERE word = '{word}'"
                                                        q_result = pd.read_sql(query, conn)['count(*)'][0]
                                                        
                                                        if q_result > 0:
                                                                st.error(f"Word '{word}' already exists!")
                                                        else:
                                                                cursor.execute(
                                                                        "INSERT INTO vocabulary (unit_id, word, meaning) VALUES (?, ?, ?)",
                                                                        (unit, word, meaning)
                                                                )
                                                                conn.commit()
                                                                st.success(f"Added '{word}' successfully!")
                                                                
                                
                                elif action == "Delete":
                                        word_search = st.text_input("Search for word to delete:")
                                        if word_search:
                                                query = f"SELECT * FROM vocabulary WHERE word LIKE '%{word_search}%'"
                                                q_result = pd.read_sql(query, conn)
                                                
                                                if not q_result.empty:
                                                        st.dataframe(q_result)
                                                        id_to_delete = st.selectbox("Select ID to delete:", q_result['id'])
                                                        
                                                        if st.button("Delete Word"):
                                                                cursor = conn.cursor()
                                                                word_to_delete = q_result[q_result['id'] == id_to_delete]['word'].values[0]
                                                                cursor.execute(f"DELETE FROM vocabulary WHERE id = {id_to_delete}")
                                                                conn.commit()
                                                                st.success(f"'{word_to_delete}' has been deleted!")
                                                          
                                                else:
                                                        st.warning(f"No words found matching '{word_search}'")
                                
                                elif action == "Update":
                                        word_search = st.text_input("Search for word to update:")
                                        if word_search:
                                                query = f"SELECT * FROM vocabulary WHERE word LIKE '%{word_search}%'"
                                                q_result = pd.read_sql(query, conn)
                                                
                                                if not q_result.empty:
                                                        st.dataframe(q_result)
                                                        id_to_update = st.selectbox("Select ID to update:", q_result['id'])
                                                        new_meaning = st.text_input("Enter new meaning:")
                                                        
                                                        if st.button("Update Word") and new_meaning:
                                                                cursor = conn.cursor()
                                                                cursor.execute("UPDATE vocabulary SET meaning = ? WHERE id = ?", (new_meaning, id_to_update))
                                                                conn.commit()
                                                                st.success(f"Word updated successfully!")
                                                              
                                                else:
                                                        st.warning(f"No words found matching '{word_search}'")
                                
                                conn.close()
                                return   None                          
  


        def traning(DB_PATH):
                st.title("Vocabulary Training")
                
                conn = sqlite3.connect(DB_PATH)
                query = "SELECT * FROM vocabulary"
                df_db = pd.read_sql(query, conn)
                
                filter = df_db['unit_id'].str.contains('unit_')
                units = df_db.loc[filter, 'unit_id'].drop_duplicates().reset_index(drop=True)
                
                unit_filter = st.selectbox("Select unit:", units)
                
                df_result = df_db[df_db['unit_id'] == unit_filter]
                
                if st.button("Start Training"):
                        if not df_result.empty:
                                with st.container():
                                        progress_bar = st.progress(0)
                                        status_text = st.empty()
                                        word_display = st.empty()
                                        meaning_display = st.empty()
                                        
                                        total_rounds = 3
                                        for round_num in range(1, total_rounds + 1):
                                                status_text.text(f"Round {round_num} of {total_rounds}")
                                                
                                                for i, (_, row) in enumerate(df_result.iterrows()):
                                                        progress = (i + (round_num - 1) * len(df_result)) / (total_rounds * len(df_result))
                                                        progress_bar.progress(progress)
                                                        
                                                        word_display.markdown(f"### Word: {row['word']}")
                                                        # Wait 2 seconds before showing meaning
                                                        time_placeholder = meaning_display.empty()
                                                        for remaining in range(2, 0, -1):
                                                                time_placeholder.text(f"Showing meaning in {remaining}...")
                                                                sleep(1)
                                                        meaning_display.markdown(f"### Meaning: {row['meaning']}")
                                                        sleep(2)
                                                
                                                if round_num < total_rounds:
                                                        st.info(f"Round {round_num} completed! Starting next round...")
                                                        sleep(1)
                                        
                                        progress_bar.progress(1.0)
                                        st.success("Training completed!")
                        else:
                                st.warning("No words found for the selected unit.")
                
                conn.close()


        def testing(DB_PATH):
                st.title("Vocabulary Testing")
                
                conn = sqlite3.connect(DB_PATH)
                query = "SELECT * FROM vocabulary"
                df_db = pd.read_sql(query, conn)
                
                filter = df_db['unit_id'].str.contains('unit_')
                units = df_db.loc[filter, 'unit_id'].drop_duplicates().reset_index(drop=True)
                
                unit_filter = st.selectbox("Select unit for testing:", units)
                
                df_result = df_db[df_db['unit_id'] == unit_filter]
                
                if st.button("Start Test"):
                        if not df_result.empty:
                                # Initialize session state if not already done
                                if 'test_index' not in st.session_state:
                                        st.session_state.test_index = 0
                                        st.session_state.score = 0
                                        st.session_state.words = df_result.to_dict('records')
                                        st.session_state.total_words = len(df_result)
                                        st.session_state.test_active = True
                                
                                # Display progress
                                st.progress(st.session_state.test_index / st.session_state.total_words)
                                st.write(f"Question {st.session_state.test_index + 1} of {st.session_state.total_words}")
                                
                                # Display current word and get user input
                                if st.session_state.test_index < st.session_state.total_words:
                                        current_word = st.session_state.words[st.session_state.test_index]
                                        st.markdown(f"### Word: {current_word['word']}")
                                        
                                        user_answer = st.text_input("Enter meaning:", key=f"answer_{st.session_state.test_index}")
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                                if st.button("Submit Answer"):
                                                        if user_answer.lower().strip() == current_word['meaning'].lower().strip():
                                                                st.success("Correct!")
                                                                st.session_state.score += 1
                                                                sleep(2)
                                                        else:
                                                                st.error(f"Wrong! The correct answer is: {current_word['meaning']}")
                                                                sleep(2)
                                                        # Move to next word
                                                        st.session_state.test_index += 1
                                                        st.rerun()
                                        
                                        with col2:
                                                if st.button("Skip Word"):
                                                        st.warning(f"Skipped. The answer was: {current_word['meaning']}")
                                                        st.session_state.test_index += 1
                                                        st.rerun()
                                
                                # Test completed
                                if st.session_state.test_index >= st.session_state.total_words:
                                        st.balloons()
                                        st.success(f"Test completed! Your score: {st.session_state.score} out of {st.session_state.total_words}")
                                        
                                        # Show percentage
                                        percentage = (st.session_state.score / st.session_state.total_words) * 100
                                        st.write(f"Percentage: {percentage:.1f}%")
                                        
                                        if st.button("Take Another Test"):
                                                # Reset session state
                                                for key in ['test_index', 'score', 'words', 'total_words', 'test_active']:
                                                        if key in st.session_state:
                                                                del st.session_state[key]
                                                st.rerun()
                        else:
                                st.warning("No words found for the selected unit.")
                
                # Reset test button
                if 'test_active' in st.session_state and st.session_state.test_active:
                        if st.button("Cancel Test"):
                                for key in ['test_index', 'score', 'words', 'total_words', 'test_active']:
                                        if key in st.session_state:
                                                del st.session_state[key]
                                st.rerun()
                
                conn.close()


               