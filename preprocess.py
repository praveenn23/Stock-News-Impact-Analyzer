import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except:
    pass  # Continue even if download fails

def clean_text(text):
    """Clean and tokenize text for sentiment analysis."""
    try:
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # Simple word splitting as fallback if NLTK fails
        try:
            tokens = word_tokenize(text)
        except:
            # Fallback to simple space splitting
            tokens = text.split()
        
        # Remove stopwords
        try:
            stop_words = set(stopwords.words('english'))
            tokens = [t for t in tokens if t not in stop_words]
        except:
            # If stopwords fail, just use the tokens as is
            pass
        
        return ' '.join(tokens)
    
    except Exception as e:
        # If all else fails, return a simple cleaned version
        return text.lower().strip()

if __name__ == "__main__":
    sample = "Stocks rally as Fed signals rate pause!"
    print(clean_text(sample)) 