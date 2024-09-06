import logging

# Configuration de base du logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("src/log/drone_project.log"),  # Enregistrement dans un fichier
        logging.StreamHandler()  # Affichage dans la console
    ]
)

# Fonction pour obtenir un logger
def get_logger(name):
    return logging.getLogger(name)