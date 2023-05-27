import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import requests

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client(DB_NAME)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/mars", methods=["POST"])
def mars_post():
    nama_receive = request.form['nama_give']
    alamat_receive = request.form['alamat_give']
    luas_receive = request.form['luas_give']
    
    doc = {
        "nama" : nama_receive,
        "alamat" : alamat_receive,
        "luas" : luas_receive
    }
    db.order.insert_one(doc)
    return jsonify({'msg': 'Berhasil Melakukan Pembelian!'})

@app.route("/mars", methods=["GET"])
def mars_get():
    orders_list = list(db.order.find({},{'_id':False}))
    return jsonify({'orders':orders_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)