from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import redis
from rq import  Queue, SimpleWorker as Worker
import psycopg2

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "mananmalik6" 
DB_HOST = "localhost"
DB_PORT = "5432"


print("Loading AI models...")
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
print("Models loaded.")

def is_question(text: str)-> bool:
    text = text.strip().lower()
    question_starters = ["what", "why", "when", "where", "who", "how", "is", "are", "do", "does", "can", "could", "will", "would"]
    if text.endswith("?") or any(text.startswith(q) for q in question_starters):
        return True
    return False

def analyze_and_save_comment(comment_text: str):


    sentiment = classifier(comment_text)[0]
    question_flag = is_question(comment_text)

    comment_corpus = [
        comment_text,
        "This is a neutral comment for context.",
        "What is the best feature in this update?",
    ]
    vectorizer = TfidfVectorizer(stop_words='english', max_features=3)
    tfidf_matrix = vectorizer.fit_transform(comment_corpus)
    feature_names = vectorizer.get_feature_names_out()
    first_document_vector = tfidf_matrix[0]
    df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"])
    df = df.sort_values(by=["tfidf"], ascending=False)
    keywords = df[df['tfidf'] > 0].head(3).index.tolist()

    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        insert_script = """
            INSERT INTO comments (video_id, comment_text, sentiment_label, sentiment_score, is_question,keywords)
            VALUES (%s, %s, %s, %s, %s,%s)
        """
        insert_values = (
            "real_video_id_123", # Placeholder video ID
            comment_text,
            sentiment['label'],
            sentiment['score'],
            question_flag,
            keywords
        )
        cur.execute(insert_script, insert_values)
        conn.commit()
        print(f"Successfully analyzed and saved comment: '{comment_text}'")

    except Exception as e:
        print(f"Error saving to DB: {e}")

    finally:
        if 'cur' in locals() and cur is not None:
            cur.close()
        if 'conn' in locals() and conn is not None:
            conn.close()


if __name__ == '__main__':
    listen = ['default']
    redis_conn = redis.Redis(host='localhost', port=6379)

    q = Queue(connection=redis_conn)
    worker = Worker(q, connection=redis_conn)
    print("Worker is starting...")
    worker.work()