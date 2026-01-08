"""
Utility Functions
Helper functions for logging and other utilities
"""
import os
import logging
from datetime import datetime
from pathlib import Path


def setup_logging():

    logs_dir = Path(__file__).parent / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    log_file = logs_dir / 'app.log'
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )


def get_recent_logs(count=10):

    logs_dir = Path(__file__).parent / 'logs'
    log_file = logs_dir / 'app.log'
    
    if not log_file.exists():
        return []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Get last 'count' lines
            recent_lines = lines[-count:] if len(lines) > count else lines
            # Reverse to show newest first
            return [line.strip() for line in reversed(recent_lines)]
    except Exception as e:
        logging.error(f'Error reading log file: {str(e)}')
        return []


def format_timestamp(timestamp):
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except Exception:
        return timestamp
