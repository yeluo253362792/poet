import os
import sys
import json
import traceback
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.logger.setLevel('DEBUG')

# Configure SiliconFlow API
SILICONFLOW_API_URL = os.getenv("SILICONFLOW_API_URL", "https://api.siliconflow.cn/v1/chat/completions")
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
SILICONFLOW_MODEL = os.getenv("SILICONFLOW_MODEL", "Qwen/QwQ-32B")

if not SILICONFLOW_API_KEY or SILICONFLOW_API_KEY == "your_siliconflow_api_key_here":
    app.logger.error("SiliconFlow API key is not set or is using the default value")
    print("警告: SiliconFlow API key 未设置或使用了默认值，请在.env文件中设置有效的API key")

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_poem():
    """Analyze the poem using SiliconFlow API."""
    data = request.json
    poem = data.get('poem', '')
    language = data.get('language', 'chinese')  # 默认使用中文
    
    if not poem:
        return jsonify({"error": "No poem provided"}), 400
    
    try:
        # Create prompt for the AI based on selected language
        if language == 'english':
            prompt = f"""
            Analyze the following poem:
            
            {poem}
            
            If it's a famous poem, provide:
            1. The author's information
            2. When it was created
            3. The historical background
            4. A detailed appreciation of the poem
            
            If it's not a famous poem or appears to be original, provide:
            1. An interpretation of the author's state of mind
            2. A detailed appreciation of the poem
            
            Finally, give the poem a score from 0 to 100 (as an integer).
            
            Format your response as a JSON object with these keys:
            - is_famous (boolean)
            - author (string, if famous)
            - creation_time (string, if famous)
            - background (string, if famous)
            - state_of_mind (string, if not famous)
            - appreciation (string)
            - score (integer between 0 and 100)
            
            You can use Markdown formatting in your response for the background, state_of_mind, and appreciation fields. For example, use bullet points (*), emphasis (*text*), strong (**text**), and blockquotes (> text) to structure your analysis. DO NOT add a heading like '## Poem Appreciation' in the appreciation field, as the UI already has this heading.
            
            Respond in English.
            """
        else:  # 默认使用中文
            prompt = f"""
            分析以下诗歌：
            
            {poem}
            
            如果这是一首著名的诗歌，请提供：
            1. 作者信息
            2. 创作时间
            3. 历史背景
            4. 详细的诗歌鉴赏
            
            如果这不是著名诗歌或是原创诗歌，请提供：
            1. 对作者心境的解读
            2. 详细的诗歌鉴赏
            
            最后，给这首诗打一个0到100分的分数（整数）。
            
            请将回复格式化为包含以下键的JSON对象：
            - is_famous (布尔值，是否著名)
            - author (字符串，如果是著名诗歌)
            - creation_time (字符串，如果是著名诗歌)
            - background (字符串，如果是著名诗歌)
            - state_of_mind (字符串，如果不是著名诗歌)
            - appreciation (字符串，鉴赏内容)
            - score (整数，0-100之间的分数)
            
            你可以在background、state_of_mind和appreciation字段中使用Markdown格式来增强内容的表现力。例如，使用项目符号（*）、强调（*文本*）、加粗（**文本**）和引用（> 文本）来结构化你的分析。请不要在appreciation字段中添加“## 诗歌鉴赏”之类的标题，因为界面中已经有这个标题了。
            
            请用中文回答。
            """
        
        # Check if API key is set
        if not SILICONFLOW_API_KEY or SILICONFLOW_API_KEY == "your_siliconflow_api_key_here":
            app.logger.error("SiliconFlow API key is not set or is using the default value")
            return jsonify({"error": "SiliconFlow API key is not set. Please set a valid API key in the .env file."}), 500
        
        # Call SiliconFlow API
        try:
            headers = {
                "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": SILICONFLOW_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a poetry expert who can analyze and appreciate poems."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False,
                "max_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.7,
                "response_format": {"type": "text"}
            }
            
            app.logger.debug(f"Sending request to SiliconFlow API: {payload}")
            response = requests.post(SILICONFLOW_API_URL, headers=headers, json=payload)
            response.raise_for_status()  # 如果请求失败，抛出异常
            
            response_data = response.json()
            app.logger.debug(f"SiliconFlow API response: {response_data}")
            
            # 提取响应内容
            result = response_data["choices"][0]["message"]["content"]
            
            # 返回分析结果
            return jsonify({"analysis": result})
        except Exception as api_error:
            app.logger.error(f"SiliconFlow API error: {str(api_error)}")
            print(f"SiliconFlow API error: {str(api_error)}")
            return jsonify({"error": f"SiliconFlow API error: {str(api_error)}"}), 500
    
    except Exception as e:
        app.logger.error(f"General error: {str(e)}")
        app.logger.error(traceback.format_exc())
        print(f"General error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
