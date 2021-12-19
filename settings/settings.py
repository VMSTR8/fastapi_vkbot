import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')

CONFIRMATION_TOKEN = os.environ.get('CONFIRMATION_TOKEN')

OPEN_GROUP_TOKEN = os.environ.get('OPEN_GROUP_TOKEN')
CLOSED_GROUP_TOKEN = os.environ.get('CLOSED_GROUP_TOKEN')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

SERVICE_TOKEN = os.environ.get('SERVICE_TOKEN')
PERSONAL_TOKEN = os.environ.get('PERSONAL_TOKEN')
VERSION = 5.131

# айдишники администраторов чатов в VK
ADMINISTRATORS = [8818396, 5244683, 3781646, 16153880]

# для проверки кому и какие ответы отдавать
TEAM_ONLY_ANSWERS = ['наши скидки', 'редкие ништяки']

# для парсера id'шники групп
GROUP_IDS = {'esg': '-13212026'}

# список исключенных альбомов для парсера
RESTRICTED = ['не продажа... просто похвастаться...']

if __name__ == '__main__':
    pass
