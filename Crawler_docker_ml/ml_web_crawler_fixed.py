# Import required libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from urllib.parse import urlparse, unquote
import re
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
import sys
from datetime import datetime
import csv
import os
from threading import Lock

# Check for required dependencies
try:
    import pandas
    import numpy
    import sklearn
    import scrapy
except ImportError as e:
    print(f"Missing dependency: {str(e).split()[-1].lower()}. Install with: pip install {str(e).split()[-1].lower()}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Function to validate and extract features from a URL
def extract_features(url):
    """
    Extracts features from a URL for classification.
    
    Args:
        url (str): The URL to analyze.
        
    Returns:
    - dict: A dictionary, or None if invalid URL.
    """
    try:
        if not isinstance(url, str):
            raise ValueError("URL must be a string")
        if len(url) < 3 or len(url) > 2048):
            logger.error(f"URL too long or too short: {url[:50]}... (length: {len(url)})")
            raise ValueError(f"URL length must be between 3 and 2048 characters")
        
        # Decode percent-encoded characters
        decoded_url = unquote(url)
        
        # Validate decoded URL
        if not re.match(r'^[\w:/?=&._@%#-+\[\]\(\)\']+$', decoded_url, re.UNICODE):
            raise ValueError("Decoded URL contains invalid characters")
        
        parsed = urlparse(decoded_url)
        if not parsed.scheme.lower() in ['http', 'https']:
            raise ValueError("Invalid scheme; only http or https allowed")
        if not parsed.netloc:
            raise ValueError("Invalid URL; missing netloc")
        if ':' in parsed.netloc:
            parts = parsed.netloc.split(':')
            if len(parts) == 2 and parts[1].isdigit():
                pass
            else:
                raise ValueError("Complex netloc (e.g., IPv6 or invalid port) not supported")
        
        features = {}
        features['length'] = len(decoded_url)
        features['num_digits'] = sum(c.isdigit() for c in decoded_url)
        features['num_special_chars'] = len(re.findall(r'[!@#$%^&*(),.?:;=<>~+#-\'\[\]\(\)]', decoded_url))
        features['has_https'] = 1 if parsed.scheme.lower() == 'https' else 0
        features['subdomains'] = max(0, len(parsed.netloc.split('.')) - 2)
        features['url'] = decoded_url
        return features
    except ValueError as e:
        logger.error(f"Error processing URL {url[:50]}...: {e}")
        return None

# Function to create a sample dataset for training
def create_sample_dataset():
    """
    Creates a small dataset of URLs with labels (0: legitimate, 1: phishing).
    
    Returns:
        pd.DataFrame: A DataFrame with URL features and labels.
    """
    logger.warning("Using small demo dataset. For production, use a larger dataset.")
    urls = [
        ('https://www.google.com', 0),
        ('http://login-paypal.example.com', 1),
        ('https://amazon.co.example.uk', 0),
        ('http://secure-bankofamerica-login.com', 1),
        ('https://github.com', 0),
        ('http://netflix-secure-login.example.com', 1)
    ]
    data = []
    for url, label in urls:
        features = extract_features(url)
        if features:
            features['label'] = label
            data.append(features)
    df = pd.DataFrame(data)
    if df.empty:
        logger.error("No valid data for training. Check dataset URLs.")
        return df
    return df

# Function to train the classifier
def train_classifier(df):
    """
    Trains a logistic regression model on URL features.
    
    Args:
        df (pd.DataFrame): DataFrame with features and labels.
        
    Returns:
        tuple: Trained model, TF-IDF vectorizer, feature columns.
    """
    if df.empty:
        logger.error("No valid data for training")
        return None, None, None
    
    X = df[['length', 'num_digits', 'num_special_chars', 'has_https', 'subdomains']]
    y = df['label']
    
    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 2), max_features=20)
    X_tfidf = vectorizer.fit_transform(df['url'])
    if X_tfidf.nnz == 0:
        logger.warning("TF-IDF features are empty; model may rely solely on numeric features.")
    X_tfidf_df = pd.DataFrame(X_tfidf.toarray(), columns=[f"tfidf_{col}" for col in vectorizer.get_feature_names_out()])
    
    # Combine features
    X = pd.concat([X.reset_index(drop=True), X_tfidf_df.reset_index(drop=True)], axis=1)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate on test data
    if len(X_test) < 2:
        logger.warning("Test set too small (<2 samples); metrics may be unreliable.")
    predictions = model.predict(X_test)
    logger.info(f"Test Accuracy: {accuracy_score(y_test, predictions):.2f}")
    logger.info("\nClassification Report:")
    logger.info(classification_report(y_test, predictions, target_names=['Legitimate', 'Phishing'], zero_division=0))
    
    return model, vectorizer, X.columns.tolist()

