#!/bin/bash
echo "🛬 Starting LandRight..."

# Start Qdrant only if not already running
if ! docker ps | grep -q qdrant_landright; then
    echo "Starting Qdrant..."
    docker run -d -p 6333:6333 --name qdrant_landright qdrant/qdrant
    sleep 3
else
    echo "Qdrant already running ✅"
fi

echo "Activating venv..."
source venv/bin/activate

echo "Indexing knowledge base..."
PYTHONPATH=. python backend/db/qdrant.py

echo "Starting app..."
PYTHONPATH=. streamlit run frontend/app.py
