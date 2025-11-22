# main.py
import logging
import threading
from bot import app
from health import create_health_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
log = logging.getLogger("TeraBoxBot")

# Start the Pyrogram client in the main thread (app.run) is blocking.
def run_bot():
    log.info("🔥 Pyrogram client initialized & handlers loaded!")
    app.run()  # This starts the client and dispatcher

if __name__ == "__main__":
    # Start health server (Flask) in background thread
    health_app = create_health_app()
    t = threading.Thread(target=lambda: health_app.run(host="0.0.0.0", port=8000), daemon=True)
    t.start()

    run_bot()