# Scrapy Spider for ML-driven crawling
class MLSpider(scrapy.Spider):
    name = 'mlspider'
    raw_urls = os.getenv('START_URLS', 'https://www.example.com')
    if ',' not in raw_urls and len(raw_urls.split()) == 1:
        logger.warning("START_URLS may use invalid separator; expected comma-separated URLs")
    start_urls = [url for url in raw_urls.split(',') if url.strip()]
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'LOG_STDOUT': True,
        'LOG_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0 (compatible; MLSpider/1.0)',
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 1.0,
        'CONCURRENT_REQUESTS': 2,
        'DEPTH_LIMIT': 3
    }
    
    def __init__(self, model, vectorizer, feature_columns, output_file=None, *args, **kwargs):
        super(MLSpider, self).__init__(*args, **kwargs)
        self.model = model
        self.vectorizer = vectorizer
        self.feature_columns = feature_columns
        self.output_file = os.getenv('OUTPUT_FILE', output_file or 'crawled_urls.csv')
        self.relevant_urls = []
        self.max_urls = 100
        self.url_count = 0
        self.file_lock = Lock()
        
        # Validate start URLs
        valid_urls = []
        for url in self.start_urls:
            if extract_features(url):
                valid_urls.append(url)
            else:
                logger.warning(f"Ignoring invalid start URL: {url}")
        self.start_urls = valid_urls or ['https://www.example.com']
        logger.info(f"Using start URLs: {self.start_urls}")
        
        # Initialize CSV file
        logger.info(f"Initializing output file: {self.output_file}")
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['URL', 'Prediction', 'Timestamp'])
        except IOError as e:
            logger.error(f"Failed to initialize output file {self.output_file}: {e}")
            raise
    
    def parse(self, response):
        """
        Parses the response and decides which URLs to follow based on ML prediction.
        """
        self.url_count += 1
        if self.url_count > self.max_urls:
            logger.info(f"Reached max URL limit ({self.max_urls}). Stopping crawl.")
            raise scrapy.exceptions.CloseSpider("max_urls_reached")
        
        if response.status >= 400:
            logger.error(f"Failed to fetch {response.url}: Status {response.status}")
            return
        
        current_url = response.url
        features = extract_features(current_url)
        
        if features:
            # Prepare features for prediction
            feature_df = pd.DataFrame([features])
            X = feature_df[['length', 'num_digits', 'num_special_chars', 'has_https', 'subdomains']]
            X_tfidf = self.vectorizer.transform([features['url']])
            X_tfidf_df = pd.DataFrame(X_tfidf.toarray(), columns=[f"tfidf_{col}" for col in self.vectorizer.get_feature_names_out()])
            X_combined = pd.concat([X.reset_index(drop=True), X_tfidf_df.reset_index(drop=True)], axis=1)
            
            # Ensure feature order matches training
            X_combined = X_combined[self.feature_columns]
            
            # Predict relevance
            prediction = self.model.predict(X_combined)[0]
            if prediction == 1:  # Relevant (phishing)
                logger.info(f"Relevant URL found: {current_url}")
                self.relevant_urls.append(current_url)
                
                # Save to CSV
                try:
                    with self.file_lock:
                        with open(self.output_file, 'a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow([current_url, 'Phishing', datetime.now().isoformat()])
                except IOError as e:
                    logger.error(f"Failed to write to output file {self.output_file}: {e}")
        
        # Extract links and follow relevant ones
        for href in response.css('a::attr(href)').getall():
            next_url = response.urljoin(href)
            features = extract_features(next_url)
            if features:
                feature_df = pd.DataFrame([features])
                X = feature_df[['length', 'num_digits', 'num_special_chars', 'has_https', 'subdomains']]
                X_tfidf = self.vectorizer.transform([features['url']])
                X_tfidf_df = pd.DataFrame(X_tfidf.toarray(), columns=[f"tfidf_{col}" for col in self.vectorizer.get_feature_names_out()])
                X_combined = pd.concat([X.reset_index(drop=True), X_tfidf_df.reset_index(drop=True)], axis=1)
                X_combined = X_combined[self.feature_columns]
                
                prediction = self.model.predict(X_combined)[0]
                if prediction == 1:  # Follow only relevant URLs
                    yield response.follow(next_url, callback=self.parse)

# Main function to run the crawler
def main():
    """
    Trains a classifier and starts the Scrapy crawler.
    """
    logger.info("Starting ML-driven web crawler demo...")
    
    # Train classifier
    df = create_sample_dataset()
    model, vectorizer, feature_columns = train_classifier(df)
    if model is None:
        logger.error("Failed to train classifier. Exiting.")
        return
    
    # Configure and start Scrapy crawler
    process = CrawlerProcess()
    process.crawl(MLSpider, model=model, vectorizer=vectorizer, feature_columns=feature_columns)
    process.start()

# Entry point
if __name__ == "__main__":
    main()