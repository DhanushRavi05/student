#!/usr/bin/env bash

echo "==============================================================================="
echo "      EduTrack AI: Student Learning Behaviour & Intervention Analytics"
echo "                   Academic Mini Project Edition"
echo "==============================================================================="
echo ""

if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python 3 could not be found."
    exit 1
fi

echo "[1/3] Verifying dependencies..."
pip install -r requirements.txt --quiet

echo "[2/3] Launching Academic Analytics Portal on http://127.0.0.1:5000 ..."
python3 app.py
