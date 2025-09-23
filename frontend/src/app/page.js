'use client';
import {useState} from 'react';

export default function HomePage(){
    const [url,setUrl] = useState('');

    const [isLoading,setIsLoading] = useState(false);
    const [jobId,setJobId] = useState(null);
    const handleAnalyzeClick = async ()=>{
      setIsLoading(true);
      setJobId(null);
    
    try{
      const response = await fetch('http://127.0.0.1:8000/start-analysis',{
        method:'POST',
        headers:{
          'Content-Type':'application/json',
        },
        body: JSON.stringify({url: url}),
      });

      if(!response.ok){
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      console.log('Backend Response:',result);
      setJobId(result.job_id);
    } catch(error){
      console.error("Failed to start analysis:",error);
      alert("Error: Could not connect to the backend.")
    }finally{
      setIsLoading(false);
    }
  };
    return(
      <main style = {{fontFamily: 'sans-serif', textAlign: 'center', marginTop: '50px' }}>
        <h1>Social Media Analytics Dashboard</h1>
        <p style={{color: '#555'}}>Paste a YouTube video URL below to analyze its comments.</p>
        <div style={{ marginTop: '30px'}}>
          <input
            type = "text"
            value={url}
            onChange={(e)=>setUrl(e.target.value)}
            placeholder="Enter YouTube URL here"
            style={{padding: '10px', width: '400px', marginRight: '10px' }}
            disabled = {isLoading}
          />
          <button 
            onClick={handleAnalyzeClick}
            style={{padding: '10px 15px', cursor: 'pointer'}}
            disabled = {isLoading}
            >
             {isLoading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
        {jobId &&(<div style={{ marginTop: '20px' }}>
          <p>Analysis started! Job ID: {jobId}</p>
        </div>)}
      </main>
    );
}