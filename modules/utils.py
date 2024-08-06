import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_ssl_error(url, error):
    logging.error(f"SSL error for {url}: {error}")
