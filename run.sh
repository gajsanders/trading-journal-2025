#!/bin/bash
# Trading Journal Analytics Tool - Startup Script
# Usage: ./run.sh
# For M1 Mac: ensure Python 3.9+ and dependencies are installed

# Activate virtual environment if needed
# source .venv/bin/activate

# Load environment variables from .env if present
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

# Run the Streamlit app
streamlit run src/app/streamlit_app.py 