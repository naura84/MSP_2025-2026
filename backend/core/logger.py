import logging
import os
from logging.handlers import RotatingFileHandler

# Crée le dossier logs/ s'il n'existe pas
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "audit.log")

# Handler fichier avec rotation (évite un fichier qui grossit à l'infini)
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=1_000_000, backupCount=5, encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
))

# Handler console (garde l'affichage dans le terminal)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:          # évite d'ajouter les handlers en double
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger