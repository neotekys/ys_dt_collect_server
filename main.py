import asyncio
from core.server import run_server

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("서버 종료")