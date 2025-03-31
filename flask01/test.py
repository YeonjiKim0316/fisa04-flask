from flask import Flask, request, redirect, session, url_for, render_template_string
from flask import abort

app = Flask(__name__)
app.secret_key = 'secret-key'  # 세션을 위한 비밀 키

# 샘플 사용자 데이터
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user': {'password': 'user123', 'role': 'user'}
}

@app.route('/')
def index():
    if 'username' in session:
        return f"안녕하세요, {session['username']}님! <a href='/logout'>로그아웃</a>"
    return "로그인이 필요합니다. <a href='/login'>로그인</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pw = request.form['password']
        user = users.get(username)

        if user and user['password'] == pw:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('index'))
        return "잘못된 사용자 이름 또는 비밀번호입니다."

    # GET 요청 시 HTML 폼을 문자열로 렌더링
    login_form = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>로그인</title>
    </head>
    <body>
        <h2>로그인</h2>
        <form method="POST" action="{{ url_for('login') }}">
            <label for="username">사용자 이름:</label><br>
            <input type="text" id="username" name="username" required><br><br>

            <label for="password">비밀번호:</label><br>
            <input type="password" id="password" name="password" required><br><br>

            <button type="submit">로그인</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(login_form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    if 'role' in session and session['role'] == 'admin':
        return "관리자 페이지에 오신 것을 환영합니다."
    else:
        return abort(403)  

if __name__ == '__main__':
    app.run(debug=True, port=5002)
