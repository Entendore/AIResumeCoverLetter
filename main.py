import streamlit as st
import requests
import json
import time
import os
from datetime import datetime
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
import pandas as pd
import platform
import subprocess
import re
from typing import Dict, List, Any, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px
from docx import Document
import PyPDF2
import io

# Set page config for professional appearance
st.set_page_config(
    page_title="CareerCraft AI - Resume & Cover Letter Generator",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4b5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stExpander {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .success-message {
        background-color: #dcfce7;
        color: #166534;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .warning-message {
        background-color: #fef3c7;
        color: #92400e;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #fecaca;
    }
    .model-badge {
        display: inline-block;
        background-color: #dbeafe;
        color: #1e40af;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    .template-card {
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .template-card:hover {
        border-color: #2563eb;
        transform: scale(1.02);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .template-card.selected {
        border-color: #2563eb;
        background-color: #bfdbfe;
    }
    .section-header {
        font-size: 1.5rem;
        color: #1e3a8a;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3b82f6;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
    }
    .connection-check {
        background-color: #f0f9ff;
        border: 2px solid #bae6fd;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    .install-instructions {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .command-box {
        background-color: #1e293b;
        color: #f1f5f9;
        padding: 1rem;
        border-radius: 6px;
        font-family: monospace;
        margin: 0.5rem 0;
        overflow-x: auto;
    }
    .sidebar-status {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .status-running {
        background-color: #dcfce7;
        border-left: 4px solid #10b981;
    }
    .status-warning {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
    }
    .status-error {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
    }
    .skill-tag {
        display: inline-block;
        background-color: #e0e7ff;
        color: #3730a3;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        margin: 0.25rem;
        font-size: 0.875rem;
    }
    .skill-tag.highlight {
        background-color: #c7d2fe;
        color: #4338ca;
        font-weight: 600;
    }
    .progress-container {
        margin: 1rem 0;
    }
    .progress-bar {
        height: 8px;
        background-color: #e5e7eb;
        border-radius: 4px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background-color: #3b82f6;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    .job-match-card {
        background-color: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .keyword-highlight {
        background-color: #fef3c7;
        padding: 0.1rem 0.2rem;
        border-radius: 3px;
        font-weight: 500;
    }
    .preview-container {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .preview-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e5e7eb;
    }
    .history-item {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .history-item:hover {
        background-color: #f9fafb;
        border-color: #3b82f6;
    }
    .tab-indicator {
        height: 3px;
        background-color: #3b82f6;
        margin-top: -3px;
        border-radius: 3px 3px 0 0;
    }
    .upload-area {
        border: 2px dashed #cbd5e1;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background-color: #f8fafc;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .upload-area:hover {
        border-color: #3b82f6;
        background-color: #eff6ff;
    }
    .upload-success {
        border-color: #22c55e;
        background-color: #f0fdf4;
    }
    .file-info {
        background-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .comparison-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
    .comparison-box {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        background-color: white;
    }
    .comparison-title {
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# Constants
OLLAMA_URL = "http://localhost:11434/api"
DEFAULT_MODEL = "llama3"
RECOMMENDED_MODELS = ["llama3", "mistral", "codellama", "phi3"]

def check_ollama_connection(max_retries: int = 3, delay: int = 2) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Check if Ollama is running with retries and detailed error information
    Returns: (is_running, error_message, models_data)
    """
    for attempt in range(max_retries):
        try:
            with st.spinner(f"🔍 Checking Ollama connection (attempt {attempt + 1}/{max_retries})..."):
                response = requests.get(f"{OLLAMA_URL}/tags", timeout=10)
                
            if response.status_code == 200:
                return True, None, response.json()
            elif response.status_code == 404:
                return False, "❌ Ollama server is running but API endpoint not found. Please update Ollama.", None
            else:
                return False, f"❌ Ollama server returned error code: {response.status_code}", None
                
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(delay)
                continue
            return False, "❌ Failed to connect to Ollama server. Is it running?", None
        except requests.exceptions.Timeout:
            return False, "❌ Connection to Ollama server timed out. Server might be busy or not responding.", None
        except Exception as e:
            return False, f"❌ Unexpected error: {str(e)}", None
    
    return False, "❌ Max retries exceeded. Could not connect to Ollama server.", None

def get_installation_instructions() -> str:
    """Get platform-specific installation instructions"""
    system = platform.system().lower()
    
    instructions = {
        'windows': """
        ### 🪟 Windows Installation:
        1. **Download Ollama**: Visit https://ollama.com/download/OllamaSetup.exe
        2. **Run the installer**: Double-click the downloaded file
        3. **Start Ollama**: 
           - Press `Win + R`, type `cmd`, press Enter
           - In Command Prompt, run: `ollama serve`
        4. **Download a model** (in a new Command Prompt window):
           ```bash
           ollama pull llama3
           ```
        5. **Keep the terminal window open** while using the application
        """,
        
        'darwin': """
        ### 🍎 macOS Installation:
        1. **Install via Homebrew** (recommended):
           ```bash
           brew install ollama
           ```
        2. **Or download directly**: Visit https://ollama.com/download/Ollama-darwin.zip
        3. **Start Ollama**:
           ```bash
           ollama serve
           ```
        4. **Download a model** (in a new Terminal window):
           ```bash
           ollama pull llama3
           ```
        5. **Keep the terminal window open** while using this application
        """,
        
        'linux': """
        ### 🐧 Linux Installation:
        1. **Install Ollama**:
           ```bash
           curl -fsSL https://ollama.com/install.sh | sh
           ```
        2. **Start the service** (recommended):
           ```bash
           sudo systemctl start ollama
           sudo systemctl enable ollama  # To start on boot
           ```
           OR run manually:
           ```bash
           ollama serve
           ```
        3. **Download a model** (in a new terminal):
           ```bash
           ollama pull llama3
           ```
        """,
        
        'default': """
        ### 💻 General Installation:
        1. **Visit the official website**: https://ollama.com
        2. **Download and install** Ollama for your operating system
        3. **Start Ollama server**:
           - Open a terminal/command prompt
           - Run: `ollama serve`
        4. **Download a model** (in a new terminal window):
           ```bash
           ollama pull llama3
           ```
        5. **Keep the server running** while using this application
        """
    }
    
    return instructions.get(system, instructions['default'])

def try_start_ollama() -> Tuple[bool, Optional[str]]:
    """Try to start Ollama service if possible"""
    system = platform.system().lower()
    
    try:
        if system == 'linux':
            # Try to start the systemd service
            result = subprocess.run(['sudo', 'systemctl', 'start', 'ollama'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return True, "✅ Ollama service started successfully!"
            else:
                return False, f"❌ Failed to start Ollama service: {result.stderr}"
        
        elif system == 'darwin':
            # Try to start via brew services
            try:
                result = subprocess.run(['brew', 'services', 'start', 'ollama'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return True, "✅ Ollama service started successfully!"
            except:
                pass
            return False, None
        
        elif system == 'windows':
            # Try to start the Windows service
            try:
                result = subprocess.run(['sc', 'start', 'ollama'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0 or "already running" in result.stdout.lower():
                    return True, "✅ Ollama service started successfully!"
                return False, f"❌ Failed to start Ollama service: {result.stderr}"
            except:
                return False, None
        
        return False, None
        
    except Exception as e:
        return False, f"❌ Error trying to start Ollama: {str(e)}"

def verify_ollama_models(models_data: Optional[Dict]) -> Tuple[bool, Optional[str]]:
    """Verify that there are models available and suggest downloads if needed"""
    if not models_data or 'models' not in models_data or not models_data['models']:
        return False, """
        ⚠️ No models found! You need to download at least one model.
        
        **Recommended models for resume generation:**
        - `llama3` (best overall for professional writing)
        - `mistral` (excellent for creative content)
        - `codellama` (great for technical roles)
        - `phi3` (fast and efficient)
        
        **To download a model, run in terminal:**
        ```bash
        ollama pull llama3
        ```
        
        **Wait for the download to complete** before refreshing this page.
        """
    
    return True, None

def initialize_session_state():
    """Initialize all session state variables"""
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = {
            'name': '',
            'title': '',
            'email': '',
            'phone': '',
            'location': '',
            'summary': '',
            'experience': [],
            'education': [],
            'skills': [],
            'projects': [],
            'certifications': []
        }

    if 'cover_letter_data' not in st.session_state:
        st.session_state.cover_letter_data = {
            'company': '',
            'position': '',
            'hiring_manager': '',
            'company_address': '',
            'job_description': '',
            'content': ''
        }

    if 'generated_resume' not in st.session_state:
        st.session_state.generated_resume = ''
    if 'generated_cover_letter' not in st.session_state:
        st.session_state.generated_cover_letter = ''
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = DEFAULT_MODEL
    if 'ollama_status' not in st.session_state:
        st.session_state.ollama_status = 'checking'
    if 'models_data' not in st.session_state:
        st.session_state.models_data = None
    if 'connection_error' not in st.session_state:
        st.session_state.connection_error = None
    if 'selected_template' not in st.session_state:
        st.session_state.selected_template = 'modern'
    if 'job_analysis' not in st.session_state:
        st.session_state.job_analysis = {}
    if 'skill_match' not in st.session_state:
        st.session_state.skill_match = {}
    if 'document_history' not in st.session_state:
        st.session_state.document_history = []
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'resume_completion' not in st.session_state:
        st.session_state.resume_completion = 0
    if 'cover_letter_completion' not in st.session_state:
        st.session_state.cover_letter_completion = 0
    if 'uploaded_resume' not in st.session_state:
        st.session_state.uploaded_resume = None
    if 'uploaded_cover_letter' not in st.session_state:
        st.session_state.uploaded_cover_letter = None
    if 'resume_filename' not in st.session_state:
        st.session_state.resume_filename = ''
    if 'cover_letter_filename' not in st.session_state:
        st.session_state.cover_letter_filename = ''

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_docx(docx_file) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

def extract_text_from_txt(txt_file) -> str:
    """Extract text from TXT file"""
    try:
        return txt_file.read().decode('utf-8')
    except Exception as e:
        st.error(f"Error reading TXT: {str(e)}")
        return ""

def parse_resume_text(text: str) -> Dict[str, Any]:
    """Parse resume text into structured data"""
    # Initialize parsed data
    parsed_data = {
        'name': '',
        'title': '',
        'email': '',
        'phone': '',
        'location': '',
        'summary': '',
        'experience': [],
        'education': [],
        'skills': [],
        'projects': [],
        'certifications': []
    }
    
    lines = text.split('\n')
    current_section = None
    current_experience = {}
    
    # Extract email and phone using regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    if emails:
        parsed_data['email'] = emails[0]
    if phones:
        parsed_data['phone'] = phones[0].replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # Simple parsing logic (can be enhanced with NLP)
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect sections
        if any(keyword in line.lower() for keyword in ['experience', 'work', 'employment']):
            current_section = 'experience'
            if current_experience and current_experience.get('title'):
                parsed_data['experience'].append(current_experience)
                current_experience = {}
        elif any(keyword in line.lower() for keyword in ['education', 'academic', 'university']):
            current_section = 'education'
        elif any(keyword in line.lower() for keyword in ['skills', 'technical', 'competencies']):
            current_section = 'skills'
        elif any(keyword in line.lower() for keyword in ['summary', 'objective', 'profile']):
            current_section = 'summary'
        elif any(keyword in line.lower() for keyword in ['projects', 'portfolio']):
            current_section = 'projects'
        elif any(keyword in line.lower() for keyword in ['certifications', 'certificates']):
            current_section = 'certifications'
        
        # Extract information based on current section
        if current_section == 'summary' and not parsed_data['summary']:
            parsed_data['summary'] = line
        elif current_section == 'skills':
            # Extract skills from comma-separated lists or bullet points
            skills = re.split(r'[,;•\n]', line)
            for skill in skills:
                skill = skill.strip()
                if skill and len(skill) > 2:
                    parsed_data['skills'].append(skill)
        elif current_section == 'experience':
            # Simple experience extraction (can be enhanced)
            if not current_experience.get('title') and len(line) < 100:
                # Likely a job title
                current_experience['title'] = line
            elif not current_experience.get('company') and '@' not in line and len(line) < 100:
                # Likely a company name
                current_experience['company'] = line
            else:
                # Description
                current_experience['description'] = current_experience.get('description', '') + line + '\n'
    
    # Add last experience if exists
    if current_experience and current_experience.get('title'):
        parsed_data['experience'].append(current_experience)
    
    # Clean up skills
    parsed_data['skills'] = list(set([skill.strip() for skill in parsed_data['skills'] if skill.strip()]))
    
    return parsed_data

def parse_cover_letter_text(text: str) -> Dict[str, Any]:
    """Parse cover letter text into structured data"""
    parsed_data = {
        'company': '',
        'position': '',
        'hiring_manager': '',
        'company_address': '',
        'content': text
    }
    
    lines = text.split('\n')
    
    # Extract company name (simple heuristic)
    for line in lines:
        if any(keyword in line.lower() for keyword in ['dear', 'to:', 'attention:']):
            # Look for company name in the same or next line
            if 'dear' in line.lower():
                parts = line.split('dear')[-1].strip()
                if parts and len(parts) < 50:
                    parsed_data['hiring_manager'] = parts
    
    # Try to extract position from first paragraph
    first_paragraph = ''
    for line in lines:
        if line.strip():
            first_paragraph = line
            break
    
    # Look for position keywords
    position_keywords = ['position', 'role', 'job', 'opportunity']
    for keyword in position_keywords:
        if keyword in first_paragraph.lower():
            # Extract the position (simple heuristic)
            start = first_paragraph.lower().find(keyword)
            if start != -1:
                end = first_paragraph.find('.', start)
                if end != -1:
                    parsed_data['position'] = first_paragraph[start:end+1].strip()
    
    return parsed_data

def generate_with_ollama(prompt: str, model_name: str = DEFAULT_MODEL, 
                        temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
    """Generate text using Ollama API with better error handling"""
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        with st.spinner("🧠 AI is crafting your content... This may take a moment."):
            response = requests.post(
                f"{OLLAMA_URL}/generate",
                json=payload,
                timeout=120  # 2 minutes timeout
            )
            
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '').strip()
        else:
            error_msg = f"❌ Error from Ollama: {response.status_code}"
            if response.text:
                error_msg += f"\nResponse: {response.text[:200]}..."
            st.error(error_msg)
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Connection failed! Ollama server might not be running.")
        st.info("💡 Please make sure Ollama is running in a separate terminal window.")
        return None
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out! Ollama server might be busy or overloaded.")
        st.info("💡 Try again in a few seconds or restart Ollama.")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None

def analyze_job_description(job_description: str) -> Dict[str, Any]:
    """Analyze job description to extract key information"""
    prompt = f"""
    Analyze this job description and extract:
    1. Key required skills and qualifications (list them)
    2. Main responsibilities (list them)
    3. Experience level required (entry-level, mid-level, senior, executive)
    4. Industry keywords for ATS optimization
    5. Company culture indicators
    6. Potential questions to address in cover letter
    
    Job Description:
    {job_description}
    
    Format your response as JSON with the following keys:
    - skills: array of strings
    - responsibilities: array of strings
    - experience_level: string
    - keywords: array of strings
    - culture_indicators: array of strings
    - cover_letter_questions: array of strings
    """
    
    try:
        response = generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.2)
        if response:
            # Try to parse as JSON
            try:
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                # If not valid JSON, try to extract information manually
                return {
                    "skills": [],
                    "responsibilities": [],
                    "experience_level": "unknown",
                    "keywords": [],
                    "culture_indicators": [],
                    "cover_letter_questions": []
                }
    except Exception as e:
        st.error(f"Error analyzing job description: {str(e)}")
    
    return {
        "skills": [],
        "responsibilities": [],
        "experience_level": "unknown",
        "keywords": [],
        "culture_indicators": [],
        "cover_letter_questions": []
    }

def match_skills_with_job(user_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
    """Match user skills with job requirements"""
    # Normalize skills for comparison
    user_skills_normalized = [skill.lower().strip() for skill in user_skills]
    job_skills_normalized = [skill.lower().strip() for skill in job_skills]
    
    # Find matching skills
    matched_skills = []
    missing_skills = []
    
    for job_skill in job_skills_normalized:
        if any(job_skill in user_skill or user_skill in job_skill 
               for user_skill in user_skills_normalized):
            # Find the original user skill that matches
            for user_skill in user_skills:
                if job_skill in user_skill.lower() or user_skill.lower() in job_skill:
                    matched_skills.append(user_skill)
                    break
        else:
            missing_skills.append(job_skill)
    
    # Calculate match percentage
    match_percentage = len(matched_skills) / len(job_skills) * 100 if job_skills else 0
    
    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "suggestions": missing_skills[:5]  # Top 5 missing skills to suggest
    }

def improve_uploaded_resume(resume_text: str, job_analysis: Optional[Dict] = None) -> Optional[str]:
    """Improve uploaded resume using AI"""
    job_specific_instructions = ""
    if job_analysis and job_analysis.get("skills"):
        job_specific_instructions = f"""
        Optimize this resume for a position requiring these skills: {', '.join(job_analysis['skills'][:10])}.
        Highlight experience and achievements that demonstrate these skills.
        Use these keywords naturally throughout the resume: {', '.join(job_analysis['keywords'][:8])}.
        """
    
    prompt = f"""
    Improve and optimize this resume for better impact and ATS compatibility:
    
    {job_specific_instructions}
    
    Original Resume:
    {resume_text}
    
    Instructions:
    1. Enhance the professional summary to be more impactful
    2. Improve bullet points to focus on achievements rather than responsibilities
    3. Add quantifiable metrics where possible (e.g., "increased by 25%", "managed team of 5")
    4. Use stronger action verbs (Led, Developed, Created, Implemented, etc.)
    5. Ensure proper formatting for ATS systems
    6. Optimize keyword density for relevant skills
    7. Maintain professional tone and structure
    8. Keep it concise but comprehensive
    9. Ensure consistent formatting and style
    10. Add any missing sections that would strengthen the resume
    
    Output the complete improved resume with clear section headers.
    """
    
    return generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.3)

def improve_uploaded_cover_letter(cover_letter_text: str, job_description: str, company_info: Dict[str, str]) -> Optional[str]:
    """Improve uploaded cover letter using AI"""
    prompt = f"""
    Improve and optimize this cover letter for better impact:
    
    Company Information:
    Company: {company_info['company']}
    Position: {company_info['position']}
    Hiring Manager: {company_info['hiring_manager'] or 'Hiring Team'}
    
    Job Description:
    {job_description}
    
    Original Cover Letter:
    {cover_letter_text}
    
    Instructions:
    1. Strengthen the opening to grab attention immediately
    2. Better align the content with the job requirements
    3. Add specific examples and achievements that match the role
    4. Improve the flow and transitions between paragraphs
    5. Add more enthusiasm and genuine interest in the company
    6. Strengthen the closing with a clear call to action
    7. Ensure proper business letter format
    8. Make it more personalized and less generic
    9. Optimize length to 300-400 words maximum
    10. Check for and fix any grammar or style issues
    
    Output the complete improved cover letter.
    """
    
    return generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.4)

def generate_resume_content(resume_data: Dict[str, Any], template_style: str = "modern", job_analysis: Optional[Dict] = None) -> Optional[str]:
    """Generate resume content using Ollama with job-specific optimization"""
    # Build a more sophisticated prompt
    job_specific_instructions = ""
    if job_analysis and job_analysis.get("skills"):
        job_specific_instructions = f"""
        Optimize this resume for a position requiring these skills: {', '.join(job_analysis['skills'][:10])}.
        Highlight experience and achievements that demonstrate these skills.
        Use these keywords naturally throughout the resume: {', '.join(job_analysis['keywords'][:8])}.
        """
    
    prompt = f"""
    Create a professional, ATS-friendly resume for the following candidate using a {template_style} style:
    
    {job_specific_instructions}
    
    Candidate Information:
    Name: {resume_data['name']}
    Professional Title: {resume_data['title']}
    Contact: {resume_data['email']} | {resume_data['phone']} | {resume_data['location']}

    Professional Summary:
    {resume_data['summary']}

    Work Experience:
    {' '.join([f"- {exp['title']} at {exp['company']} ({exp['duration']}): {exp['description']}" for exp in resume_data['experience']])}

    Education:
    {' '.join([f"- {edu['degree']} from {edu['institution']} ({edu['year']}): {edu['details']}" for edu in resume_data['education']])}

    Skills:
    {', '.join(resume_data['skills'])}

    Projects:
    {' '.join([f"- {proj['name']}: {proj['description']}" for proj in resume_data['projects']])}

    Certifications:
    {' '.join([f"- {cert['name']} ({cert['issuer']}, {cert['year']})" for cert in resume_data['certifications']])}

    Instructions:
    1. Format as a professional resume with clear section headers (## for main sections, ### for subsections)
    2. Use bullet points for lists and achievements
    3. Make it ATS-friendly (no tables, no columns, standard fonts)
    4. Include quantifiable achievements where possible
    5. Use action verbs (Managed, Developed, Led, Created, etc.)
    6. Keep it concise but comprehensive (1-2 pages max)
    7. Professional tone suitable for job applications
    8. Include all sections even if some have minimal content
    9. Format dates consistently (Month Year - Month Year)
    10. Highlight key skills and achievements prominently
    11. If job-specific information is provided, tailor the content to highlight relevant experience
    12. Use industry-specific terminology appropriate for the target role
    13. Include a skills section that showcases both technical and soft skills
    14. For each experience, focus on achievements rather than just responsibilities
    """
    
    return generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.3)

def generate_cover_letter(job_description: str, resume_data: Dict[str, Any], company_info: Dict[str, str], job_analysis: Optional[Dict] = None) -> Optional[str]:
    """Generate cover letter using Ollama with job-specific personalization"""
    # Build a more sophisticated prompt
    job_specific_questions = ""
    if job_analysis and job_analysis.get("cover_letter_questions"):
        job_specific_questions = f"""
        Address these specific questions or points in your cover letter:
        {', '.join(job_analysis['cover_letter_questions'][:3])}
        """
    
    prompt = f"""
    Create a professional, personalized cover letter for the following position:
    
    {job_specific_questions}
    
    Company Information:
    Company: {company_info['company']}
    Position: {company_info['position']}
    Hiring Manager: {company_info['hiring_manager'] or 'Hiring Team'}
    Company Address: {company_info['company_address'] or 'Address not provided'}

    Candidate Information:
    Name: {resume_data['name']}
    Current Title: {resume_data['title']}
    Contact: {resume_data['email']} | {resume_data['phone']}

    Professional Background:
    {resume_data['summary']}

    Relevant Experience:
    {' '.join([f"{exp['title']} at {exp['company']}: {exp['description']}" for exp in resume_data['experience'][:2]])}

    Job Description to Match:
    {job_description}

    Instructions:
    1. Write a formal business letter with proper structure:
       - Date
       - Hiring Manager/Company Address
       - Salutation (Dear [Name] or Dear Hiring Team)
       - Introduction paragraph
       - 2-3 body paragraphs highlighting relevant experience
       - Closing paragraph
       - Professional sign-off
    2. Personalize the letter for this specific company and role
    3. Show genuine enthusiasm and research about the company
    4. Highlight 2-3 most relevant skills/experiences that match the job description
    5. Quantify achievements where possible (e.g., "increased efficiency by 25%")
    6. Explain why you're interested in this specific role at this company
    7. Keep it to one page maximum (300-400 words)
    8. Use professional tone and business language
    9. Close with a call to action (request for interview)
    10. Format with proper spacing and professional structure
    11. If job-specific questions are provided, address them directly
    12. Reference specific aspects of the company that appeal to you
    13. Connect your career goals with the company's mission or values
    14. Avoid generic phrases and be specific about your qualifications
    """
    
    return generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.4)

def create_pdf(content: str, filename: str, document_type: str = "resume") -> str:
    """Create PDF from content and return base64 encoded string"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='Title',
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.navy,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='Heading1',
        fontSize=16,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.navy,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='Heading2',
        fontSize=14,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=4,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='BodyText',
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=14,
        fontName='Helvetica'
    ))
    
    styles.add(ParagraphStyle(
        name='ContactInfo',
        fontSize=11,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.darkblue,
        fontName='Helvetica'
    ))
    
    styles.add(ParagraphStyle(
        name='Bullet',
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=4,
        leftIndent=20,
        bulletIndent=10,
        bulletFontName='Helvetica',
        bulletFontSize=11
    ))
    
    # Parse content into sections
    story = []
    
    if document_type == "resume":
        # Split content into lines and process
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('# '):
                story.append(Paragraph(line[2:], styles['Title']))
                story.append(Spacer(1, 12))
            elif line.startswith('## '):
                story.append(Paragraph(line[3:], styles['Heading1']))
                story.append(Spacer(1, 6))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], styles['Heading2']))
                story.append(Spacer(1, 4))
            elif line.startswith('- '):
                story.append(Paragraph(f"• {line[2:]}", styles['BodyText']))
            else:
                story.append(Paragraph(line, styles['BodyText']))
                
    else:  # Cover letter
        # Split into paragraphs
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            if any(para.startswith(prefix) for prefix in ['Dear', 'Sincerely', 'Best regards', 'Thank you']):
                story.append(Paragraph(para, styles['BodyText']))
                story.append(Spacer(1, 12))
            elif para.startswith('# '):
                story.append(Paragraph(para[2:], styles['Title']))
                story.append(Spacer(1, 12))
            else:
                story.append(Paragraph(para, styles['BodyText']))
                story.append(Spacer(1, 6))
    
    doc.build(story)
    buffer.seek(0)
    
    # Encode PDF to base64 for download
    pdf_bytes = buffer.getvalue()
    return base64.b64encode(pdf_bytes).decode()

def save_to_history(document_type: str, content: str, metadata: Dict[str, Any]):
    """Save document to history"""
    timestamp = datetime.now().isoformat()
    history_item = {
        "type": document_type,
        "content": content,
        "metadata": metadata,
        "timestamp": timestamp
    }
    st.session_state.document_history.append(history_item)
    
    # Keep only the last 10 items
    if len(st.session_state.document_history) > 10:
        st.session_state.document_history = st.session_state.document_history[-10:]

def calculate_resume_completion(resume_data: Dict[str, Any]) -> int:
    """Calculate percentage of resume completion"""
    required_fields = ['name', 'title', 'email', 'phone', 'location']
    filled_required = sum(1 for field in required_fields if resume_data.get(field, '').strip())
    
    required_score = (filled_required / len(required_fields)) * 40
    
    # Check for summary
    summary_score = 10 if resume_data.get('summary', '').strip() else 0
    
    # Check for experience
    experience_score = min(20, len(resume_data.get('experience', [])) * 10)
    
    # Check for education
    education_score = min(10, len(resume_data.get('education', [])) * 5)
    
    # Check for skills
    skills_score = min(20, len(resume_data.get('skills', [])) * 2)
    
    return int(required_score + summary_score + experience_score + education_score + skills_score)

def calculate_cover_letter_completion(cover_letter_data: Dict[str, Any]) -> int:
    """Calculate percentage of cover letter completion"""
    required_fields = ['company', 'position', 'job_description']
    filled_required = sum(1 for field in required_fields if cover_letter_data.get(field, '').strip())
    
    required_score = (filled_required / len(required_fields)) * 60
    
    # Check for hiring manager
    hiring_manager_score = 20 if cover_letter_data.get('hiring_manager', '').strip() else 0
    
    # Check for company address
    address_score = 20 if cover_letter_data.get('company_address', '').strip() else 0
    
    return int(required_score + hiring_manager_score + address_score)

def show_ollama_setup_page():
    """Show the setup page when Ollama is not running or has no models"""
    st.markdown('<h2 class="section-header">🚀 Setup Required</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="connection-check">', unsafe_allow_html=True)
    
    if st.session_state.ollama_status == 'not_running':
        st.error("❌ **Ollama Server Not Running**")
        st.markdown("""
        To use CareerCraft AI, you need to have Ollama running locally on your machine.
        
        Ollama allows you to run large language models completely offline without sending your data to external servers.
        """)
    elif st.session_state.ollama_status == 'no_models':
        st.warning("⚠️ **No Models Found**")
        st.markdown(st.session_state.connection_error)
    else:
        st.info("🔍 **Checking Ollama Connection...**")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Try to start Ollama automatically
    if st.session_state.ollama_status == 'not_running':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Try to Start Ollama Service", type="secondary", use_container_width=True):
                success, message = try_start_ollama()
                if success:
                    st.success(message)
                    st.session_state.ollama_status = 'checking'
                    st.rerun()
                else:
                    if message:
                        st.error(message)
                    st.info("💡 Manual startup may be required. Follow the instructions below.")
        with col2:
            if st.button("🔃 Check Connection Again", type="primary", use_container_width=True):
                st.session_state.ollama_status = 'checking'
                st.rerun()
    
    # Show installation instructions
    st.markdown('<div class="install-instructions">', unsafe_allow_html=True)
    st.markdown("### 📋 Installation Guide")
    st.markdown(get_installation_instructions())
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick start summary
    st.markdown("### ⚡ Quick Start Summary")
    st.markdown("""
    1. **Install Ollama** from https://ollama.com
    2. **Start the server** in a terminal: `ollama serve`
    3. **Download a model** in a new terminal: `ollama pull llama3`
    4. **Keep the terminal window open** while using this application
    5. **Refresh this page** to start creating your resume!
    """)
    
    # Common issues troubleshooting
    with st.expander("🔧 Troubleshooting Common Issues"):
        st.markdown("""
        **Connection Issues:**
        - Make sure you have a terminal window running `ollama serve`
        - Check that no other application is using port 11434
        - Restart Ollama if it's been running for a long time
        - Try `localhost:11434` in your browser to verify the server is running
        
        **Model Issues:**
        - If you get "model not found" errors, download the model first
        - Use `ollama list` to see available models
        - Try `ollama pull llama3:latest` for the most recent version
        - Large models (7B+ parameters) require 8GB+ RAM
        
        **Performance Issues:**
        - Close other memory-intensive applications
        - Use smaller models like `phi3` or `llama3:8b` if you have limited RAM
        - Generation may take 30-60 seconds for the first request
        - Subsequent requests are usually faster
        """)
    
    # Verification section
    st.markdown("### ✅ Verification")
    st.markdown("After following the steps above, click the button below to verify your setup:")
    
    if st.button("✅ Verify Ollama Setup", type="primary", use_container_width=True):
        st.session_state.ollama_status = 'checking'
        st.rerun()
    
    # Footer with helpful links
    st.markdown("---")
    st.markdown("""
    **Helpful Links:**
    - [Ollama Documentation](https://ollama.com/docs)
    - [Available Models](https://ollama.com/library)
    - [Troubleshooting Guide](https://github.com/ollama/ollama/blob/main/docs/troubleshooting.md)
    """)

def show_main_application():
    """Show the main application when Ollama is properly configured"""
    # Sidebar for model selection and settings
    with st.sidebar:
        st.markdown("### 🤖 AI Model Settings")
        
        # Display available models
        if st.session_state.models_data and 'models' in st.session_state.models_data:
            available_models = [model['name'].split(':')[0] for model in st.session_state.models_data['models']]
            
            selected_model = st.selectbox(
                "Select AI Model", 
                available_models, 
                index=available_models.index(st.session_state.selected_model) if st.session_state.selected_model in available_models else 0,
                help="Different models have different strengths. llama3 works well for most resume tasks."
            )
            st.session_state.selected_model = selected_model
            
            # Show model info
            model_info = next((model for model in st.session_state.models_data['models'] if model['name'].startswith(selected_model)), None)
            if model_info:
                st.markdown(f'<div class="sidebar-status status-running">', unsafe_allow_html=True)
                st.markdown(f"**Model Size:** {model_info.get('size', 'Unknown')}")
                st.markdown(f"**Modified:** {model_info.get('modified_at', 'Unknown')}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ No models detected. Please download a model using `ollama pull llama3`")
        
        st.markdown("---")
        st.markdown("### 📋 Quick Actions")
        if st.button("🔄 Reset All Data", use_container_width=True):
            initialize_session_state()
            st.success("✅ All data reset successfully!")
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info("""
        **CareerCraft AI** uses local AI models via Ollama to generate professional resumes and cover letters without sending your data to external servers.
        
        **Privacy First:** All processing happens on your local machine.
        
        **No API Keys:** No subscriptions or external services required.
        """)
        
        # Connection status indicator
        st.markdown("### 🔗 Connection Status")
        st.markdown(f'<div class="sidebar-status status-running">', unsafe_allow_html=True)
        st.markdown("✅ **Ollama Connected**")
        st.markdown(f"🧠 **Active Model:** {st.session_state.selected_model}")
        if st.session_state.models_data and 'models' in st.session_state.models_data:
            st.markdown(f"📦 **Models Available:** {len(st.session_state.models_data['models'])}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Document history
        if st.session_state.document_history:
            st.markdown("---")
            st.markdown("### 📚 Document History")
            for i, item in enumerate(reversed(st.session_state.document_history[-5:])):
                with st.expander(f"{item['type'].title()} - {item['metadata'].get('title', 'Untitled')}"):
                    st.markdown(f"**Created:** {item['timestamp']}")
                    st.markdown(f"**Type:** {item['type'].title()}")
                    if st.button(f"Use This {item['type'].title()}", key=f"use_history_{i}"):
                        if item['type'] == 'resume':
                            st.session_state.generated_resume = item['content']
                        else:
                            st.session_state.generated_cover_letter = item['content']
                        st.success(f"✅ Loaded {item['type']} from history!")
                        st.rerun()
    
    # Main tabs with progress indicators
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Resume Builder", "✉️ Cover Letter", "📁 Upload & Edit", "🎨 Templates & Export", "📊 Analytics"])
    
    with tab1:
        st.markdown('<h2 class="section-header">Resume Builder</h2>', unsafe_allow_html=True)
        
        # Progress indicator
        st.session_state.resume_completion = calculate_resume_completion(st.session_state.resume_data)
        st.markdown(f"""
        <div class="progress-container">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Resume Completion</span>
                <span>{st.session_state.resume_completion}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {st.session_state.resume_completion}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Personal Information
        with st.expander("👤 Personal Information", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.resume_data['name'] = st.text_input("Full Name*", st.session_state.resume_data['name'], 
                                                                   placeholder="John Doe")
                st.session_state.resume_data['email'] = st.text_input("Email Address*", st.session_state.resume_data['email'],
                                                                     placeholder="john.doe@email.com")
            with col2:
                st.session_state.resume_data['title'] = st.text_input("Professional Title*", st.session_state.resume_data['title'],
                                                                      placeholder="Senior Software Engineer")
                st.session_state.resume_data['phone'] = st.text_input("Phone Number*", st.session_state.resume_data['phone'],
                                                                      placeholder="(555) 123-4567")
            st.session_state.resume_data['location'] = st.text_input("Location (City, State)*", st.session_state.resume_data['location'],
                                                                     placeholder="San Francisco, CA")
        
        # Professional Summary
        with st.expander("🎯 Professional Summary"):
            st.session_state.resume_data['summary'] = st.text_area(
                "Write a brief professional summary (2-3 sentences)",
                st.session_state.resume_data['summary'],
                height=120,
                placeholder="Experienced software engineer with 5+ years in full-stack development. Proven track record of delivering scalable web applications and leading engineering teams. Passionate about building user-centric solutions and mentoring junior developers."
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✨ Generate Summary with AI", use_container_width=True):
                    if st.session_state.resume_data['name'] and st.session_state.resume_data['title']:
                        prompt = f"""
                        Generate a professional summary for {st.session_state.resume_data['name']}, 
                        a {st.session_state.resume_data['title']}. Make it concise (2-3 sentences), 
                        highlighting key skills, experience level, and career goals. Use professional language suitable for a resume.
                        Focus on achievements and value proposition.
                        """
                        summary = generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.4)
                        if summary:
                            st.session_state.resume_data['summary'] = summary
                            st.success("✅ Summary generated successfully!")
                    else:
                        st.warning("⚠️ Please enter your name and professional title first.")
            with col2:
                if st.button("🔍 Improve Existing Summary", use_container_width=True):
                    if st.session_state.resume_data['summary']:
                        prompt = f"""
                        Improve this professional summary to make it more impactful and concise:
                        "{st.session_state.resume_data['summary']}"
                        
                        Requirements:
                        - Keep it to 2-3 sentences maximum
                        - Use strong action verbs
                        - Highlight quantifiable achievements if possible
                        - Make it ATS-friendly and professional
                        - Focus on value proposition to employers
                        """
                        improved_summary = generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.3)
                        if improved_summary:
                            st.session_state.resume_data['summary'] = improved_summary
                            st.success("✅ Summary improved successfully!")
                    else:
                        st.warning("⚠️ Please write or generate a summary first.")
        
        # Experience Section
        with st.expander("💼 Work Experience"):
            # Display existing experience
            for i, exp in enumerate(st.session_state.resume_data['experience']):
                st.markdown(f"### Experience {i+1}")
                col1, col2 = st.columns(2)
                with col1:
                    exp['title'] = st.text_input(f"Job Title*", exp['title'], key=f"title_{i}")
                    exp['company'] = st.text_input(f"Company*", exp['company'], key=f"company_{i}")
                with col2:
                    exp['duration'] = st.text_input(f"Duration*", exp['duration'], key=f"duration_{i}", 
                                                  placeholder="Jan 2020 - Present")
                exp['description'] = st.text_area(f"Description*", exp['description'], key=f"desc_{i}", height=100,
                                                placeholder="• Led a team of 5 developers to build a scalable web application\n• Increased system performance by 40% through optimization\n• Implemented CI/CD pipeline reducing deployment time by 60%")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✨ Improve Description", key=f"improve_exp_{i}", use_container_width=True):
                        if exp['title'] and exp['company']:
                            prompt = f"""
                            Improve this work experience description for a {exp['title']} at {exp['company']}:
                            "{exp['description']}"
                            
                            Requirements:
                            - Write 3-5 bullet points with specific achievements
                            - Use action verbs (Led, Developed, Managed, Created, etc.)
                            - Include quantifiable results where possible
                            - Focus on skills relevant to {st.session_state.resume_data['title']}
                            - Make it concise and professional
                            - ATS-friendly format
                            """
                            improved_desc = generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.4)
                            if improved_desc:
                                exp['description'] = improved_desc
                                st.success("✅ Experience description improved successfully!")
                        else:
                            st.warning("⚠️ Please fill in job title and company first.")
                
                with col2:
                    if st.button(f"🗑️ Remove Experience {i+1}", key=f"remove_exp_{i}", use_container_width=True):
                        st.session_state.resume_data['experience'].pop(i)
                        st.rerun()
                
                st.markdown("---")
            
            if st.button("➕ Add Experience", type="secondary", use_container_width=True):
                st.session_state.resume_data['experience'].append({
                    'title': '',
                    'company': '',
                    'duration': '',
                    'description': ''
                })
                st.rerun()
            
            if st.button("✨ Generate Experience Description", type="primary", use_container_width=True):
                if st.session_state.resume_data['experience']:
                    latest_exp = st.session_state.resume_data['experience'][-1]
                    if latest_exp['title'] and latest_exp['company']:
                        prompt = f"""
                        Generate a professional work experience description for:
                        Position: {latest_exp['title']}
                        Company: {latest_exp['company']}
                        Duration: {latest_exp['duration']}
                        
                        Requirements:
                        - Write 3-5 bullet points with specific achievements
                        - Use action verbs (Led, Developed, Managed, Created, etc.)
                        - Include quantifiable results where possible
                        - Focus on skills relevant to {st.session_state.resume_data['title']}
                        - Make it concise and professional
                        - ATS-friendly format
                        """
                        description = generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.4)
                        if description:
                            latest_exp['description'] = description
                            st.success("✅ Experience description generated successfully!")
                    else:
                        st.warning("⚠️ Please fill in job title and company first.")
                else:
                    st.warning("⚠️ Please add an experience first.")
        
        # Skills Section
        with st.expander("⭐ Skills"):
            skills_input = st.text_input("Add skills (comma-separated)", 
                                       placeholder="Python, Data Analysis, Project Management, Communication, Leadership")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Add Skills", use_container_width=True):
                    if skills_input:
                        new_skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
                        # Remove duplicates
                        existing_skills = set(st.session_state.resume_data['skills'])
                        new_unique_skills = [skill for skill in new_skills if skill not in existing_skills]
                        
                        if new_unique_skills:
                            st.session_state.resume_data['skills'].extend(new_unique_skills)
                            st.success(f"✅ Added {len(new_unique_skills)} new skills!")
                        else:
                            st.info("ℹ️ All skills already exist in your list.")
            with col2:
                if st.button("✨ Generate Relevant Skills", use_container_width=True):
                    if st.session_state.resume_data['title']:
                        prompt = f"""
                        Generate 8-12 relevant technical and soft skills for a {st.session_state.resume_data['title']}.
                        Format as a comma-separated list.
                        Include both technical skills and professional soft skills.
                        Make them specific and relevant to current industry standards.
                        """
                        skills_text = generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.4)
                        if skills_text:
                            # Extract skills from the response
                            skills_list = [skill.strip() for skill in re.split(r'[,\n]', skills_text) if skill.strip()]
                            # Clean up and filter
                            cleaned_skills = []
                            for skill in skills_list:
                                # Remove numbers, bullets, and extra text
                                skill = re.sub(r'^[\d\-\*•]+\s*', '', skill)
                                skill = re.sub(r'[^\w\s\-/]', '', skill)
                                if skill and len(skill) > 2:
                                    cleaned_skills.append(skill)
                            
                            if cleaned_skills:
                                # Add only unique skills
                                existing_skills = set(st.session_state.resume_data['skills'])
                                new_skills = [skill for skill in cleaned_skills if skill not in existing_skills]
                                st.session_state.resume_data['skills'].extend(new_skills[:8])  # Limit to 8 new skills
                                st.success(f"✅ Generated {min(8, len(new_skills))} relevant skills!")
                    else:
                        st.warning("⚠️ Please enter your professional title first.")
            
            # Display and manage skills
            if st.session_state.resume_data['skills']:
                st.markdown("**Your Skills:**")
                skills_cols = st.columns(min(4, len(st.session_state.resume_data['skills'])))
                for i, skill in enumerate(st.session_state.resume_data['skills']):
                    with skills_cols[i % 4]:
                        st.markdown(f"• **{skill}**")
                        if st.button(f"❌", key=f"remove_skill_{i}", help=f"Remove {skill}"):
                            st.session_state.resume_data['skills'].pop(i)
                            st.rerun()
                
                if st.button("🗑️ Clear All Skills", type="secondary", use_container_width=True):
                    st.session_state.resume_data['skills'] = []
                    st.success("✅ All skills cleared!")
        
        # Generate Resume Button
        if st.button("🚀 Generate Professional Resume", type="primary", use_container_width=True):
            # Validate required fields
            required_fields = ['name', 'title', 'email', 'phone', 'location']
            missing_fields = [field for field in required_fields if not st.session_state.resume_data[field].strip()]
            
            if missing_fields:
                st.warning(f"⚠️ Please fill in all required fields: {', '.join(missing_fields)}")
            elif not st.session_state.resume_data['experience']:
                st.warning("⚠️ Please add at least one work experience")
            elif not st.session_state.resume_data['skills']:
                st.warning("⚠️ Please add at least some skills")
            else:
                with st.spinner("🎨 Creating your professional resume... This may take 30-60 seconds."):
                    resume_content = generate_resume_content(st.session_state.resume_data, st.session_state.selected_template, st.session_state.job_analysis)
                    if resume_content:
                        st.session_state.generated_resume = resume_content
                        save_to_history("resume", resume_content, {"title": f"{st.session_state.resume_data['name']} Resume"})
                        st.success("✅ Resume generated successfully!")
                        st.balloons()
        
        # Display generated resume
        if st.session_state.generated_resume:
            st.markdown("---")
            st.markdown('<h3 class="section-header">Generated Resume</h3>', unsafe_allow_html=True)
            
            # Metrics and actions
            col1, col2, col3 = st.columns(3)
            with col1:
                word_count = len(st.session_state.generated_resume.split())
                st.metric("Word Count", f"{word_count}")
            with col2:
                section_count = st.session_state.generated_resume.count('##') - 1  # Subtract title
                st.metric("Sections", f"{max(0, section_count)}")
            with col3:
                st.metric("AI Model", st.session_state.selected_model)
            
            # Display in expandable section
            with st.expander("📄 View Generated Resume", expanded=True):
                st.markdown(st.session_state.generated_resume)
            
            # Improvement options
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✨ Improve Resume Content", use_container_width=True):
                    with st.spinner("🎯 Improving your resume content..."):
                        prompt = f"""
                        Improve this resume content to make it more professional, concise, and impactful:
                        {st.session_state.generated_resume}
                        
                        Focus on:
                        - Making it more ATS-friendly
                        - Improving action verbs and quantifiable achievements
                        - Better formatting and structure
                        - More professional language
                        - Concise but comprehensive content
                        """
                        improved_resume = generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.3)
                        if improved_resume:
                            st.session_state.generated_resume = improved_resume
                            st.success("✅ Resume improved successfully!")
            with col2:
                if st.button("🎯 Optimize for ATS", use_container_width=True):
                    with st.spinner("🔍 Optimizing for Applicant Tracking Systems..."):
                        prompt = f"""
                        Analyze and optimize this resume for Applicant Tracking Systems (ATS):
                        {st.session_state.generated_resume}
                        
                        Requirements:
                        - Ensure proper keyword density for {st.session_state.resume_data['title']} roles
                        - Fix any formatting issues that might confuse ATS
                        - Add relevant industry keywords
                        - Maintain professional structure
                        - Keep it human-readable while being ATS-friendly
                        - Output the complete optimized resume
                        """
                        optimized_resume = generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.2)
                        if optimized_resume:
                            st.session_state.generated_resume = optimized_resume
                            st.success("✅ Resume optimized for ATS successfully!")
    
    with tab2:
        st.markdown('<h2 class="section-header">Cover Letter Generator</h2>', unsafe_allow_html=True)
        
        # Progress indicator
        st.session_state.cover_letter_completion = calculate_cover_letter_completion(st.session_state.cover_letter_data)
        st.markdown(f"""
        <div class="progress-container">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Cover Letter Completion</span>
                <span>{st.session_state.cover_letter_completion}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {st.session_state.cover_letter_completion}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Company Information
        with st.expander("🏢 Company & Position Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.cover_letter_data['company'] = st.text_input(
                    "Company Name*", 
                    st.session_state.cover_letter_data['company'],
                    placeholder="Google, Microsoft, Tesla, etc."
                )
                st.session_state.cover_letter_data['position'] = st.text_input(
                    "Position Title*", 
                    st.session_state.cover_letter_data['position'],
                    placeholder="Senior Software Engineer, Marketing Manager, Data Scientist"
                )
            with col2:
                st.session_state.cover_letter_data['hiring_manager'] = st.text_input(
                    "Hiring Manager Name (optional)", 
                    st.session_state.cover_letter_data['hiring_manager'],
                    placeholder="John Smith or 'Hiring Team'"
                )
                st.session_state.cover_letter_data['company_address'] = st.text_input(
                    "Company Address (optional)", 
                    st.session_state.cover_letter_data['company_address'],
                    placeholder="123 Main St, San Francisco, CA 94105"
                )
        
        # Job Description Input
        with st.expander("📋 Job Description", expanded=True):
            st.session_state.cover_letter_data['job_description'] = st.text_area(
                "Paste the complete job description here*",
                st.session_state.cover_letter_data['job_description'],
                height=200,
                placeholder="""We are seeking a talented Software Engineer to join our innovative team at [Company Name]. 

Key Responsibilities:
- Design and implement scalable web applications
- Collaborate with product and design teams to define feature specifications
- Write clean, maintainable, and well-tested code
- Participate in code reviews and mentor junior engineers

Requirements:
- 3+ years of experience in software development
- Proficiency in Python, JavaScript, and modern web frameworks
- Experience with cloud platforms (AWS, GCP, or Azure)
- Strong problem-solving skills and attention to detail
- Excellent communication and teamwork abilities

Preferred Qualifications:
- Experience with machine learning or AI systems
- Contributions to open-source projects
- Advanced degree in Computer Science or related field"""
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✨ Analyze Job Description", use_container_width=True):
                    if st.session_state.cover_letter_data['job_description']:
                        with st.spinner("🔍 Analyzing job description..."):
                            st.session_state.job_analysis = analyze_job_description(st.session_state.cover_letter_data['job_description'])
                            if st.session_state.job_analysis:
                                st.success("✅ Job description analyzed successfully!")
                    else:
                        st.warning("⚠️ Please paste the job description first.")
            
            if st.session_state.job_analysis:
                with st.expander("📊 Job Description Analysis", expanded=False):
                    if st.session_state.job_analysis.get("skills"):
                        st.markdown("**Key Required Skills:**")
                        for skill in st.session_state.job_analysis["skills"]:
                            st.markdown(f"- {skill}")
                    
                    if st.session_state.job_analysis.get("responsibilities"):
                        st.markdown("**Main Responsibilities:**")
                        for resp in st.session_state.job_analysis["responsibilities"]:
                            st.markdown(f"- {resp}")
                    
                    if st.session_state.job_analysis.get("experience_level"):
                        st.markdown(f"**Experience Level:** {st.session_state.job_analysis['experience_level']}")
                    
                    if st.session_state.job_analysis.get("keywords"):
                        st.markdown("**Keywords for ATS:**")
                        keywords_str = ", ".join(st.session_state.job_analysis["keywords"])
                        st.markdown(f"*{keywords_str}*")
                    
                    if st.session_state.job_analysis.get("cover_letter_questions"):
                        st.markdown("**Points to Address in Cover Letter:**")
                        for question in st.session_state.job_analysis["cover_letter_questions"]:
                            st.markdown(f"- {question}")
        
        # Generate Cover Letter
        if st.button("✍️ Generate Cover Letter", type="primary", use_container_width=True):
            # Validate required fields
            if not st.session_state.cover_letter_data['company'] or not st.session_state.cover_letter_data['position']:
                st.warning("⚠️ Please enter company name and position title first.")
            elif not st.session_state.cover_letter_data['job_description']:
                st.warning("⚠️ Please paste the job description.")
            elif not st.session_state.resume_data['name'] or not st.session_state.resume_data['title']:
                st.warning("⚠️ Please complete your resume information first (name and title required).")
            else:
                with st.spinner("✍️ Crafting your personalized cover letter... This may take 30-60 seconds."):
                    company_info = {
                        'company': st.session_state.cover_letter_data['company'],
                        'position': st.session_state.cover_letter_data['position'],
                        'hiring_manager': st.session_state.cover_letter_data['hiring_manager'],
                        'company_address': st.session_state.cover_letter_data['company_address']
                    }
                    
                    cover_letter = generate_cover_letter(
                        st.session_state.cover_letter_data['job_description'], 
                        st.session_state.resume_data, 
                        company_info,
                        st.session_state.job_analysis
                    )
                    if cover_letter:
                        st.session_state.generated_cover_letter = cover_letter
                        save_to_history("cover_letter", cover_letter, {"title": f"Cover Letter for {st.session_state.cover_letter_data['company']}"})
                        st.success("✅ Cover letter generated successfully!")
                        st.balloons()
        
        # Display generated cover letter
        if st.session_state.generated_cover_letter:
            st.markdown("---")
            st.markdown('<h3 class="section-header">Generated Cover Letter</h3>', unsafe_allow_html=True)
            
            # Display metrics
            col1, col2 = st.columns(2)
            with col1:
                word_count = len(st.session_state.generated_cover_letter.split())
                st.metric("Word Count", f"{word_count}")
            with col2:
                st.metric("Target Company", st.session_state.cover_letter_data['company'])
            
            with st.expander("📄 View Generated Cover Letter", expanded=True):
                st.markdown(st.session_state.generated_cover_letter)
            
            # Improvement options
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✨ Improve Cover Letter", use_container_width=True):
                    with st.spinner("🎯 Improving your cover letter..."):
                        prompt = f"""
                        Improve this cover letter to make it more compelling and professional:
                        {st.session_state.generated_cover_letter}
                        
                        Focus on:
                        - Stronger opening and closing paragraphs
                        - Better connection between candidate skills and job requirements
                        - More specific examples and achievements
                        - Professional tone and flow
                        - Concise but impactful content
                        """
                        improved_letter = generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.3)
                        if improved_letter:
                            st.session_state.generated_cover_letter = improved_letter
                            st.success("✅ Cover letter improved successfully!")
            with col2:
                if st.button("🎯 Personalize Further", use_container_width=True):
                    with st.spinner("🎯 Adding personal touches..."):
                        prompt = f"""
                        Personalize this cover letter further by:
                        1. Adding a specific reason why the candidate is interested in {st.session_state.cover_letter_data['company']}
                        2. Including a relevant personal connection or research about the company
                        3. Making the tone more enthusiastic and genuine
                        4. Adding a memorable closing statement
                        
                        Cover Letter:
                        {st.session_state.generated_cover_letter}
                        """
                        personalized_letter = generate_with_ollama(prompt, st.session_state.selected_model, temperature=0.4)
                        if personalized_letter:
                            st.session_state.generated_cover_letter = personalized_letter
                            st.success("✅ Cover letter personalized successfully!")
    
    with tab3:
        st.markdown('<h2 class="section-header">Upload & Edit Documents</h2>', unsafe_allow_html=True)
        
        # Resume Upload Section
        st.markdown("### 📄 Upload Resume")
        st.markdown("Upload your existing resume to improve and optimize it with AI")
        
        # File upload for resume
        uploaded_resume_file = st.file_uploader(
            "Choose a resume file",
            type=['pdf', 'docx', 'txt'],
            key="resume_upload",
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_resume_file is not None:
            # Display file info
            st.markdown(f"""
            <div class="file-info">
                <strong>Uploaded File:</strong> {uploaded_resume_file.name}<br>
                <strong>File Size:</strong> {uploaded_resume_file.size / 1024:.1f} KB<br>
                <strong>File Type:</strong> {uploaded_resume_file.type}
            </div>
            """, unsafe_allow_html=True)
            
            # Extract text based on file type
            if uploaded_resume_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_resume_file)
            elif uploaded_resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(uploaded_resume_file)
            else:  # TXT file
                resume_text = extract_text_from_txt(uploaded_resume_file)
            
            if resume_text:
                st.session_state.uploaded_resume = resume_text
                st.session_state.resume_filename = uploaded_resume_file.name
                
                # Parse the resume
                parsed_resume = parse_resume_text(resume_text)
                
                # Update session state with parsed data
                for key, value in parsed_resume.items():
                    if key in st.session_state.resume_data and value:
                        st.session_state.resume_data[key] = value
                
                st.success("✅ Resume uploaded and parsed successfully!")
                
                # Display parsed information
                with st.expander("📊 Parsed Resume Information", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Contact Information:**")
                        st.markdown(f"- **Name:** {parsed_resume.get('name', 'Not found')}")
                        st.markdown(f"- **Email:** {parsed_resume.get('email', 'Not found')}")
                        st.markdown(f"- **Phone:** {parsed_resume.get('phone', 'Not found')}")
                        st.markdown(f"- **Location:** {parsed_resume.get('location', 'Not found')}")
                    
                    with col2:
                        st.markdown("**Summary:**")
                        st.markdown(parsed_resume.get('summary', 'No summary found'))
                    
                    if parsed_resume.get('experience'):
                        st.markdown("**Work Experience:**")
                        for i, exp in enumerate(parsed_resume['experience'][:3]):  # Show first 3
                            st.markdown(f"- **{exp.get('title', 'N/A')}** at {exp.get('company', 'N/A')}")
                    
                    if parsed_resume.get('skills'):
                        st.markdown("**Skills:**")
                        skills_str = ", ".join(parsed_resume['skills'][:10])  # Show first 10
                        st.markdown(skills_str)
                
                # Show improvement options
                st.markdown("---")
                st.markdown("### 🚀 Improve Your Resume")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✨ Improve with AI", type="primary", use_container_width=True):
                        with st.spinner("🎯 Improving your resume with AI..."):
                            improved_resume = improve_uploaded_resume(resume_text, st.session_state.job_analysis)
                            if improved_resume:
                                st.session_state.generated_resume = improved_resume
                                save_to_history("resume", improved_resume, {"title": f"Improved {uploaded_resume_file.name}"})
                                st.success("✅ Resume improved successfully!")
                                st.balloons()
                
                with col2:
                    if st.button("📋 Use as Template", use_container_width=True):
                        st.success("✅ Resume data loaded as template!")
                        st.info("💡 You can now edit the parsed information in the Resume Builder tab and generate a new resume.")
                
                # Show original text
                with st.expander("📄 Original Resume Text", expanded=False):
                    st.text_area("Original Content", resume_text, height=400)
        
        # Cover Letter Upload Section
        st.markdown("---")
        st.markdown("### ✉️ Upload Cover Letter")
        st.markdown("Upload your existing cover letter to improve and personalize it")
        
        # File upload for cover letter
        uploaded_cover_letter_file = st.file_uploader(
            "Choose a cover letter file",
            type=['pdf', 'docx', 'txt'],
            key="cover_letter_upload",
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_cover_letter_file is not None:
            # Display file info
            st.markdown(f"""
            <div class="file-info">
                <strong>Uploaded File:</strong> {uploaded_cover_letter_file.name}<br>
                <strong>File Size:</strong> {uploaded_cover_letter_file.size / 1024:.1f} KB<br>
                <strong>File Type:</strong> {uploaded_cover_letter_file.type}
            </div>
            """, unsafe_allow_html=True)
            
            # Extract text based on file type
            if uploaded_cover_letter_file.type == "application/pdf":
                cover_letter_text = extract_text_from_pdf(uploaded_cover_letter_file)
            elif uploaded_cover_letter_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                cover_letter_text = extract_text_from_docx(uploaded_cover_letter_file)
            else:  # TXT file
                cover_letter_text = extract_text_from_txt(uploaded_cover_letter_file)
            
            if cover_letter_text:
                st.session_state.uploaded_cover_letter = cover_letter_text
                st.session_state.cover_letter_filename = uploaded_cover_letter_file.name
                
                # Parse the cover letter
                parsed_cover_letter = parse_cover_letter_text(cover_letter_text)
                
                # Update session state with parsed data
                for key, value in parsed_cover_letter.items():
                    if key in st.session_state.cover_letter_data and value:
                        st.session_state.cover_letter_data[key] = value
                
                st.success("✅ Cover letter uploaded and parsed successfully!")
                
                # Display parsed information
                with st.expander("📊 Parsed Cover Letter Information", expanded=True):
                    st.markdown(f"- **Company:** {parsed_cover_letter.get('company', 'Not found')}")
                    st.markdown(f"- **Position:** {parsed_cover_letter.get('position', 'Not found')}")
                    st.markdown(f"- **Hiring Manager:** {parsed_cover_letter.get('hiring_manager', 'Not found')}")
                
                # Show improvement options
                st.markdown("---")
                st.markdown("### 🚀 Improve Your Cover Letter")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✨ Improve with AI", type="primary", use_container_width=True):
                        if not st.session_state.cover_letter_data['job_description']:
                            st.warning("⚠️ Please paste the job description in the Cover Letter Generator tab first.")
                        else:
                            with st.spinner("🎯 Improving your cover letter with AI..."):
                                improved_letter = improve_uploaded_cover_letter(
                                    cover_letter_text,
                                    st.session_state.cover_letter_data['job_description'],
                                    st.session_state.cover_letter_data
                                )
                                if improved_letter:
                                    st.session_state.generated_cover_letter = improved_letter
                                    save_to_history("cover_letter", improved_letter, {"title": f"Improved {uploaded_cover_letter_file.name}"})
                                    st.success("✅ Cover letter improved successfully!")
                                    st.balloons()
                
                with col2:
                    if st.button("📋 Use as Template", use_container_width=True):
                        st.success("✅ Cover letter data loaded as template!")
                        st.info("💡 You can now edit the information in the Cover Letter Generator tab and generate a new cover letter.")
                
                # Show original text
                with st.expander("📄 Original Cover Letter Text", expanded=False):
                    st.text_area("Original Content", cover_letter_text, height=400)
        
        # Document Comparison
        if st.session_state.uploaded_resume and st.session_state.generated_resume:
            st.markdown("---")
            st.markdown("### 📊 Before & After Comparison")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="comparison-box">', unsafe_allow_html=True)
                st.markdown('<div class="comparison-title">Original Resume</div>', unsafe_allow_html=True)
                st.text_area("Original", st.session_state.uploaded_resume[:1000] + "..." if len(st.session_state.uploaded_resume) > 1000 else st.session_state.uploaded_resume, height=400, disabled=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="comparison-box">', unsafe_allow_html=True)
                st.markdown('<div class="comparison-title">Improved Resume</div>', unsafe_allow_html=True)
                st.text_area("Improved", st.session_state.generated_resume[:1000] + "..." if len(st.session_state.generated_resume) > 1000 else st.session_state.generated_resume, height=400, disabled=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.uploaded_cover_letter and st.session_state.generated_cover_letter:
            st.markdown("---")
            st.markdown("### 📊 Cover Letter Comparison")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="comparison-box">', unsafe_allow_html=True)
                st.markdown('<div class="comparison-title">Original Cover Letter</div>', unsafe_allow_html=True)
                st.text_area("Original", st.session_state.uploaded_cover_letter[:1000] + "..." if len(st.session_state.uploaded_cover_letter) > 1000 else st.session_state.uploaded_cover_letter, height=400, disabled=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="comparison-box">', unsafe_allow_html=True)
                st.markdown('<div class="comparison-title">Improved Cover Letter</div>', unsafe_allow_html=True)
                st.text_area("Improved", st.session_state.generated_cover_letter[:1000] + "..." if len(st.session_state.generated_cover_letter) > 1000 else st.session_state.generated_cover_letter, height=400, disabled=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 class="section-header">Export & Templates</h2>', unsafe_allow_html=True)
        
        # Template Selection
        st.markdown("### 🎨 Resume Templates")
        st.markdown("Select a template style for your resume generation:")
        
        template_cols = st.columns(4)
        templates = {
            'modern': 'Modern Professional',
            'executive': 'Executive',
            'technical': 'Technical',
            'creative': 'Creative'
        }
        
        for i, (template_id, template_name) in enumerate(templates.items()):
            with template_cols[i]:
                is_selected = st.session_state.selected_template == template_id
                css_class = "template-card selected" if is_selected else "template-card"
                
                st.markdown(f"""
                <div class="{css_class}">
                    <h4 style="color: #1e3a8a; margin: 0 0 0.5rem 0;">{template_name}</h4>
                    <p style="color: #6b7280; margin: 0 0 1rem 0; font-size: 0.9rem;">
                        {"Clean, contemporary design" if template_id == 'modern' else
                         "Sophisticated layout for leadership roles" if template_id == 'executive' else
                         "Optimized for technical and engineering roles" if template_id == 'technical' else
                         "Dynamic design for creative positions"}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Select {template_name}", key=f"template_{template_id}", use_container_width=True):
                    st.session_state.selected_template = template_id
                    st.success(f"✅ Selected {template_name} template")
        
        # Export Options
        st.markdown("---")
        st.markdown("### 📥 Export Documents")
        
        if st.session_state.generated_resume:
            with st.expander("📄 Export Resume", expanded=True):
                st.markdown("#### Resume Export Options")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("**Format:** PDF")
                with col2:
                    st.markdown("**Template:** " + templates[st.session_state.selected_template])
                with col3:
                    st.markdown("**Model:** " + st.session_state.selected_model)
                
                if st.button("📥 Download Resume as PDF", type="primary", use_container_width=True):
                    try:
                        pdf_base64 = create_pdf(st.session_state.generated_resume, "resume.pdf", "resume")
                        filename = f"resume_{st.session_state.resume_data['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                        
                        st.markdown(f"""
                        <a href="data:application/pdf;base64,{pdf_base64}" download="{filename}">
                            <button style="background-color: #22c55e; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer; width: 100%; font-weight: 600; font-size: 1.1rem; margin: 1rem 0;">
                                ✅ Click to Download Resume PDF
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
                        
                        st.success(f"✅ Resume ready for download as `{filename}`")
                        st.info("💡 **Pro Tip:** Always review the PDF before sending to employers!")
                    except Exception as e:
                        st.error(f"❌ Error generating PDF: {str(e)}")
                        st.info("💡 Try copying the resume content and pasting it into a Word document as an alternative.")
        else:
            st.info("💡 Generate a resume first to enable export options.")
        
        if st.session_state.generated_cover_letter:
            with st.expander("📄 Export Cover Letter", expanded=True):
                st.markdown("#### Cover Letter Export Options")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Format:** PDF")
                with col2:
                    st.markdown("**Target:** " + st.session_state.cover_letter_data['company'])
                
                if st.button("📥 Download Cover Letter as PDF", type="primary", use_container_width=True):
                    try:
                        pdf_base64 = create_pdf(st.session_state.generated_cover_letter, "cover_letter.pdf", "cover_letter")
                        filename = f"cover_letter_{st.session_state.cover_letter_data['company'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
                        
                        st.markdown(f"""
                        <a href="data:application/pdf;base64,{pdf_base64}" download="{filename}">
                            <button style="background-color: #22c55e; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer; width: 100%; font-weight: 600; font-size: 1.1rem; margin: 1rem 0;">
                                ✅ Click to Download Cover Letter PDF
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
                        
                        st.success(f"✅ Cover letter ready for download as `{filename}`")
                    except Exception as e:
                        st.error(f"❌ Error generating PDF: {str(e)}")
        else:
            st.info("💡 Generate a cover letter first to enable export options.")
        
        # Export Tips
        st.markdown("---")
        st.markdown("### 💡 Export Tips")
        st.info("""
        **Best Practices for Exported Documents:**
        - 📄 **Always Review**: Proofread the generated content before sending to employers
        - 🎯 **Customize**: Tailor each resume/cover letter for specific job applications
        - 🔍 **ATS Check**: The generated content is optimized for Applicant Tracking Systems
        - 📊 **File Naming**: Use professional file names like `FirstName_LastName_Resume.pdf`
        - 🔄 **Iterate**: Generate multiple versions and choose the best one
        - 💾 **Backup**: Save your generated documents locally for future reference
        """)
    
    with tab5:
        st.markdown('<h2 class="section-header">Analytics & Insights</h2>', unsafe_allow_html=True)
        
        # Resume Analytics
        st.markdown("### 📊 Resume Analytics")
        
        if st.session_state.generated_resume:
            # Word count analysis
            resume_words = st.session_state.generated_resume.split()
            word_count = len(resume_words)
            
            # Section analysis
            sections = {}
            lines = st.session_state.generated_resume.split('\n')
            current_section = "Introduction"
            
            for line in lines:
                if line.startswith('## '):
                    current_section = line[3:].strip()
                    sections[current_section] = 0
                elif line.strip() and current_section in sections:
                    sections[current_section] += len(line.split())
            
            # Create visualization
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Word Count by Section**")
                if sections:
                    fig = px.pie(
                        values=list(sections.values()),
                        names=list(sections.keys()),
                        title="Resume Word Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**Resume Metrics**")
                st.metric("Total Word Count", word_count)
                st.metric("Number of Sections", len(sections))
                
                # Calculate average words per section
                avg_words = sum(sections.values()) / len(sections) if sections else 0
                st.metric("Avg. Words per Section", f"{avg_words:.1f}")
                
                # Estimate reading time
                reading_time = max(1, word_count // 200)  # Average reading speed
                st.metric("Est. Reading Time", f"{reading_time} min")
            
            # Skills analysis
            if st.session_state.resume_data['skills']:
                st.markdown("**Skills Analysis**")
                skill_cols = st.columns(min(5, len(st.session_state.resume_data['skills'])))
                for i, skill in enumerate(st.session_state.resume_data['skills']):
                    with skill_cols[i % 5]:
                        # Check if skill appears in resume
                        skill_appearances = st.session_state.generated_resume.lower().count(skill.lower())
                        highlight_class = "skill-tag highlight" if skill_appearances > 0 else "skill-tag"
                        st.markdown(f'<span class="{highlight_class}">{skill}</span>', unsafe_allow_html=True)
                        st.markdown(f"<small>{skill_appearances} mentions</small>", unsafe_allow_html=True)
            
            # ATS optimization score
            st.markdown("**ATS Optimization Score**")
            ats_score = 0
            
            # Check for action verbs
            action_verbs = ["managed", "developed", "led", "created", "implemented", "achieved", "improved", "designed", "coordinated", "executed"]
            action_verb_count = sum(st.session_state.generated_resume.lower().count(verb) for verb in action_verbs)
            ats_score += min(25, action_verb_count * 2)
            
            # Check for quantifiable achievements
            quant_patterns = [r'\d+%$', r'\d+\s*(year|years|month|months)', r'\$\d+', r'\d+\s*(person|people|team)']
            quant_count = sum(len(re.findall(pattern, st.session_state.generated_resume, re.IGNORECASE)) for pattern in quant_patterns)
            ats_score += min(25, quant_count * 5)
            
            # Check for proper formatting
            if not re.search(r'[^\w\s\-.,;:!?()[\]{}"\'\/@#%&*+=<>~`|]', st.session_state.generated_resume):
                ats_score += 25
            
            # Check for length
            if 300 <= word_count <= 700:
                ats_score += 25
            
            # Display ATS score
            st.markdown(f"""
            <div class="progress-container">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>ATS Optimization Score</span>
                    <span>{ats_score}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {ats_score}%; background-color: {'#22c55e' if ats_score >= 75 else '#f59e0b' if ats_score >= 50 else '#ef4444'};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if ats_score < 75:
                st.info("💡 **Improvement Tips:** Consider adding more quantifiable achievements and action verbs to improve your ATS score.")
        else:
            st.info("💡 Generate a resume first to see analytics.")
        
        # Cover Letter Analytics
        st.markdown("### 📊 Cover Letter Analytics")
        
        if st.session_state.generated_cover_letter:
            # Word count analysis
            cover_letter_words = st.session_state.generated_cover_letter.split()
            word_count = len(cover_letter_words)
            
            # Paragraph analysis
            paragraphs = [p.strip() for p in st.session_state.generated_cover_letter.split('\n\n') if p.strip()]
            
            # Sentiment analysis (simplified)
            positive_words = ["excited", "enthusiastic", "passionate", "eager", "interested", "thrilled", "delighted"]
            positive_count = sum(st.session_state.generated_cover_letter.lower().count(word) for word in positive_words)
            
            # Create visualization
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Cover Letter Metrics**")
                st.metric("Total Word Count", word_count)
                st.metric("Number of Paragraphs", len(paragraphs))
                
                # Estimate reading time
                reading_time = max(1, word_count // 200)  # Average reading speed
                st.metric("Est. Reading Time", f"{reading_time} min")
                
                # Sentiment score
                sentiment_score = min(100, positive_count * 10)
                st.metric("Enthusiasm Score", f"{sentiment_score}%")
            
            with col2:
                st.markdown("**Personalization Analysis**")
                
                # Check for company name mentions
                company_mentions = st.session_state.generated_cover_letter.lower().count(st.session_state.cover_letter_data['company'].lower())
                st.metric("Company Name Mentions", company_mentions)
                
                # Check for position title mentions
                position_mentions = st.session_state.generated_cover_letter.lower().count(st.session_state.cover_letter_data['position'].lower())
                st.metric("Position Title Mentions", position_mentions)
                
                # Check for personal pronouns
                personal_pronouns = ["i", "my", "me", "i'm", "i've"]
                personal_count = sum(st.session_state.generated_cover_letter.lower().count(pronoun) for pronoun in personal_pronouns)
                st.metric("Personal Pronouns", personal_count)
                
                # Check for specific examples
                example_indicators = ["for example", "such as", "specifically", "in particular", "instance"]
                example_count = sum(st.session_state.generated_cover_letter.lower().count(indicator) for indicator in example_indicators)
                st.metric("Specific Examples", example_count)
            
            # Cover letter quality score
            quality_score = 0
            
            # Check for appropriate length
            if 200 <= word_count <= 400:
                quality_score += 25
            
            # Check for proper structure
            if any(st.session_state.generated_cover_letter.lower().startswith(prefix) for prefix in ["dear", "hello", "greetings"]):
                quality_score += 15
            
            if any(st.session_state.generated_cover_letter.lower().endswith(suffix) for suffix in ["sincerely", "regards", "thank you"]):
                quality_score += 15
            
            # Check for personalization
            if company_mentions >= 2:
                quality_score += 20
            
            # Check for enthusiasm
            if sentiment_score >= 50:
                quality_score += 25
            
            # Display quality score
            st.markdown(f"""
            <div class="progress-container">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Cover Letter Quality Score</span>
                    <span>{quality_score}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {quality_score}%; background-color: {'#22c55e' if quality_score >= 75 else '#f59e0b' if quality_score >= 50 else '#ef4444'};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if quality_score < 75:
                st.info("💡 **Improvement Tips:** Consider adding more personalization, enthusiasm, and specific examples to improve your cover letter quality.")
        else:
            st.info("💡 Generate a cover letter first to see analytics.")
        
        # Job Match Analysis
        if st.session_state.job_analysis and st.session_state.resume_data['skills']:
            st.markdown("### 🎯 Job Match Analysis")
            
            # Calculate skill match
            job_skills = st.session_state.job_analysis.get('skills', [])
            user_skills = st.session_state.resume_data['skills']
            
            skill_match_result = match_skills_with_job(user_skills, job_skills)
            st.session_state.skill_match = skill_match_result
            
            # Display match percentage
            st.markdown(f"""
            <div class="progress-container">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Skill Match Percentage</span>
                    <span>{skill_match_result['match_percentage']:.1f}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {skill_match_result['match_percentage']}%; background-color: {'#22c55e' if skill_match_result['match_percentage'] >= 75 else '#f59e0b' if skill_match_result['match_percentage'] >= 50 else '#ef4444'};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display matched and missing skills
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Matched Skills:**")
                for skill in skill_match_result['matched_skills']:
                    st.markdown(f'<span class="skill-tag highlight">{skill}</span>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Missing Skills:**")
                for skill in skill_match_result['missing_skills']:
                    st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
            
            # Suggestions for improvement
            if skill_match_result['suggestions']:
                st.markdown("**Skills to Consider Adding:**")
                for skill in skill_match_result['suggestions']:
                    st.markdown(f"- {skill}")
                
                if st.button("Add Suggested Skills to Resume"):
                    for skill in skill_match_result['suggestions']:
                        if skill not in st.session_state.resume_data['skills']:
                            st.session_state.resume_data['skills'].append(skill)
                    st.success("✅ Suggested skills added to your resume!")
        else:
            st.info("💡 Analyze a job description and add skills to your resume to see job match analysis.")

def main():
    """Main application function"""
    st.markdown('<h1 class="main-header">💼 CareerCraft AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Professional Resume & Cover Letter Generator powered by Local AI</p>', unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Check Ollama connection - do this first
    if st.session_state.ollama_status == 'checking':
        with st.spinner("🔍 Checking Ollama server status..."):
            is_running, error_msg, models_data = check_ollama_connection()
            
            if is_running:
                st.session_state.ollama_status = 'running'
                st.session_state.models_data = models_data
                st.session_state.connection_error = None
                
                # Verify models are available
                has_models, model_error = verify_ollama_models(models_data)
                if not has_models:
                    st.session_state.ollama_status = 'no_models'
                    st.session_state.connection_error = model_error
            else:
                st.session_state.ollama_status = 'not_running'
                st.session_state.connection_error = error_msg
    
    # Handle different Ollama states
    if st.session_state.ollama_status in ['not_running', 'no_models', 'checking']:
        show_ollama_setup_page()
    else:
        show_main_application()

if __name__ == "__main__":
    main()