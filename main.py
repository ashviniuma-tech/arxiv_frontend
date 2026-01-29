"""
ArXiv Similarity Search - FastAPI Backend
Professional web interface for finding and analyzing similar research papers
"""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pipeline_orchestrator import MockPipelineOrchestrator

# Initialize FastAPI app
app = FastAPI(
    title="ArXiv Similarity Search",
    description="AI-Powered Research Paper Discovery & Analysis Engine",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instances
orchestrators = {
    "arxiv": None,
    "local": None
}

# Session storage
sessions = {}


class SearchRequest(BaseModel):
    """Search request model"""
    mode: str  # "arxiv" or "local"
    abstract: str


class SummaryRequest(BaseModel):
    """Summary request model"""
    mode: str
    paper_index: int
    session_id: str


def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        'data/temp_pdfs',
        'data/sample_pdfs',
        'data/local_database',
        'data/faiss_indices',
        'outputs',
        'logs',
        'frontend/static/css',
        'frontend/static/js',
        'frontend/static'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        gitkeep_path = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            Path(gitkeep_path).touch()


def load_config() -> dict:
    """Load configuration from config.yaml"""
    if not os.path.exists('config.yaml'):
        return {
            'arxiv': {'max_results': 20},
            'reranking': {'top_k': 5},
            'local_database': {'folder_path': 'data/local_database'},
            'paths': {'sample_pdfs': 'data/sample_pdfs'}
        }
    
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def get_orchestrator(mode: str) -> MockPipelineOrchestrator:
    """Get or create orchestrator for mode"""
    if orchestrators[mode] is None:
        orchestrators[mode] = MockPipelineOrchestrator(mode=mode)
    return orchestrators[mode]


@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    print("Initializing ArXiv Similarity Search System...")
    create_directories()
    print("Directories created successfully")


# Mount static files directory
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the login page"""
    login_path = Path("frontend/login.html")
    
    if login_path.exists():
        return FileResponse(login_path)
    
    # If file doesn't exist, return error
    return HTMLResponse(content="""
    <html>
    <body>
        <h1>Error: Login page not found</h1>
        <p>Please create frontend/login.html</p>
    </body>
    </html>
    """)


@app.get("/index.html", response_class=HTMLResponse)
async def read_main():
    """Serve the main application HTML page"""
    html_path = Path("frontend/index.html")
    
    if html_path.exists():
        return FileResponse(html_path)
    
    # If file doesn't exist, return embedded HTML
    return HTMLResponse(content=get_embedded_html())


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.get("/api/config")
async def get_config():
    """Get system configuration"""
    config = load_config()
    
    # Check local database status
    local_db_path = config.get('local_database', {}).get('folder_path', 'data/local_database')
    sample_pdfs_path = config.get('paths', {}).get('sample_pdfs', 'data/sample_pdfs')
    
    local_pdfs = []
    if os.path.exists(local_db_path):
        local_pdfs = [f for f in os.listdir(local_db_path) if f.endswith('.pdf')]
    
    sample_pdfs = []
    if os.path.exists(sample_pdfs_path):
        sample_pdfs = [f for f in os.listdir(sample_pdfs_path) if f.endswith('.pdf')]
    
    pdf_count = max(len(local_pdfs), len(sample_pdfs))
    
    return {
        "arxiv_max_results": config.get('arxiv', {}).get('max_results', 20),
        "top_k_papers": config.get('reranking', {}).get('top_k', 5),
        "local_database": {
            "path": local_db_path,
            "pdf_count": pdf_count,
            "ready": pdf_count > 0
        },
        "modes": {
            "arxiv": {
                "name": "ArXiv Mode",
                "description": "Search from ArXiv (online)",
                "status": "online"
            },
            "local": {
                "name": "Local Database",
                "description": "Search from local papers (offline)",
                "status": "ready" if pdf_count > 0 else "no_pdfs"
            }
        }
    }


@app.post("/api/search")
async def search_papers(request: SearchRequest):
    """Search for similar papers"""
    try:
        # Validate input
        if len(request.abstract) < 50:
            raise HTTPException(
                status_code=400,
                detail="Abstract too short. Please provide at least 50 characters."
            )
        
        if request.mode not in ["arxiv", "local"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid mode. Must be 'arxiv' or 'local'."
            )
        
        # Get orchestrator
        orchestrator = get_orchestrator(request.mode)
        
        # Run pipeline
        results = orchestrator.run_pipeline(request.abstract)
        
        if not results:
            raise HTTPException(
                status_code=500,
                detail="Search failed. Please try again."
            )
        
        # Generate session ID
        session_id = f"{request.mode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        sessions[session_id] = results
        
        # Prepare response
        response = {
            "session_id": session_id,
            "mode": request.mode,
            "query_abstract": request.abstract,
            "timestamp": results.get('query_timestamp'),
            "keywords": results.get('keywords', []),
            "metrics": results.get('metrics', {}),
            "top_5_papers": []
        }
        
        # Format top 5 papers
        for paper in results.get('top_5_papers', [])[:5]:
            response['top_5_papers'].append({
                "rank": paper.get('rank'),
                "title": paper.get('title'),
                "authors": paper.get('authors', []),
                "year": paper.get('year'),
                "arxiv_id": paper.get('arxiv_id'),
                "url": paper.get('url', ''),
                "similarity": paper.get('similarity'),
                "rerank_score": paper.get('rerank_score'),
                "abstract": paper.get('abstract', '')[:300] + "..."
            })
        
        # Add comparative analysis
        if 'comparative_analysis' in results:
            response['comparative_analysis'] = results['comparative_analysis']
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in search: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/summary")
async def generate_summary(request: SummaryRequest):
    """Generate detailed summary for a paper"""
    try:
        # Validate session
        if request.session_id not in sessions:
            raise HTTPException(
                status_code=404,
                detail="Session not found. Please perform a search first."
            )
        
        results = sessions[request.session_id]
        
        # Validate paper index
        if request.paper_index < 1 or request.paper_index > 5:
            raise HTTPException(
                status_code=400,
                detail="Invalid paper index. Must be between 1 and 5."
            )
        
        # Get paper
        papers = results.get('top_5_papers', [])
        if request.paper_index > len(papers):
            raise HTTPException(
                status_code=404,
                detail="Paper not found."
            )
        
        paper = papers[request.paper_index - 1]
        
        # Get orchestrator
        orchestrator = get_orchestrator(request.mode)
        
        # Generate summary
        summary = orchestrator.generate_summary(paper)
        
        if not summary:
            raise HTTPException(
                status_code=500,
                detail="Summary generation failed."
            )
        
        # Update session with summary
        paper['summary'] = summary
        sessions[request.session_id] = results
        
        return {
            "paper": {
                "rank": paper.get('rank'),
                "title": paper.get('title'),
                "authors": paper.get('authors', []),
                "year": paper.get('year'),
                "arxiv_id": paper.get('arxiv_id')
            },
            "summary": {
                "research_objective": summary.get('research_objective', ''),
                "methodology_summary": summary.get('methodology_summary', ''),
                "key_findings": summary.get('key_findings', []),
                "innovation_and_contribution": summary.get('innovation_and_contribution', ''),
                "technical_details": summary.get('technical_details', ''),
                "limitations_and_future_work": summary.get('limitations_and_future_work', '')
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in summary generation: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session data"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return sessions[session_id]


def get_embedded_html() -> str:
    """Return embedded HTML if frontend/index.html doesn't exist"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ArXiv Similarity Search</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 40px;
            }
            .error {
                background: #fee;
                border: 1px solid #fcc;
                padding: 20px;
                border-radius: 5px;
                color: #c33;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ArXiv Similarity Search</h1>
            <p class="subtitle">AI-Powered Research Paper Discovery</p>
            <div class="error">
                <h3>Frontend Not Found</h3>
                <p>Please create <code>frontend/index.html</code> with the complete frontend.</p>
                <p>The backend API is running at <code>/api/*</code></p>
            </div>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    
    print("="*80)
    print("ARXIV SIMILARITY SEARCH SYSTEM - FASTAPI SERVER")
    print("="*80)
    print("\nStarting server...")
    print("Access the application at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")