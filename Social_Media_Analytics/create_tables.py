
import psycopg2


DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "your_password" 
DB_HOST = "localhost"
DB_PORT = "5432"

try:

    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)

    cur = conn.cursor() 


    create_script = ''' CREATE TABLE IF NOT EXISTS comments (
                            id      SERIAL PRIMARY KEY,
                            video_id  VARCHAR(255) NOT NULL,
                            comment_text TEXT NOT NULL
                        )'''


    cur.execute(create_script)
    print("Table 'comments' created successfully!")


    conn.commit()

except Exception as e:
    print(f"An error occurred: {e}")

finally:

    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()