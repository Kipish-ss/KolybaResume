from keybert import KeyBERT
from transformers import AutoTokenizer, AutoModelForSequenceClassification
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


def load_models() -> None:
    global _embedding_model, _tokenizer, _classification_model, _label_encoder, _keybert_model

    logger.info("Loading all ML models...")

    _embedding_model = SentenceTransformer('all-mpnet-base-v2')
    logger.info("Sentence transformer model loaded")

    _tokenizer = AutoTokenizer.from_pretrained("ml_backend/fine_tuned_bert")
    _classification_model = AutoModelForSequenceClassification.from_pretrained("ml_backend/fine_tuned_bert")
    _classification_model.eval()

    if torch.cuda.is_available():
        _classification_model.to('cuda')
        logger.info("Classification model moved to GPU")

    _label_encoder = joblib.load("ml_backend/label_encoder.joblib")

    _keybert_model = KeyBERT(model='all-mpnet-base-v2')

    logger.info("All models loaded successfully")


def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        raise RuntimeError("Embedding model not loaded. Call load_models() first.")
    return _embedding_model


def get_classification_models() -> tuple[AutoTokenizer, AutoModelForSequenceClassification, LabelEncoder]:
    global _tokenizer, _classification_model, _label_encoder
    if _tokenizer is None or _classification_model is None or _label_encoder is None:
        raise RuntimeError("Classification models not loaded. Call load_models() first.")
    return _tokenizer, _classification_model, _label_encoder


def get_keybert_model() -> SentenceTransformer:
    global _keybert_model
    if _keybert_model is None:
        raise RuntimeError("Keybert model not loaded. Call load_models() first.")
    return _keybert_model
