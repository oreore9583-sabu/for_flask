
import gettext

import keyword
from flask import Flask, render_template, request
from decimal import Decimal, DivisionByZero, InvalidOperation
from datetime import datetime
from zoneinfo import ZoneInfo
from markupsafe import Markup
import sqlite3
import re
from flask import g
from flask import jsonify

app = Flask(__name__)
def calc(data):
    while "**" in data:
        idx = data.index("**")

        base = Decimal(data[idx - 1])  # '2'
        exp = Decimal(data[idx + 1])  # '3'
        result = str(base**exp)

        # 計算に使った3つの要素を、計算結果の1つに置き換える
        data[idx - 1 : idx + 2] = [(result)]

    ii = 0
    while ii < len(data):
        if data[ii] == "/":
            base = Decimal(data[ii - 1])  # '2'
            exp = Decimal(data[ii + 1])  # '3'
            result = str(base / exp)  # '8'

            # 計算に使った3つの要素を、計算結果の1つに置き換える
            data[ii - 1 : ii + 2] = [(result)]
            ii = 0  # カウンタを最初に戻す

            continue  # whileの先頭に戻る

        # 何らかの理由で最初からやり直したい時
        elif data[ii] == "*":
            base = Decimal(data[ii - 1])  # '2'
            exp = Decimal(data[ii + 1])  # '3'
            result = str(base * exp)  # '8'
            data[ii - 1 : ii + 2] = [(result)]

            ii = 0  # カウンタを最初に戻す

            continue  # whileの先頭に戻る

        ii += 1  # 正常に終わったら次のステップへ

    i = 0
    while i < len(data):
        if data[i] == "+":
            base = Decimal(data[i - 1])  # '2'
            exp = Decimal(data[i + 1])  # '3'
            result = str(base + exp)  # '8'

            # 計算に使った3つの要素を、計算結果の1つに置き換える
            data[i - 1 : i + 2] = [(result)]

            i = 0  # カウンタを最初に戻す

            continue  # whileの先頭に戻る

        # 何らかの理由で最初からやり直したい時
        elif data[i] == "-":
            base = Decimal(data[i - 1])  # '2'
            exp = Decimal(data[i + 1])  # '3'
            result = str(base - exp)
            data[i - 1 : i + 2] = [result]

            i = 0
            
            continue

            # カウンタを最初に戻す

            # whileの先頭に戻る

            i += 1  # 正常に終わったら次のステップへ
        else:
            i += 1
    return data

def a(data):
    zi = 0
    while zi < len(data):
        if data[zi] == "-":
            if zi == 0 or data[zi - 1] in ["+", "-", "*", "/", "**", "("]:
                data[zi : zi + 2] = [data[zi] + data[zi + 1]]
                zi = 0
                continue
        zi += 1

def caco(data, kakuri):
    check_list = []

    qq = 1
    aq = 0

    while "(" in data and ")" in data:
        check_list = []
        aq = 0
        if "(" in data and ")" in data:
            for p in range(len(data)):
                if data[p] == "(":
                    aq += 1
                    check_list.append((aq, data[p]))
                elif data[p] == ")":
                    check_list.append((aq, data[p]))
                    aq -= 1

                else:
                    check_list.append((aq, data[p]))

        else:
            qq += 1
        ch = len(data)
        for i, listing in enumerate(check_list):
            if (
                listing[0] == max(x[0] for x in check_list)
                and listing[1] == "("
            ):
                inside_left = i

            elif (
                listing[0] == max(x[0] for x in check_list)
                and listing[1] == ")"
            ):
                inside_right = i

        data[inside_right] = "】"
        data[inside_left] = "【"

        data[inside_left : inside_right + 1] = calc(
            data[inside_left + 1 : inside_right]
        )

        qq = 0

    return kakuri



@app.route("/")
def index():
    fraud_input=""
    siki = request.args.get("siki")
    siki_for_else=siki
    check=""#一応残す
    result=None
    
    if siki:
        Error_check=["+/" in siki,"+*" in siki,"*/"in siki,"-*" in siki,"-/" in siki,"/*" in siki,"/+" in siki,"*+" in siki]
        if "++" in siki:
            fraud_input="+"
            check="dont"
        elif "//" in siki:
            fraud_input="/"
            check="dont"
        elif "***" in siki:
            fraud_input="*"
            check="dont"
        elif any(Error_check):
            fraud_input="演算子"
            check="dont"
        elif any([siki[0]=="+",siki[0]=="*",siki[0]=="/"]):
            fraud_input="式の始めに演算子を書かないでください"
            check="else_Error"
        elif any([siki[-1]=="+",siki[-1]=="-",siki[-1]=="*",siki[-1]=="/"]):
            fraud_input="式の終わりは演算子にしないでください"
            check="else_Error"
        elif "()" in siki:
            fraud_input="(と)の間は空にしないでください(なんかしらの式を書くかそもそも書かないで)"
            check="()Error"
        elif not siki.count("(")==siki.count(")"):
            fraud_input="()の数が同じになるようにしてください"
            check="()Error"
        elif re.search(r'[a-zA-Z]', siki) or re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', siki):
            fraud_input="正しい式を入力してください(アルファベットとか日本語は当然なし)"
            check="Foreign object contamination"


            
        
        
    try:
        if siki and check=="":

            siki = re.split(r"(\*\*|\*|\+|-|/|\(|\)|【|】)", siki)
            q = 1
            while q == 1:
                if "" in siki:
                    siki.pop(siki.index(""))
                else:
                    q = 0
            if "(" in siki and ")" in siki:
                left = siki.index("(")
                right = siki.index(")")
                a(siki)
    
            betu = []
            kakuri = []
            a(siki)
            caco(siki, kakuri)
            betu = calc(betu)
            if "(" in siki and ")" in siki:
                siki[left : right + 1] = betu
    
            siki = calc(siki)
    
            result = siki[0]
    except DivisionByZero:
        result="0で割ることはできません"
        check="DivisionByZero"
    if fraud_input:
        if check=="()Error"or check=="else_Error"or check=="Foreign object contamination":
            result=fraud_input
        
        else:
            result=f"{fraud_input}は連続させないでください"
        
    elif result is None:
        result="式を入力してください"
    if siki_for_else is None:
        siki_for_else=""

    else:
        siki_for_else+="="

    if request.args.get("ajax")=="1":


        for_json={"siki":siki_for_else,"result":result}
        return jsonify(for_json)
        
    return render_template("index.html", result=result, siki=siki_for_else)




@app.route("/add")
def add():
    a = request.args.get("a")
    b = request.args.get("b")
    if not a is None and not b is None:
        try:
            ans = Decimal(a) + Decimal(b)

        except InvalidOperation:
            ans = "数字を入力してください"
    else:
        ans = ""
    return render_template("add.html", ans=ans)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
