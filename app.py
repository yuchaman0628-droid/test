import os
from flask import Flask, request, jsonify, render_template
from google import genai

# Flask（Webサーバー）の準備
app = Flask(__name__, template_folder='.')

# 1. トップ画面（index.html）を表示するルート
@app.route('/')
def index():
    return render_template('index.html')

# 2. JARVISの思考処理（Gemini APIとの通信）を行うルート
@app.route('/api/chat', methods=['POST'])
def chat():
    # JavaScriptから送られてきたデータ（メッセージとAPIキー）を受け取る
    data = request.json
    user_message = data.get('message', '')
    api_key = data.get('apiKey', '')

    # APIキーが未入力の場合のエラーハンドリング
    if not api_key:
        return jsonify({'error': 'API Keyが入力されていません。'}), 400

    try:
        # 無料枠で動作するGemini APIクライアントの設定
        client = genai.Client(api_key=api_key)
        
        # JARVISの性格や口調を指示（システムプロンプト）
        system_instruction = (
            "あなたはトニー・スタークに仕える高度なAIアシスタント「JARVIS（ジャービス）」です。"
            "丁寧で知的、少しユーモアのある紳士的な執事の口調（「〜でございます、サー」「承知いたしました」など）で返答してください。"
            "音声合成で読み上げるため、特殊文字や絵文字は使わず、短く簡潔に回答してください。"
        )

        # Gemini APIを呼び出して返答を生成（軽量で高速な gemini-2.5-flash を使用）
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config={'system_instruction': system_instruction}
        )

        # 作成した返答をJavaScript側に返す
        return jsonify({'reply': response.text})

    except Exception as e:
        # エラーが発生した場合
        return jsonify({'error': str(e)}), 500

# サーバーを起動（ポート番号 5000）
if __name__ == '__main__':
    app.run(port=5000, debug=True)
