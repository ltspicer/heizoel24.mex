#!/bin/bash

# Standardwert auf 14400 setzen, falls nicht anders angegeben
WAIT_TIME=${WAIT_TIME:-14400}

while true; do
    echo "Starte Python-Skript..."
    python -u mex.py
    echo "Durchlauf beendet. Warte ${WAIT_TIME} Sekunden..."
    sleep "$WAIT_TIME"
done
