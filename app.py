from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.ecijcpt.mongodb.net/?retryWrites=true&w=majority') #cloud
# mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle  # 'dbjungle'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['POST'])
def post_article():
    memo_receive = request.form['memo_give']
    comment_receive = request.form['comment_give']

    memo_list = list(db.memos.find({},{'_id':False}))
    name = len(memo_list) + 1

    memos = {
        'name': name,
        'memo': memo_receive,
        'comment': comment_receive,
        'like':0,
        'type':0
    }
    db.memos.insert_one(memos)

    return jsonify({'result': 'success'})



@app.route('/memo', methods=['GET'])
def read_articles():
    result = list(db.memos.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'result': 'success', 'memos': result})



@app.route('/memo/like', methods=['POST'])
def like_memo():
    name_receive = request.form['name_give']

    memo = db.memos.find_one({'name': int(name_receive)})
    new_like = memo['like'] + 1

    db.memos.update_one({'name': int(name_receive)}, {'$set': {'like': new_like}})

    return jsonify({'result': 'success'})



@app.route('/memo/delete', methods=['POST'])
def delete_memo():

    name_receive = request.form['name_give']
    db.memos.delete_one({'name': int(name_receive)})

    return jsonify({'result': 'success'})



@app.route('/memo/modify', methods=['POST'])
def modified_memo():
    name_receive = request.form['name_give']
    memo_receive = request.form['memo_give']
    comment_receive = request.form['comment_give']

    new_memo = memo_receive;
    new_comment = comment_receive;

    db.memos.update_one({'name': int(name_receive)}, {'$set': {'memo': new_memo}});
    db.memos.update_one({'name': int(name_receive)}, {'$set': {'comment': new_comment}});
    db.memos.update_one({'name': int(name_receive)}, {'$set': {'type': 0}});

    return jsonify({'result': 'success'})



@app.route('/memo/modifystart', methods=['POST'])
def modifystart_memo():
    name_receive = request.form['name_give']
    db.memos.update_one({'name': int(name_receive)}, {'$set': {'type': 1}})

    return jsonify({'result': 'success'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)