import psycopg2

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "mananmalik6" 
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    alter_script = '''
                   ALTER TABLE comments
                   ADD COLUMN IF NOT EXISTS sentiment_label VARCHAR(50),
                   ADD COLUMN IF NOT EXISTS sentiment_score FLOAT,
                   ADD COLUMN IF NOT EXISTS is_question BOOLEAN,
                   ADD COLUMN IF NOT EXISTS keywords TEXT[]; '''
    cur.execute(alter_script)
    print("Table 'comments' updated sucessfully with keyword column!" )
    conn.commit()
except Exception as e:
    print(f"Error updating table: {e}")
finally:
    if 'cur' in locals() and cur is not None:
        cur.close()
    if 'conn' in locals() and conn is not None:
        conn.close()