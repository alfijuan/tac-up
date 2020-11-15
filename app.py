import os
from src.main import create_app

app = create_app(os.getenv('CONFIG_MODE') or 'development')

if __name__ == '__main__':
    app.run()