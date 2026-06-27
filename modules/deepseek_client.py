# DeepSeek API 调用模块
# 负责将 prompt 发送给 DeepSeek，并尽量把 AI 返回内容解析成结构化报告。

import requests
import os
import json

def call_deepseek_api(prompt):
    """
    调用 DeepSeek Chat Completions API，返回 AI 生成的原始文本。

    输入：
        prompt: prompt_builder 构造好的客户分析提示词。

    输出：
        成功时返回 AI 文本；请求失败、缺少 API Key 或网络异常时返回 None。
    """
    # 从环境变量中读取 API Key，避免将密钥写入代码
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if api_key is None:
        print("未读取到 DEEPSEEK_API_KEY, 请先设置环境变量")
        return None

    url = "https://api.deepseek.com/chat/completions"


    # Authorization 使用 Bearer Token，这是大多数 Chat Completions API 的鉴权方式。
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # 请求体保持 DeepSeek API 所需结构；模型和 thinking 参数会影响返回速度与内容形态。
    payload = {
        "model": "deepseek-v4-flash",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "thinking": {
            "type": "disabled"
        }
    }

    try:
        response = requests.post(
            url= url,
            headers= headers,
            json= payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()

            # DeepSeek 返回结构中 choices[0].message.content 才是模型生成的正文。
            ai_text = result["choices"][0]["message"]["content"]
            return ai_text

        else:
            print("请求失败，状态码：", response.status_code)
            print("错误信息：", response.text)
            return None

    except requests.exceptions.RequestException as error:
        print("请求异常：", error)
        return None


def parse_ai_response(ai_text):
    """
    尝试把 AI 返回的 JSON 字符串转换成 Python dict。

    输入：
        ai_text: DeepSeek 返回的原始文本。

    输出：
        解析成功时返回 dict；解析失败时返回 {"raw_text": ai_text}；
        API 无返回内容时返回错误说明。
    """
    if ai_text is None:
        return {
            "error": "AI接口未返回内容"
        }

    try:
        # prompt 要求 AI 输出 JSON，这里解析成 dict，方便前端展示或写入报告。
        return json.loads(ai_text)
    except json.JSONDecodeError:
        # 如果模型输出了额外说明或非标准 JSON，保留原文，避免分析结果丢失。
        return {
            "raw_text": ai_text
        }

def call_deepseek_json_api(prompt):
    """
    调用 DeepSeek，并尽量将 AI 返回结果解析为 Python dict。

    输入：
        prompt: 客户分析提示词。

    输出：
        Python dict。可能是标准分析报告，也可能是 raw_text 或 error 包装结果。
    """
    ai_text = call_deepseek_api(prompt)
    ai_result = parse_ai_response(ai_text)
    return ai_result
