import logging
import time
# ------------------------------------------------------------

class LogFormatter(logging.Formatter):
    formats = {
        logging.ERROR       : "%(asctime)s - %(levelname)s - %(message)s",
        logging.DEBUG       : "%(asctime)s - %(levelname)s - %(message)s in %(funcName)s line %(lineno)d",
        logging.INFO        : "%(asctime)s - %(levelname)s - %(message)s"
    }
    
    def format(self, record : logging.LogRecord):
        f = logging.Formatter(self.formats.get(record.levelno))
        f.converter = time.gmtime
        return f.format(record)