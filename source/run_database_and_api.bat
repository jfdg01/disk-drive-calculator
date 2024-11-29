@echo off
start cmd /k "cd /d C:\Users\gara\Documents\Projects\disc\db && .\pocketbase.exe serve"
start cmd /k "cd /d C:\Users\gara\Documents\Projects\disc\source && uvicorn api:app --reload"