"""
==========================================
选修: FastAPI SSE 流式端点
==========================================
学习目标：
1. 最小 FastAPI 应用
2. Server-Sent Events 流式响应
3. 与 PySide6 QThread 流式的对比参考

运行（需额外安装 fastapi uvicorn）:
  pip install fastapi uvicorn
  python example/optional_fastapi_sse.py
  curl -N http://127.0.0.1:8000/stream?q=hello
"""

import asyncio
import time

from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse

app = FastAPI(title="Phase6 SSE Demo")

MOCK_TOKENS = [
    "这是 ",
    "FastAPI ",
    "SSE ",
    "流式 ",
    "演示。",
    "桌面端可用 ",
    "QThread+Signal ",
    "实现类似效果。",
]


async def token_stream(query: str):
    """异步生成 SSE 数据块。"""
    yield f"data: [start] query={query}\n\n"
    for token in MOCK_TOKENS:
        await asyncio.sleep(0.08)
        yield f"data: {token}\n\n"
    yield "data: [done]\n\n"


@app.get("/stream")
async def stream(q: str = Query(default="test")):
    """SSE 流式端点。"""
    return StreamingResponse(
        token_stream(q),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/")
async def root():
    return {"message": "GET /stream?q=your_question"}


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
