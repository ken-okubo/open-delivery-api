import os
import sys
from dotenv import load_dotenv

# Adiciona o path raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Decide qual .env carregar
RUNNING_OUTSIDE_DOCKER = os.getenv("RUNNING_OUTSIDE_DOCKER", "0") == "1"
env_file = ".env.dev" if RUNNING_OUTSIDE_DOCKER else ".env"

# Carrega o arquivo
load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), "..", env_file)
)
