import logging

logging.basicConfig(level=logging.INFO, filename="../logs/temporary_logs.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
