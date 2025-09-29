import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer  # Extractive algorithm
from transformers import pipeline
import torch

# Global instances for efficiency (load once)
# Abstractive: BART model (fine-tuned for summarization; handles ~1024 tokens)
summarizer_abstractive = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=0 if torch.cuda.is_available() else -1,  # Use GPU if available
    framework="pt"
)

def summarize_text(text: str, mode: str, length: int = None) -> str:
    """
    Generate summary based on mode.
    
    Args:
        text (str): Input text (up to 2000 chars).
        mode (str): 'abstractive' or 'extractive'.
        length (int, optional): Number of sentences for extractive mode.
    
    Returns:
        str: Summarized text.
    
    Raises:
        ValueError: If invalid mode or parameters.
    """
    if mode == 'abstractive':
        return _summarize_abstractive(text)
    elif mode == 'extractive':
        if length is None:
            length = 3  # Default
        return _summarize_extractive(text, length)
    else:
        raise ValueError("Mode must be 'abstractive' or 'extractive'.")

def _summarize_abstractive(text: str) -> str:
    """Abstractive summarization using BART (generates new sentences)."""
    # Truncate if too long (BART max ~1024 tokens; rough char estimate)
    if len(text) > 1500:  # Conservative limit
        text = text[:1500] + "..."
    
    # Generate summary (min_length=30, max_length=150 for concise output)
    result = summarizer_abstractive(
        text,
        max_length=150,
        min_length=30,
        do_sample=False  # Deterministic for consistency
    )
    return result[0]['summary_text']

def _summarize_extractive(text: str, num_sentences: int) -> str:
    """Extractive summarization using Sumy LexRank (selects important sentences)."""
    # Parse text into sentences
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    
    # Summarize with LexRank (graph-based ranking)
    summarizer = LexRankSummarizer()
    summary_sentences = summarizer(parser.document, num_sentences)
    
    # Join sentences into a coherent summary
    summary = ' '.join([str(sentence) for sentence in summary_sentences])
    
    if not summary:
        return "No key sentences could be extracted from the provided text."
    
    return summary