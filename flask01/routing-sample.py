from flask import Flask, request, jsonify, render_template_string, make_response, redirect, url_for

app = Flask(__name__)

# 1. 기본 문자열 변수: 어떤 텍스트도 받지만 슬래시(/)는 제외
@app.route('/user/<username>/<age>')
def show_user_profile(username, age):
    return f'User: {username, age}'

# 2. 경로 변수: 슬래시(/)를 포함한 문자열을 받음
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath: {subpath}'

# 3. 정수형 변수: 정수 값을 받음
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post ID: {post_id}'

# 4. 부동소수점 변수: 부동소수점 값을 받음
@app.route('/pi/<float:pi_value>')
def show_pi(pi_value):
    return f'Pi value: {pi_value}'

# 5. URL 변수: 변수명만 사용하여 문자열을 받음 (기본값은 string과 동일)
@app.route('/item/')
@app.route('/item/<itemname>')
def show_item(itemname='기본값'):
    return f'Item: {itemname}'

# 6. jsonify로 josn으로 요청 처리. (MIME 타입 설정, 특수문자 처리, 유니코드 지원)
@app.route('/json')
def json_example():
    return jsonify({"key1": "value1", "key2": [1,2,3,4,"string", 3.14, True, None]})

# 7. GET 및 POST 요청 처리
@app.route('/message', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def handle_message():
    if request.method in ['POST', 'PUT', 'PATCH']:
        # 공통 데이터 처리
        message = request.form.get('message')
        username = request.form.get('username')
        response = {'method': request.method}

        if request.method == 'POST':
            response.update({'message': message, 'username': username})
        elif request.method == 'PUT':
            response.update({'message': message, 'username': username})
        elif request.method == 'PATCH':
            response.update({'message': message, 'username': username})

        return jsonify(response)

    elif request.method == 'DELETE':
        # DELETE 요청 처리
        return jsonify({'method': 'DELETE', 'message': 'Message deleted'})

    else:
        # GET 요청: 메시지와 사용자 이름 입력 폼 제공
        return render_template_string('''
            <!doctype html>
            <html lang="ko">                        
            <title>메시지 입력</title>
            <h1>메시지 입력</h1>
            <form method=post action="/message">
                <label for="message">메시지:</label>
                <input type=text name=message id="message"><br>
                <label for="username">사용자 이름:</label>
                <input type=text name=username id="username"><br>
                <input type=submit value=전송>
            </form>
        ''')
    

# 8. make_response로 상태코드와 헤더 지정
@app.route('/response')
def response_example():
    # 응답 바디, 상태코드
    resp = make_response("Add to Header", 200)
    # 헤더에 추가한 값
    resp.headers['Custom-Header'] = 'custom-value'
    resp.headers['Custom-Header2'] = 'custom-value2'
    return resp

# 9. url_for(bp명.함수명, 파라미터=값)로 동적으로 url 생성
# 10. redirect()으로 다른 주소로 리다이렉트
@app.route('/')
def index():
    # /user/john 으로 리다이렉트
    return redirect(url_for('show_user_profile', username='john'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
