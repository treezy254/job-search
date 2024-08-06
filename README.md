# Job Search Application
## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/job_search.git
   cd job_search

2. Build the Docker image:

    ```sh
    docker-compose build
    ```

3. Run the Docker container:
    ```sh
    docker-compose up
    ```
### Configuration
Update the config/config.py file with your API keys and other configuration settings. You can also use environment variables to override the default settings.

### Usage
Modify the main.py file to use your desired functionality from the modules.
Run the application inside the Docker container.
Project Modules
- config/config.py: Configuration settings for the application.
- modules/ai.py: AI-related functions for job evaluation.
- modules/cv_parser.py: Functions for parsing CV files.
- modules/job_search.py: Functions for searching and evaluating job listings.
modules/utils.py: Utility functions such as logging setup.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

