# Job Search Application

This application allows you to search for job listings and analyze their relevance based on your CV.

## Setup and Run Locally

### Prerequisites

- Python 3.x
- pip

### Steps

1. Clone the repository:

   ```sh
   git clone <repository_url>
   cd job_search
### Run the application:

```
./run_local.sh
```

Follow the prompts to enter the job title, location, and optionally use your CV to refine the search.

### Configuration
Update the config.py file with your API keys and priority domains:

### config.py
```
API_KEY = "YOUR_GOOGLE_API_KEY"
CSE_ID = "YOUR_CUSTOM_SEARCH_ENGINE_ID"
PRIORITY_DOMAINS = [
    "linkedin.com", "indeed.com", "glassdoor.com", "monster.com",
    "careerbuilder.com", "dice.com", "ziprecruiter.com"
]
```
### Dependencies
The required Python packages are listed in the requirements.txt file:

~~~
requests
PyPDF2
python-docx
transformers
torch
scikit-learn
beautifulsoup4
python-whois
spacy
~~~

Additionally, download the spaCy model:
```
python -m spacy download en_core_web_sm
```

### Running with Docker
If you prefer to run the application with Docker, use the following commands:

Build the Docker image:
```
docker-compose build
```

Run the Docker container:
```
docker-compose up
```

### License
This project is licensed under the MIT License - see the LICENSE file for details.