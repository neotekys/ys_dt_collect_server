import logging
from logging.handlers import RotatingFileHandler
from config import settings


def get_logger(name):
    # 일관된 포맷의 로거 객체 반환
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    # 이미 핸들러가 설정된 경우 중복 추가 방지
    if not logger.hasHandlers():
        # 콘솔 핸들러
        stream_handler = logging.StreamHandler()
        # 파일 핸들러
        file_handler = RotatingFileHandler(
            filename=settings.LOG_FILE,
            maxBytes=1024 * 1024 * 5,  # 5MB
            backupCount=5  # 최대 5개의 백업 파일 유지
        )

        # 로그 포맷 설정
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger