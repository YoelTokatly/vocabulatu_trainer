
import json
import pandas as pd
import constant as cs
import sqlite3
from time import sleep
from rich.console import Console
from rich.table import Table

class Functions: 
            def  edit(DB_PATH):                
                conn = sqlite3.connect(DB_PATH)
                query = f"SELECT *  FROM vocabulary"
                df_result = pd.read_sql(query,conn) 
                cursor = conn.cursor()
                choose =input ("do you what to: (a) for adding , 'd' for deliting , 'u' for updating").lower().strip()
                if choose == 'a':
                        new_row =[]
                        while True:
                                unit = input("Enter unit (or 'q' to quit): ")
                                if unit == 'q':
                                    break                                
                                word = input ("Enter word:")
                                meaning = input ("Enter meaning:")                                                                
                                query = f"SELECT count(*) FROM vocabulary WHERE word =  '{word}'"
                                q_result = pd.read_sql(query,conn)['count(*)'][0]
                                if q_result >0: 
                                        print ('already exist')
                                else:      
                                        cursor.execute(
                                            "INSERT INTO vocabulary (unit_id, word, meaning) VALUES (?, ?, ?)",
                                             (unit, word, meaning)
                                        )
                                        conn.commit()
                                        conn.close()
                                        print("Done")
                                        exit()
                elif choose == 'd':
                        try :
                            word = input ("Enter word to delete:").lower().strip()
                            query = f"SELECT * FROM vocabulary WHERE word like '%{word}%'"
                            q_result = pd.read_sql(query,conn)
                            print(q_result)
                            id_2_delete = int(input(f'please select id to delete {q_result}'))
                            df_2_delete =q_result[ q_result['id'] == id_2_delete]
                            cursor.execute(f"delete from vocabulary WHERE id = {id_2_delete}"                                        )
                            conn.commit()
                            conn.close()
                            print(q_result[q_result['id'] == id_2_delete]['word'] +'is no more!')
                        except :
                            print(f'{df_2_delete['name']} was not found, goodby!')

                elif choose == 'u':
                        try:
                             # Prepare the SQL query with placeholders for safety
                            word = input ("Enter word to update:").lower().strip()
                            query = f"SELECT * FROM vocabulary WHERE word like '%{word}%'"
                            q_result = pd.read_sql(query,conn)
                            # print(q_result)
                            id_2_delete = int(input(f'please select id to update {q_result}'))
                            df_2_delete = q_result[ q_result['id'] == id_2_delete]
                            meaning = input ("Enter updated meaning:") 
                            query = f"UPDATE vocabulary SET meaning = {meaning} where id = {id_2_delete}"
                            # Execute the update query
                            cursor.execute(query,(meaning,id_2_delete))
                            conn.commit()
                            conn.close()
                        except: None    
                            
                        return   None                          
  


            def  traning(DB_PATH):
                conn = sqlite3.connect(DB_PATH)
                query = f"SELECT *  FROM vocabulary"
                df_db = pd.read_sql(query,conn) 
                df_db['meaning'] = df_db['meaning'].apply(lambda x: x[::-1])
                # df_db['meaning'] = df_db['meaning'].str.lower()
                # df_db['meaning'][0:0:-1]
                filter = df_db['unit_id'].str.contains('unit_')
                units = df_db['unit_id'][filter].drop_duplicates().reset_index(drop=True)
                unit_filter = input(f"Select unit: {units} ")
                df_result = df_db[df_db['unit_id'] == 'unit_'+unit_filter]
                looping = 0
                # remember
                while looping < 3:
                        for word in df_result['word']:
                                print(f'word is : {word}')
                                sleep(2)
                                print(f"Meaning {df_result[df_result['word'] == word]['meaning'].values[0]}")
                        looping += 1
                        print (f'round {looping} is over')
                conn.close()
                exit()
            
            def  testing(DB_PATH):
                conn = sqlite3.connect(DB_PATH)
                query = f"SELECT *  FROM vocabulary"
                df_db = pd.read_sql(query,conn) 
                # df_db['meaning'] = df_db['meaning'].str.lower()
                # df_db['meaning'][0:0:-1]
                filter = df_db['unit_id'].str.contains('unit_') #to include only real units
                units = df_db['unit_id'][filter].drop_duplicates().reset_index(drop=True) #filter only real units
                unit_filter = input(f"Select unit: {units} ") #user choose unit for the quize
                df_result = df_db[df_db['unit_id'] == 'unit_'+unit_filter] #filter data to user unit of chooice
                ### the quize ####
                score = 0 
                
                for word in df_result['word']:
                        print(f'word is : {word}')
                        meaning = input("Enter meaning:")
                        if meaning == df_result[df_result['word'] == word]['meaning'].values[0]:
                            score += 1
                            print("correct")
                            exit()
                        else:
                            print("wrong")
                            print(f"the correct answer is : {df_result[df_result['word'] == word]['meaning'].values[0]}")
                print (f"your score is : {score} out of {len(df_result)}")
                exit()


                console = Console()

                def display_table(dataframe):
                        table = Table(show_header=True, header_style="bold magenta")
                        for column in dataframe.columns:
                                table.add_column(column)
                        for _, row in dataframe.iterrows():
                                table.add_row(*map(str, row.values))
                        console.print(table)




