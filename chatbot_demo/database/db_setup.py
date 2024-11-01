import psycopg2
from typing import List, Dict

#connection params
db_params = {
        'dbname': 'testdatabase',
        'user': 'testuser',
        'password': 'password',
        'host': 'localhost',
        'port': '5432'
    }

#UNSAFE FOR CODE INJECTION, DO NOT USE WITH USER INPUT
def create_table_if_not_exists(table_name: str, column_lines: str[]):
    try:
        conn = psyc.connect(**db_params)
        cursor = conn.cursor()
        command = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        
        for line in column_lines:
            command += f"\n{line},"
        command += ");"
        
                
        



def db_setup():

    #connect to the PostgreSQL database
    try:
        print("starting database setup")
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        print("connected to database")
        #create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            candidate_uuid UUID,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            job_position VARCHAR(50),
            interview_status VARCHAR(20)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            company_uuid UUID,
            company_name VARCHAR(50)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_candidates (
            company_uuid UUID,
            candidate_uuid UUID
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            question_uuid UUID,
            question VARCHAR(1000)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            candidate_uuid UUID,
            question_uuid UUID,
            response VARCHAR(1000)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcripts (
            candidate_uuid UUID,
            interview_date DATE,
            transcript VARCHAR(50000)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bots (
            bot_uuid UUID,
            bot_name VARCHAR(50),
            bot_description VARCHAR(200)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_presets (
            company_uuid UUID,
            bot_uuid UUID,
            presets VARCHAR(100)
        );
        ''')

        # Commit the changes
        conn.commit()
        print("database setup successful")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
