from flask import Flask
from flask import request
from flask import render_template
import pymongo
from bson.objectid import ObjectId
from flask import redirect
from flask import session
import os
from dotenv import load_dotenv
import json
from flask import jsonify
import jinja2
load_dotenv()#呼叫 load_dotenv() 載入 .env 檔
GOOGLE_OAUTH2_CLIENT_ID = os.getenv("GOOGLE_OAUTH2_CLIENT_ID")
root = os.getenv("root")#讀取 .env 檔中，Key 為 SERVER_IP 的值
print(root)

app = Flask(
    __name__,
    static_folder="static",#靜態檔案的資料夾名稱
    static_url_path="/"#靜態檔案對應的網址路徑
    )# __name__ 代表目前執行的模組

client = pymongo.MongoClient("mongodb+srv://{}@clusternew.5zmm1ew.mongodb.net/?retryWrites=true&w=majority".format(root))
db = client.member#選擇要操作的（member)資料庫



app.secret_key="key value"

@app.route("/") #裝飾：以函式為基礎，提供附加功能
def home():
    return render_template("index.html", google_oauth2_client_id=GOOGLE_OAUTH2_CLIENT_ID)

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
@app.route("/article" ,methods=["POST"])
def create_article():
    if "email" in session:
        email = session["email"]
        title = request.form["title"]
        content = request.form["content"]
        collection = db.article
        
        collection.insert_one({
            "email" : email,
            "title" : title,
            "content" : content
        })

        return render_template("/article.html",title=title,content=content)
    else:
        return redirect("/")       
@app.route("/view_article")
def view_article():
    if "email" in session:
        email = session["email"]
        collection = db.article
        result= collection.find({
            "email" : email

        })
        articles = []
        for article in result:
            articles.append({
                "title": article["title"],
                "content": article["content"]
                            })
        return render_template("view_article.html", articles=articles)
        # return json.dumps({"articles": articles})
        # title=[]
        # content=[]
        # for x in result:
        #     content.append(x["content"])
        #     title.append(x["title"])
        #     print(title,content)
            
        # content = result["content"]
        # title = result["title"]
        # return render_template("/article.html",title=title,content=content)
        # return json.dumps(dict(title=title,content=content))
@app.route("/view2_article")
def view2_article():
    if "email" in session:
        email = session["email"]
        collection = db.article
        result = collection.find({"email": email})
        articles = []
        for x in result:
            articles.append({
                "title": x["title"],
                "content": x["content"]
            })
        return jsonify(articles)
    else:
        return redirect("/")
@app.route("/modify",methods=["POST"])
def modify_article():
    if "email" in session:
        email = session["email"]
        title = request.form["title"]
        modify_title=request.form["motitle"]
        content= request.form["content"]
        
        collection = db.article
        collection.replace_one({
            "title" : title
        },{
            "email" : email,
            "title" : modify_title,
            "content":content
            })#upsert?
        return "更動完成"
@app.route("/delete",methods=["POST"])
def delete_article():
    if "email" in session:
        
        title = request.form["title"]
        collection = db.article
        collection.delete_one({
            "title" : title
        })
        return "刪除完成"       

    
#/error?msg=錯誤訊息
@app.route("/error")
def error():
    message = request.args.get("msg","發生錯誤,請找客服")#抓要求字串（前面放要求字串,預設值）
    return render_template("error.html",mess = message)#（前面mess為html{{}}，後面message為py變數）
@app.route("/signin2")
def signin2():
    return render_template("signin2.html")

@app.route("/mo")
def mo():
    return render_template("modify.html")
@app.route("/de")
def de():
    return render_template("delete.html")




if __name__ =="__main__":#如果以主程式執行，如果把app.py當成主程式來運作
    app.debug = True
    app.run()

#先使用python 不要用python3

