"""
Cache Layer Module
Simple in-memory caching with TTL support
"""
import os
import time
from threading import Lock


class WeatherCache:

    
    def __init__(self):

        self.cache = {}
        self.lock = Lock()
        self.ttl = int(os.getenv('CACHE_TTL_SECONDS', 600))  # Default 10 minutes
    
    def get(self, key):
        with self.lock:
            if key in self.cache:
                value, expiry_time = self.cache[key]
                
                # Check if expired
                if time.time() < expiry_time:
                    return value
                else:
                    # Remove expired entry
                    del self.cache[key]
            
            return None
    
    def set(self, key, value):

        with self.lock:
            expiry_time = time.time() + self.ttl
            self.cache[key] = (value, expiry_time)
    
    def clear(self):
        """Clear all cache entries"""
        with self.lock:
            self.cache.clear()
    
    def remove_expired(self):
        with self.lock:
            current_time = time.time()
            expired_keys = [
                key for key, (_, expiry) in self.cache.items()
                if current_time >= expiry
            ]
            
            for key in expired_keys:
                del self.cache[key]
