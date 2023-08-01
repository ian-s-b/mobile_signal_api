"""Log creation utilities."""
import logging

class CreateLogger:
    """Class used to create a logger."""
    def __init__(self, app_name: str, logger_level:int = logging.ERROR):
        """CreatLogger class initialization."""
        self._logger = logging.getLogger(app_name)
        self._logger.setLevel(logger_level)
        handler = logging.FileHandler(f'logs/{app_name}.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def get_logger(self):
        """Method to get the setted logger."""
        return self._logger
