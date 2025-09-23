from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import redis
from rq import Queue, SimpleWorker as Worker
import psycopg2
from youtube_comment_downloader import YoutubeCommentDownloader

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "mananmalik6" 
DB_HOST = "localhost"
DB_PORT = "5432"

print("Loading AI models...")
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
print("Models loaded.")

def is_question(text: str) -> bool:
    text = text.strip().lower()
    question_starters = ["what", "why", "when", "where", "who", "how", "is", "are", "do", "does", "can", "could", "will", "would"]
    if text.endswith("?") or any(text.startswith(q) for q in question_starters):
        return True
    return False

def fetch_and_analyze_comments(youtube_url: str, video_id: str):
    downloader = YoutubeCommentDownloader()
    comments_generator = downloader.get_comments_from_url(youtube_url, language="en")


    comments_data = []
    comment_texts = []

    for comment in comments_generator:
        if len(comments_data) >= 20:
            break
        comments_data.append(comment)
        comment_texts.append(comment['text'])
    
    if not comment_texts:
        print("No comments found or fetched for this URL.")
        return


    vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
    tfidf_matrix = vectorizer.fit_transform(comment_texts)
    feature_names = vectorizer.get_feature_names_out()
    

    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    for i, comment in enumerate(comments_data):
        comment_text = comment['text']
        sentiment = classifier(comment_text)[0]
        question_flag = is_question(comment_text)

        vector = tfidf_matrix[i]
        df = pd.DataFrame(vector.T.todense(), index=feature_names, columns=["tfidf"])
        df = df.sort_values(by=["tfidf"], ascending=False)
        keywords = df[df['tfidf'] > 0].head(3).index.tolist()

        try:
            insert_script = """
                INSERT INTO comments (video_id, comment_text, sentiment_label, sentiment_score, is_question, keywords)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            insert_values = (video_id, comment_text, sentiment['label'], sentiment['score'], question_flag, keywords)
            cur.execute(insert_script, insert_values)
            conn.commit()
            print(f"Processed and saved comment: {comment_text[:50]}...")
        except Exception as e:
            print(f"Error saving to DB: {e}")
            conn.rollback()
    
    cur.close()
    conn.close()
    print(f"--- Finished processing {len(comments_data)} comments for video {video_id} ---")

if __name__ == '__main__':
    listen = ['default']
    redis_conn = redis.Redis(host='localhost', port=6379)
    q = Queue(connection=redis_conn)
    worker = Worker(queues=[q], connection=redis_conn)
    print("Worker is starting...")
    worker.work()