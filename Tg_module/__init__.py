import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname('../'), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(os.environ['MIN_STR'])
