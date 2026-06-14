"""DashScope OpenAI 兼容接口 LLM 客户端（占位实现）。"""

from typing import Any

from openai import OpenAI

from app.core.config import AppConfig, load_config


def _build_client(config: AppConfig) -> OpenAI:
    """创建指向 DashScope 兼容端点的 OpenAI 客户端。

    base_url 示例: https://dashscope.aliyuncs.com/compatible-mode/v1
    """
    return OpenAI(
        api_key=config.dashscope_api_key,
        base_url=config.dashscope_base_url,
    )


def call_llm(
    messages: list[dict[str, str]],
    *,
    model: str | None = None,
    stream: bool = False,
) -> Any:
    """调用 LLM 完成对话（占位）。

    TODO: 实现非流式/流式响应，统一错误处理与重试。
    """
    config = load_config()
    client = _build_client(config)
    chosen_model = model or config.llm_model

    # TODO: 根据 stream 参数返回完整响应或迭代器
    _ = client, chosen_model, messages, stream
    raise NotImplementedError("call_llm 尚未实现")
