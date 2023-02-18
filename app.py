from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

# client = MongoClient('localhost', 27017)
# mongoDB는 27017 포트로 돌아갑니다.
client = MongoClient('mongodb+srv://test:sparta@cluster0.ecijcpt.mongodb.net/?retryWrites=true&w=majority') #cloud
db = client.dbjungle  # 'dbjungle'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    memo_receive = request.form['memo_give']  # 클라이언트로부터 url을 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

    memo_list = list(db.memos.find({},{'_id':False}))
    name = len(memo_list) + 1

    memos = {
        'name': name,
        'memo': memo_receive,
        'comment': comment_receive,
        'like':0,
        'type':0
    }

    # 3. mongoDB에 데이터를 넣기
    db.memos.insert_one(memos)

    return jsonify({'result': 'success'})



@app.route('/memo', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.memos.find({}, {'_id': False}).sort('like', -1))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'memos': result})



@app.route('/memo/like', methods=['POST'])
def like_memo():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']

    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    memo = db.memos.find_one({'name': int(name_receive)})
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_like = memo['like'] + 1

    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    # 참고: '$set' 활용하기!
    db.memos.update_one({'name': int(name_receive)}, {'$set': {'like': new_like}})

    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})



@app.route('/memo/delete', methods=['POST'])
def delete_memo():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.memos.delete_one({'name': int(name_receive)})

    #name 재설정 해주기!

    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})



@app.route('/memo/modify', methods=['POST'])
def modified_memo():
    name_receive = request.form['name_give']
    memo_receive = request.form['memo_give']  # 클라이언트로부터 url을 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

    new_memo = memo_receive;
    new_comment = comment_receive;

    db.memos.update_one({'name': int(name_receive)}, {'$set': {'memo': new_memo}}, {'$set': {'comment': new_comment}}, {'$set': {'type': 1}})


    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)