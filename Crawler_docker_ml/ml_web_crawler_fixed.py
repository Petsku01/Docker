# "fixed" version -pk

import os
import sys
import csv
import logging
import re
from datetime import datetime
from urllib.parse import urlparse, unquote
from threading import Lock

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import scrapy
from scrapy.crawler import CrawlerProcess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def extract_url_features(url):
    """Extract features from URL for classification."""
    try:
        if not isinstance(url, str) or len(url) < 10 or len(url) > 2000:
            return None
            
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https'] or not parsed.netloc:
            return None
        
        return {
            'url': url,
            'length': len(url),
            'num_digits': sum(c.isdigit() for c in url),
            'num_special': len(re.findall(r'[!@#$%^&*(),.?:;=<>~+-]', url)),
            'has_https': int(parsed.scheme == 'https'),
            'num_dots': url.count('.'),
            'num_hyphens': url.count('-'),
            'path_depth': len([p for p in parsed.path.split('/') if p])
        }
    except Exception:
        return None


def create_training_data():
    """Create sample training dataset."""
    samples = [
        ('https://google.com', 0),
        ('https://amazon.com', 0),
        ('https://github.com', 0),
        ('https://stackoverflow.com', 0),
        ('https://microsoft.com', 0),
        ('http://secure-bank-login.suspicious.com', 1),
        ('http://paypal-verify.fake-site.com', 1),
        ('http://amazon-security.phishing.net', 1),
        ('http://verify-account.suspicious-domain.org', 1),
        ('http://update-security.fake-bank.com', 1),
    ]
    
    data = []
    for url, label in samples:
        features = extract_url_features(url)
        if features:
            features['label'] = label
            data.append(features)
    
    return pd.DataFrame(data)


def train_model(df):
    """Train the ML model."""
    if df.empty:
        logger.error("No training data available")
        return None, None, None
    
    # Prepare features
    feature_cols = ['length', 'num_digits', 'num_special', 'has_https', 
                   'num_dots', 'num_hyphens', 'path_depth']
    X = df[feature_cols]
    y = df['label']
    
    # TF-IDF features
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3), max_features=50)
    X_tfidf = vectorizer.fit_transform(df['url'])
    X_tfidf_df = pd.DataFrame(
        X_tfidf.toarray(), 
        columns=[f"tfidf_{i}" for i in range(X_tfidf.shape[1])]
    )
    
    # Combine features
    X_combined = pd.concat([X.reset_index(drop=True), X_tfidf_df], axis=1)
    
    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(
        X_combined, y, test_size=0.3, random_state=42, stratify=y
    )
    
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = accuracy_score(y_test, model.predict(X_test))
    logger.info(f"Model accuracy: {accuracy:.2f}")
    
    return model, vectorizer, X_combined.columns.tolist()


class MLCrawlerSpider(scrapy.Spider):
    name = 'ml_crawler'
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'MLCrawler/1.0',
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 2,
        'DEPTH_LIMIT': 2,
        'DOWNLOAD_TIMEOUT': 10,
        'RETRY_TIMES': 1,
    }
    
    def __init__(self, model, vectorizer, feature_columns, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.vectorizer = vectorizer
        self.feature_columns = feature_columns
        self.output_file = os.getenv('OUTPUT_FILE', 'output/crawled_urls.csv')
        self.max_urls = int(os.getenv('MAX_URLS', '50'))
        self.url_count = 0
        self.file_lock = Lock()
        self.seen_urls = set()
        
        # Parse start URLs
        urls_env = os.getenv('START_URLS', 'https://example.com')
        self.start_urls = [u.strip() for u in urls_env.split(',') if u.strip()]
        
        # Initialize output file
        try:
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            with open(self.output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['URL', 'Classification', 'Confidence', 'Timestamp'])
            logger.info(f"Output file: {self.output_file}")
        except Exception as e:
            logger.error(f"Failed to initialize output: {e}")
            raise
    
    def predict_url(self, url):
        """Predict if URL is suspicious."""
        features = extract_url_features(url)
        if not features:
            return 0, 0.5
        
        try:
            # Extract features
            feature_cols = ['length', 'num_digits', 'num_special', 'has_https',
                           'num_dots', 'num_hyphens', 'path_depth']
            X = pd.DataFrame([features])[feature_cols]
            
            # TF-IDF features
            X_tfidf = self.vectorizer.transform([url])
            X_tfidf_df = pd.DataFrame(
                X_tfidf.toarray(),
                columns=[f"tfidf_{i}" for i in range(X_tfidf.shape[1])]
            )
            
            # Combine and predict
            X_combined = pd.concat([X.reset_index(drop=True), X_tfidf_df], axis=1)
            X_combined = X_combined[self.feature_columns]
            
            prediction = self.model.predict(X_combined)[0]
            confidence = self.model.predict_proba(X_combined)[0].max()
            
            return prediction, confidence
        except Exception:
            return 0, 0.5
    
    def parse(self, response):
        """Parse response and extract URLs."""
        if self.url_count >= self.max_urls:
            logger.info(f"Reached max URLs limit ({self.max_urls})")
            raise scrapy.exceptions.CloseSpider('max_urls_reached')
        
        current_url = response.url
        if current_url in self.seen_urls:
            return
        
        self.seen_urls.add(current_url)
        self.url_count += 1
        
        # Predict current URL
        prediction, confidence = self.predict_url(current_url)
        
        # Log suspicious URLs
        if prediction == 1:
            logger.info(f"Suspicious URL found: {current_url} (confidence: {confidence:.2f})")
            
            with self.file_lock:
                try:
                    with open(self.output_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            current_url,
                            'Suspicious' if prediction == 1 else 'Safe',
                            f"{confidence:.2f}",
                            datetime.now().isoformat()
                        ])
                except Exception as e:
                    logger.error(f"Failed to write to CSV: {e}")
        
        # Extract and follow links
        for href in response.css('a::attr(href)').getall()[:20]:  # Limit links per page
            next_url = response.urljoin(href)
            
            if next_url not in self.seen_urls:
                prediction, confidence = self.predict_url(next_url)
                
                # Follow suspicious URLs with higher probability
                if prediction == 1 or (confidence < 0.7 and np.random.random() < 0.3):
                    yield response.follow(next_url, callback=self.parse, dont_filter=True)


def main():
    """Main execution function."""
    logger.info("Starting ML Web Crawler...")
    
    # Train model
    logger.info("Training classifier...")
    df = create_training_data()
    model, vectorizer, feature_columns = train_model(df)
    
    if model is None:
        logger.error("Failed to train model")
        sys.exit(1)
    
    # Start crawler
    logger.info("Starting web crawler...")
    process = CrawlerProcess()
    process.crawl(MLCrawlerSpider, 
                 model=model, 
                 vectorizer=vectorizer,
                 feature_columns=feature_columns)
    process.start()
    
    logger.info("Crawling complete")


if __name__ == "__main__":
    main()
