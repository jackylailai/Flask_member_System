from flask import Flask
from flask import request
from flask import render_template
import pymongo
from bson.objectid import ObjectId
from flask import redirect
from flask import session
import os
from dotenv import load_dotenv
load_dotenv()#呼叫 load_dotenv() 載入 .env 檔

root = os.getenv("root")#讀取 .env 檔中，Key 為 SERVER_IP 的值
print(root)

app = Flask(
    __name__,
    static_folder="public",#靜態檔案的資料夾名稱
    static_url_path="/"#靜態檔案對應的網址路徑
    )# __name__ 代表目前執行的模組

client = pymongo.MongoClient("mongodb+srv://{}@clusternew.5zmm1ew.mongodb.net/?retryWrites=true&w=majority".format(root))
db = client.member#選擇要操作的（member)資料庫



app.secret_key="key value"

@app.route("/") #裝飾：以函式為基礎，提供附加功能
def home():
    return render_template("index.html")

@app.route("/signup",methods=["POST"])#method+s
def signup():
    name = request.form["name"]#[對應到前端form的"name"]記得：“”
    email = request.form["email"]
    password = request.form["password"]
    collection = db.users#選擇操作 users集合
#把資料新增到集合中
    result=collection.find_one({
        "email" : email
    })
    if result!= None:
        return redirect("/error?msg=信箱已經註冊")
    collection.insert_one({
        "name" : name,
        "email" : email,
        "password" : password#記得要逗號
    })
    return "註冊ok"
@app.route("/signin",methods=["POST"])#要中括弧
def signin():
    email=request.form["email"]
    password = request.form["password"]
    collection = db.users
    result = collection.find_one({
        "$and":[#記得“”然後:中括弧
        {"email":email},
        {"password":password}
        ]
    })#要各別{}#記得要逗號
    if result==None:
        return redirect("/error?msg=輸入錯誤")
    print("輸入成功")
    session["email"]=result["email"]#記得“”
    return redirect("/member")#要“”
@app.route("/signout")
def signout():
    del session["email"]
    return redirect("/")
@app.route("/member")
def member():
    if "email" in session:
        return render_template("/member.html")
    else:
        return redirect("/")
#/error?msg=錯誤訊息
@app.route("/error")
def error():
    message = request.args.get("msg","發生錯誤,請找客服")#抓要求字串（前面放要求字串,預設值）
    return render_template("error.html",mess = message)#（前面mess為html{{}}，後面message為py變數）
@app.route("/signin2")
def signin2():
    return render_template("signin2.html")
if __name__ =="__main__":#如果以主程式執行，如果把app.py當成主程式來運作
    app.run()

#先使用python 不要用python3

