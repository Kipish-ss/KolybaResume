from keybert import KeyBERT
from transformers import BertTokenizer, BertForSequenceClassification, AutoTokenizer, \
    AutoModelForSequenceClassification, pipeline, Pipeline
from sentence_transformers import SentenceTransformer
import torch
import logging
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*divide by zero encountered in matmul.*")
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*overflow encountered in matmul.*")
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*invalid value encountered in matmul.*")

logger = logging.getLogger(__name__)

_embedding_model = None
_tokenizer = None
_classification_model = None
_label_encoder = None
_keybert_model = None
_vacancies_stopwords = None
_skills_extraction_pipe = None
_skills_tokenizer = None


def load_models() -> None:
    global _embedding_model, _tokenizer, _classification_model, _label_encoder, _keybert_model, _vacancies_stopwords, _skills_tokenizer, _skills_extraction_pipe

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f"Using device: {device}")

    _embedding_model = SentenceTransformer('all-mpnet-base-v2', device=device)
    logger.info("Sentence transformer model loaded")

    _tokenizer = AutoTokenizer.from_pretrained("Kipish/resume_classifier")
    _classification_model = AutoModelForSequenceClassification.from_pretrained("Kipish/resume_classifier")
    _classification_model.eval()

    _keybert_model = KeyBERT(model=_embedding_model)
    logger.info("KeyBERT model initialized with existing SentenceTransformer")

    _skills_tokenizer = AutoTokenizer.from_pretrained('ihk/skillner')
    _skills_extraction_pipe = pipeline("token-classification", model='ihk/skillner')

    if device == 'cuda':
        _classification_model.to(device)
        _embedding_model.to(device)
        _skills_extraction_pipe.model.to(device)
        logger.info("All models moved to GPU")

    logger.info("Skills extraction model loaded")


def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        raise RuntimeError("Embedding model not loaded. Call load_models() first.")
    return _embedding_model


def get_classification_model() -> tuple[BertTokenizer, BertForSequenceClassification]:
    global _tokenizer, _classification_model
    if _tokenizer is None or _classification_model is None:
        raise RuntimeError("Classification model not loaded. Call load_models() first.")
    return _tokenizer, _classification_model


def get_keybert_model() -> KeyBERT:
    global _keybert_model
    if _keybert_model is None:
        raise RuntimeError("Keybert model not loaded. Call load_models() first.")
    return _keybert_model


def get_skills_model() -> tuple[BertTokenizer, Pipeline]:
    global _skills_tokenizer, _skills_extraction_pipe
    if _skills_tokenizer is None or _skills_extraction_pipe is None:
        raise RuntimeError("Skills extraction model not loaded. Call load_models() first.")
    return _skills_tokenizer, _skills_extraction_pipe
