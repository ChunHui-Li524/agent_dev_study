"""
==========================================
示例 5: AutoGen 代码执行
==========================================
学习目标：
1. 配置 code_execution_config
2. 理解代码生成与执行流程
3. 本示例关闭执行（安全学习模式）
"""

import os
from dotenv import load_dotenv
import autogen

load_dotenv()

CONFIG_LIST = [{"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}]


def create_code_assistant():
    """创建可生成代码的助手"""

    return autogen.AssistantAgent(
        name="coder",
        llm_config={"config_list": CONFIG_LIST, "temperature": 0.2},
        system_message=(
            "你是 Python 编程导师。生成简洁可运行的 LangChain 示例代码，"
            "用 markdown 代码块包裹，并附简短说明。"
        ),
    )


def create_user_proxy_disabled_exec():
    """UserProxy：关闭代码执行（学习模式）"""

    return autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        code_execution_config=False,
    )


def demo_code_generation_no_exec():
    """生成代码但不执行"""

    coder = create_code_assistant()
    user_proxy = create_user_proxy_disabled_exec()

    print("=== 代码生成（code_execution_config=False）===\n")
    print("注意: 已关闭自动执行，仅展示生成代码，避免本地运行风险。\n")
    user_proxy.initiate_chat(
        coder,
        message="写一个简单的 LangChain LCEL 链示例：prompt | llm | parser。",
    )


def show_exec_config_note():
    """说明如何开启代码执行"""

    print("\n=== 开启执行的配置示例 ===\n")
    print("code_execution_config = {")
    print('    "work_dir": "coding",')
    print('    "use_docker": False,  # 生产环境建议 use_docker=True')
    print("}")


if __name__ == "__main__":
    print("🚀 示例 5: AutoGen 代码执行\n")

    demo_code_generation_no_exec()
    show_exec_config_note()

    print("\n✅ 示例运行完成！")
