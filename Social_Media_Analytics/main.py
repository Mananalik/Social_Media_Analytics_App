
from fastapi import FastAPI
from pydantic import BaseModel
import redis
from rq import Queue
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlparse, parse_qs
from worker import fetch_and_analyze_comments
import psycopg2
from rq.job import Job

app = FastAPI()

origins=[
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_conn = redis.Redis(host='localhost', port=6379)
q = Queue(connection=redis_conn)

class CommentPayload(BaseModel):
    url:str


@app.get("/")
def read_root():
    return {"message": "Server is running."}


@app.post("/start-analysis")
def start_analysis(payload: CommentPayload):
    parsed_url = urlparse(payload.url)
    video_id = parse_qs(parsed_url.query).get('v')
    if not video_id:
        return {"error": "Invalid YouTube URL. 'v' parameter not found."}
    video_id = video_id[0]
    job = q.enqueue(fetch_and_analyze_comments, payload.url,video_id,job_id=video_id)
    return{
        "message":"Analysis job has been queued successfully.",
        "job_id": job.id,
    }
@app.get("/results/{job_id}")
def get_results(job_id:str):
    try:
        job = Job.fetch(job_id,connection=redis_conn)
        if job.is_finished:
            conn = psycopg2.connect(database="postgres", user="postgres", password="mananmalik6", host="localhost", port="5432")
            cur = conn.cursor()
            cur.execute("SELECT * FROM comments WHERE video_id = %s", (job_id,))

            results = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

            cur.close()
            conn.close()

            results_as_dict = [dict(zip(colnames, row)) for row in results]
            return {"status": "finished", "data": results_as_dict}
        elif job.is_failed:
            return {"status": "failed"}
        else:
            return {"status": "pending"}
    except Exception as e:
        return{"status":"error","message":str(e)}



