# DeepSeek API 调用模块
# 负责将 prompt 发送给 DeepSeek，并返回 AI 生成的客户分析报告

import requests
import os

# 调用 DeepSeek Chat Completions API，返回 AI 生成的文本报告
# 成功时返回 AI 文本，失败时返回 None
def call_deepseek_api(prompt):
    # 从环境变量中读取 API Key，避免将密钥写入代码
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if api_key is None:
        print("未读取到 DEEPSEEK_API_KEY, 请先设置环境变量")
        return None

    url = "https://api.deepseek.com/chat/completions"


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # 按 DeepSeek Chat Completions API 格式构造请求体
    payload = {
        "model": "deepseek-v4-flash",
        "messages": [
            {
                "role": "system",
                "content": "你是一名ToB软件实施/售前支持助理。"
            },
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
            json= payload
        )
        
        if response.status_code == 200:
            result = response.json()

            # 提取 DeepSeek 返回结果中的正文内容
            ai_text = result["choices"][0]["message"]["content"]
            return ai_text

        else:
            print("请求失败，状态码：", response.status_code)
            print("错误信息：", response.text)
            return None

    except requests.exceptions.RequestException as error:
        print("请求异常：", error)
        return None
