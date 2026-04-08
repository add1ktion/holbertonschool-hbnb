import os
from app import create_app

env = os.getenv('FLASK_ENV', 'development')
config_path = "config.ProductionConfig" if env == 'production' else "config.DevelopmentConfig"

app = create_app(config_path)

if __name__ == '__main__':
    app.run(debug=True)