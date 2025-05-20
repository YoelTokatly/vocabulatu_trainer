
import json
# import polars as pl
import pandas as pd
import constant as cs
import sqlite3
from time import sleep

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
                            
                            # # Execute the update query
                            cursor.execute(query,(meaning,id_2_delete))
                            
                            # # Get the number of affected rows
                            # updated_count = cursor.rowcount
                            
                            # Commit the changes
                            conn.commit()
                            conn.close()
                        except: None    
                            
                        return   None                          
  


            def  traning(DB_PATH):
                conn = sqlite3.connect(DB_PATH)
                query = f"SELECT *  FROM vocabulary"
                df_db = pd.read_sql(query,conn) 
                df_db['meaning'] = df_db['meaning'].str.lower()
                df_db['meaning'][0:0:-1]
                filter = df_db['unit_id'].str.contains('unit_')
                units = df_db['unit_id'][filter].drop_duplicates().reset_index(drop=True)
                unit_filter = input(f"Select unit: {units} ")
                df_result = df_db[df_db['unit_id'] == 'unit_'+unit_filter]
                score = 0
                # Quize
                # for word in df_result['word']:
                #         print(f'word is : {word}')
                #         meaning = input("Enter meaning:")
                #         if meaning == df_result[df_result['word'] == word]['meaning'].values[0]:
                #             score += 1
                #             print("correct")
                #             exit()
                #         else:
                #             print("wrong")
                #             print(f"the correct answer is : {df_result[df_result['word'] == word]['meaning'].values[0]}")
                # print (f"your score is : {score} out of {len(df_result)}")

                # remember
                for word in df_result['word']:
                        print(f'word is : {word}')
                        sleep(2)
                        print(f"Meaning {df_result[df_result['word'] == word]['meaning'].values[0]}")
      

                conn.close()
                exit()
            
            def  testing():
                    print("i will test")
                    exit()







