# 诗歌鉴赏 (Poetry Appreciation)

一个基于AI的诗歌鉴赏Web应用，支持用户输入诗歌，应用调用AI大模型进行诗歌解析和鉴赏。

## 功能特点

- 支持用户输入任意诗歌进行分析
- 自动识别著名诗歌和原创诗歌
- 对著名诗歌提供作者信息、创作时间和历史背景
- 对原创诗歌分析作者的心境
- 提供详细的诗歌鉴赏内容
- 给出0-100分的诗歌评分

## 技术栈

- 前端: HTML, CSS, JavaScript
- 后端: Python, Flask
- AI: SiliconFlow API

## 安装与运行

1. 克隆仓库到本地

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置SiliconFlow API密钥
在项目根目录创建`.env`文件，添加以下内容：
```
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
SILICONFLOW_API_URL=https://api.siliconflow.cn/v1/chat/completions
SILICONFLOW_MODEL=Qwen/QwQ-32B
```
请将`your_siliconflow_api_key_here`替换为你的实际SiliconFlow API密钥。你也可以根据需要更改使用的模型。

4. 运行应用
```bash
python app.py
```

5. 在浏览器中访问
```
http://127.0.0.1:5000
```

## 使用方法

1. 在文本框中输入诗歌
2. 点击"鉴赏分析"按钮
3. 等待AI分析结果
4. 查看诗歌的评分、鉴赏内容和相关信息

## 注意事项

- 需要有效的SiliconFlow API密钥才能使用
- 分析结果的质量取决于所选SiliconFlow模型的能力
- 对于非常长的诗歌，可能需要更长的处理时间
- 默认使用Qwen/QwQ-32B模型，可以在`.env`文件中更改
