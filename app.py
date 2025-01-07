from flask import Flask, render_template, request, jsonify, send_from_directory
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from flask_cors import CORS
import traceback
# 載入環境變量
load_dotenv()

app = Flask(__name__)
CORS(app)
# 配置 OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
print("open api key:", openai.api_key)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
@app.route('/')
def home():
    return render_template('index_new1.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data['message']
        print(f"Received message: {user_message}")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        ai_message = response.choices[0].message.content
        print(f"AI response: {ai_message}")
        return jsonify({"response": ai_message})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# 服務靜態文件
@app.route('/static/js/<path:filename>')
def serve_static(filename):
    return send_from_directory('static/js', filename)

if __name__ == '__main__':
    app.run(debug=True)