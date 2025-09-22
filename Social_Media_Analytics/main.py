
from fastapi import FastAPI
from pydantic import BaseModel
import redis
from rq import Queue
from worker import analyze_and_save_comment
from fastapi.middleware.cors import CORSMiddleware

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
    text:str


@app.get("/")
def read_root():
    return {"message": "Server is running."}


@app.post("/start-analysis")
def start_analysis(payload: CommentPayload):
    job = q.enqueue(analyze_and_save_comment, payload.text)
    return{
        "message":"Analysis job has been queued successfully.",
        "job_id": job.id
    }