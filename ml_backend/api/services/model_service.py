from keybert import KeyBERT
from transformers import BertTokenizer, BertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
import torch
import joblib
import logging

logger = logging.getLogger(__name__)

_embedding_model = None
_tokenizer = None
_classification_model = None
_label_encoder = None
_keybert_model = None
_vacancies_stopwords = None


def load_models() -> None:
    global _embedding_model, _tokenizer, _classification_model, _label_encoder, _keybert_model, _vacancies_stopwords

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f"Using device: {device}")

    _embedding_model = SentenceTransformer('all-mpnet-base-v2', device=device)
    logger.info("Sentence transformer model loaded")

    _tokenizer = AutoTokenizer.from_pretrained("Kipish/resume_classifier")
    _classification_model = AutoModelForSequenceClassification.from_pretrained("Kipish/resume_classifier")
    _classification_model.eval()

    if device == 'cuda':
        _classification_model.to(device)
        logger.info("Classification model moved to GPU")

    _label_encoder = joblib.load("ml_backend/label_encoder.joblib")

    _keybert_model = KeyBERT(model=_embedding_model)
    logger.info("KeyBERT model initialized with existing SentenceTransformer")

    with open('ml_backend/vacancies_stopwords.txt') as f:
        _vacancies_stopwords = set(f.read().splitlines())

    logger.info("Vacancies stopwords loaded")


def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        raise RuntimeError("Embedding model not loaded. Call load_models() first.")
    return _embedding_model


def get_classification_models() -> tuple[BertTokenizer, BertForSequenceClassification, LabelEncoder]:
    global _tokenizer, _classification_model, _label_encoder
    if _tokenizer is None or _classification_model is None or _label_encoder is None:
        raise RuntimeError("Classification models not loaded. Call load_models() first.")
    return _tokenizer, _classification_model, _label_encoder


def get_keybert_model() -> KeyBERT:
    global _keybert_model
    if _keybert_model is None:
        raise RuntimeError("Keybert model not loaded. Call load_models() first.")
    return _keybert_model


def get_vacancies_stopwords() -> set[str]:
    global _vacancies_stopwords
    if _vacancies_stopwords is None:
        raise RuntimeError("Vacancies stopwords not loaded. Call load_models() first.")
    return _vacancies_stopwords
