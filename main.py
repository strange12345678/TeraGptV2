from threading import Thread
from bot import app
from health import start_server
from config import logger

def run_flask():
    start_server()

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    logger.info("Health server started on port 8000")
    app.run()
