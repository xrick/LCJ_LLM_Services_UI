from flask import Blueprint, render_template, jsonify, request, current_app
from config import settings
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
import json
from datetime import datetime

bp = Blueprint('main', __name__)

# 存儲聊天歷史的字典
chat_history = {}

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    chat_id = data.get('chat_id')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        chat = ChatOpenAI(
            temperature=settings.TEMPERATURE,
            model_name=settings.DEFAULT_MODEL,
            max_tokens=settings.MAX_TOKENS
        )
        
        # 獲取或創建聊天歷史
        if chat_id not in chat_history:
            chat_history[chat_id] = []
        
        # 添加用戶消息到歷史
        chat_history[chat_id].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # 準備消息列表
        messages = [HumanMessage(content=msg['content']) 
                   for msg in chat_history[chat_id] if msg['role'] == 'user']
        
        # 獲取 AI 響應
        response = chat(messages)
        
        # 添加 AI 響應到歷史
        chat_history[chat_id].append({
            'role': 'assistant',
            'content': response.content,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'response': response.content,
            'chat_id': chat_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
    
    except Exception as e:
        current_app.logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    if request.method == 'POST':
        data = request.json
        try:
            # 驗證設置
            if 'temperature' in data:
                temp = float(data['temperature'])
                if not 0 <= temp <= 1:
                    raise ValueError("Temperature must be between 0 and 1")
            
            if 'max_tokens' in data:
                tokens = int(data['max_tokens'])
                if not 1 <= tokens <= 4096:
                    raise ValueError("Max tokens must be between 1 and 4096")
            
            # TODO: 實現設置更新邏輯
            return jsonify({'status': 'success'})
        
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # GET request
    return jsonify({
        'model': settings.DEFAULT_MODEL,
        'temperature': settings.TEMPERATURE,
        'max_tokens': settings.MAX_TOKENS
    })

@bp.route('/api/chat/<chat_id>', methods=['GET'])
def get_chat_history(chat_id):
    if chat_id not in chat_history:
        return jsonify({'error': 'Chat not found'}), 404
    
    return jsonify({
        'history': chat_history[chat_id],
        'chat_id': chat_id
    })

@bp.route('/api/chat/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    if chat_id in chat_history:
        del chat_history[chat_id]
    
    return jsonify({'status': 'success'})