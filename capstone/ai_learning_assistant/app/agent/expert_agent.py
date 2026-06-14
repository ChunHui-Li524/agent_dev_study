"""ExpertAgent：LangChain Agent 封装（占位实现）。"""

from dataclasses import dataclass, field

from app.agent.tools import lookup_glossary, recommend_topic


@dataclass
class AgentResponse:
    """Agent 返回结构。"""

    answer: str
    sources: list[str] = field(default_factory=list)
    tool_calls: list[str] = field(default_factory=list)


class ExpertAgent:
    """AI 学习专家 Agent。

    TODO: 使用 LangChain 绑定 LLM 与 tools，实现 ReAct 或 tool-calling 循环。
    """

    def __init__(self) -> None:
        self._tools = [lookup_glossary, recommend_topic]

    def ask(self, question: str, *, chat_history: list[dict] | None = None) -> AgentResponse:
        """回答用户问题并返回引用来源（占位）。"""
        _ = chat_history, self._tools
        return AgentResponse(
            answer=f"TODO: ExpertAgent 尚未实现。收到问题：{question}",
            sources=[],
            tool_calls=[],
        )
