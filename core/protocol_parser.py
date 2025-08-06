from utils.logger import get_logger

logger = get_logger(__name__)

# 로라 서버로 부터 받은 데이터 파싱
def parse_lora_packet(data:bytes, addr: tuple):
    try:
        logger.info(f"[{addr[0]}:{addr[1]}]로 부터 데이터 수신: {data.hex()}")

        return data
    except Exception as e:
        logger.error(f"데이터 파싱 중 오류 발생: {e}")