import os

class Config:
    API_KEY = os.getenv("API_KEY", "your_default_api_key")
    CSE_ID = os.getenv("CSE_ID", "your_default_cse_id")
    PRIORITY_DOMAINS = [
        "linkedin.com", "indeed.com", "glassdoor.com", 
        "monster.com", "careerbuilder.com", "dice.com", "ziprecruiter.com"
    ]

# Add more configuration settings as needed

# Example usage:
# from config import Config
# api_key = Config.API_KEY
