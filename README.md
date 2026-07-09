# Schoolarshild

Next-generation AI writing platform with AI Detection, Humanization, Paraphrasing, Grammar Correction, Plagiarism Detection, and Research Assistance.

## Project Structure

- `/frontend` - Next.js (React) application
- `/backend` - FastAPI (Python) backend

## Local Development

### Requirements
- Node.js (v18+)
- Python 3.10+
- Docker and Docker Compose

### Infrastructure Setup

Start the local PostgreSQL and Redis databases:

```bash
docker-compose up -d
```

### Backend Setup

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
