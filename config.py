from os import getenv
from webdriver_manager.chrome import ChromeDriverManager


PROJECT_NAME = 'Avito bot'
DRIVER_PATH = ChromeDriverManager().install()
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
BOT_TOKEN = getenv('AVITO_BOT_TOKEN')
ADMIN_ID = getenv('ADMIN_ID')
CHECK_FREQUENCY = 10