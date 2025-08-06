# 비동기 통신 위한 라이브러리 asyncio
import asyncio
from config import settings
from utils.logger import get_logger
from .protocol_parser import parse_lora_packet

logger = get_logger(__name__)

# 개별 클라이언트 연결을 처리하는 비동기 함수
async def handle_client(reader, writer):
    addr = writer.get_extra_info('pername')
    logger.info(f"클라이언트 연결됨: {addr}")

    try:
        while True:
            # 1024 바이트 단위로 데이터 수신
            data = await reader.read(1024)
            if not data:
                logger.info(f"클라이언트 연결 종료: {addr}")
                break

            # 데이터 파싱 및 확인
            parsed_data = parse_lora_packet(data, addr)

            if parsed_data:
                # TODO: 파싱된 데이터를 기반으로 DB 저장 또는 추가 로직 호출
                logger.info(f"{addr[0]}:{addr[1]}]로 부터 받은 데이터: {parsed_data.hex()}")
    except asyncio.CancelledError:
        logger.info(f"클라이언트 핸들러 취소됨 : {addr}")
    except Exception as e:
        logger.error(f"클라이언트 핸들러 오류 발생: {addr}, 오류: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        logger.info(f"클라이언트 연결 종료됨: {addr}")

# TCP 서버 시작하고 실행
async def run_server():
    server = await asyncio.start_server(handle_client, settings.HOST, settings.PORT)

    addr = server.sockets[0].getsockname()
    logger.info(f"서버 시작됨: {addr}")

    async with server:
        await server.serve_forever()
