# README.md
# Mental Health Journal Analysis Dashboard

An AI-powered web application that analyzes personal journal entries to provide insights similar to Spotify Wrapped, offering analytical perspectives on writing patterns, emotional trends, and topic evolution.

## Features

- 📊 Core Statistics Analysis
- 🎭 Emotional & Sentiment Analysis
- 🔍 Topic Analysis & Pattern Recognition
- 📈 Comparative Analysis
- 🎨 Custom Visual Reports
- 📝 Writing Style Insights
- 🌱 Personal Growth Metrics
- 💫 Memory Time Capsule
- 🤖 AI-Generated Insights

## Tech Stack

### Frontend
- Next.js
- React
- TailwindCSS
- D3.js/Chart.js/Three.js

### Backend
- Python 3.9+
- FastAPI
- LangChain
- OpenAI API
- PostgreSQL with pgvector

## Setup

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL 14+

### Installation
```bash
# TODO: Add installation steps
```

### Environment Variables
```bash
# TODO: Add environment variables documentation
```

### Development
```bash
# TODO: Add development commands
```

## Contributing
TODO: Add contributing guidelines

## License
TODO: Add license information

---

# .env.example
# Frontend Environment Variables
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Backend Environment Variables
DATABASE_URL=postgresql://user:password@localhost:5432/journal_analysis
OPENAI_API_KEY=your-api-key
PGVECTOR_CONNECTION=postgresql://user:password@localhost:5432/journal_analysis

---

# .replit
run = "bash start.sh"
entrypoint = "main.py"

[env]
PYTHON_VERSION = "3.9"
POETRY_VERSION = "1.4.2"

[nix]
channel = "stable-22_11"

[deployment]
run = ["sh", "-c", "bash start.sh"]
deploymentTarget = "cloudrun"

---

# replit.nix
{ pkgs }: {
  deps = [
    pkgs.python39
    pkgs.postgresql
    pkgs.nodejs-18_x
    pkgs.yarn
    pkgs.poetry
  ];
}

---

# start.sh
#!/bin/bash
# Start both frontend and backend services

# Start PostgreSQL
pg_ctl start

# Install dependencies
cd frontend && yarn install
cd ../backend && poetry install

# Start services
cd ../frontend && yarn dev &
cd ../backend && poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000