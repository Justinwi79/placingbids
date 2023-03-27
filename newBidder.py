"""
Name: Harold Justin Windham
Date: 10/23/2022
Assignment: Module 8: Send Authenticated Message
Due Date: 10/23/2022
About this project: This script authenticates messages sent in browser
Assumptions: N/A
All work below was performed by Harold Justin Windham
"""

"""
References: Dr. Works modules and videos. 
"""
from flask import Flask, render_template, request, Blueprint, session, flash
import sqlite3 as sql
import os
import string
import base64
import Encryption
import pandas as pd

app = Flask(__name__)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['admin'] = -99
    return home()


@app.route('/login', methods=['POST'])
def do_admin_login():
    try:
        name = request.form['username']
        pwd = request.form['password']

        nm = str(Encryption.cipher.encrypt(bytes(name, 'utf-8')).decode("utf-8"))
        pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))

        # print(nm,pwd)

        with sql.connect("FlaskDB.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            sql_select_query = """select * from Bidder where Name = ? and LoginPassword = ?"""
            cur.execute(sql_select_query, (nm, pwd))

            row = cur.fetchone();
            if (row != None):
                session['logged_in'] = True
                session['name'] = name
                session['SecurityLevel'] = int(row['AppRoleLevel'])
                userId = int(row[0])
                session['user_id'] = userId
            else:
                session['logged_in'] = False
                flash('invalid username and/or password!')
    except:
        con.rollback()
        flash("error in logging in")
    finally:
        con.close()
    return home()


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', name=session['name'])


@app.route('/enternew')
def new_secretAgent():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('SecurityLevel') == 1:
        return render_template('newBidder.html')
    else:
        return render_template("result.html", msg="page not found")


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('SecurityLevel') == 1 and request.method == 'POST':
        try:
            error = False
            nm = request.form['Name']
            phNum = request.form['PhoneNumber']
            PrequalifiedUpperLimit = request.form['PrequalifiedUpperLimit']
            AppRoleLevel = request.form['AppRoleLevel']
            pwd = request.form['Password']

            nm = str(nm).lstrip()
            phNum = str(phNum).lstrip()
            pwd = str(pwd).lstrip()

            msg = "\n"
            if (len(nm) == 0):
                error = True
                msg += "You can not enter in an empty name \n"

            if (len(phNum) == 0):
                error = True
                msg += "You can not enter in an empty phone number \n"

            try:
                if (float(PrequalifiedUpperLimit) <= 0):
                    error = True
                    msg += "The Prequalified Upper Limit must be a numeric greater than 0. \n"
            except ValueError:
                error = True
                msg += "The Prequalified Upper Limit must be a numeric greater than 0. \n"

            try:
                if ((int(AppRoleLevel) <= 0) or (int(AppRoleLevel) > 3)):
                    error = True
                    msg += "The AppRoleLevel must be a numeric between 1 and 3. \n"
            except ValueError:
                error = True
                msg += "The AppRoleLevel must be a numeric between 1 and 3. \n"

            if (len(pwd) == 0):
                error = True
                msg += "You can not enter in an empty pwd \n"

            if (not (error)):
                nm = str(Encryption.cipher.encrypt(bytes(nm, 'utf-8')).decode("utf-8"))
                phNum = str(Encryption.cipher.encrypt(bytes(phNum, 'utf-8')).decode("utf-8"))
                pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))

                with sql.connect("FlaskDB.db") as con:
                    cur = con.cursor()

                    cur.execute(
                        "INSERT INTO Bidder (Name,PhoneNumber,PrequalifiedUpperLimit,AppRoleLevel,LoginPassword) VALUES (?,?,?,?,?)",
                        (nm, phNum, PrequalifiedUpperLimit, AppRoleLevel, pwd))

                    con.commit()
                    msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('SecurityLevel') == 1 or session.get('SecurityLevel') == 2:
        con = sql.connect("FlaskDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select Name, PhoneNumber, PrequalifiedUpperLimit, AppRoleLevel, LoginPassword from Bidder")
        df = pd.DataFrame(cur.fetchall(),
                          columns=['Name', 'PhoneNumber', 'PrequalifiedUpperLimit', 'AppRoleLevel', 'LoginPassword']);

        index = 0
        for nm in df['Name']:
            # print("before = ",nm)
            nm = str(Encryption.cipher.decrypt(nm))
            # print("after = ",nm)
            df._set_value(index, 'Name', nm)
            index += 1

        index = 0
        for phNum in df['PhoneNumber']:
            # print("before = ",alias)
            phNum = str(Encryption.cipher.decrypt(phNum))
            # print("after = ",alias)
            df._set_value(index, 'PhoneNumber', phNum)
            index += 1

        index = 0
        for pwd in df['LoginPassword']:
            # print("before = ",pwd)
            pwd = str(Encryption.cipher.decrypt(pwd))
            # print("after = ",pwd)
            df._set_value(index, 'LoginPassword', pwd)
            index += 1

        return render_template("list.html", rows=df)


@app.route('/auctionItemList')
def auctionItemList():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('SecurityLevel') == 1 or session.get('SecurityLevel') == 2:
        conn = sql.connect("SilentAuction.db")  # The SilentAuction database
        conn.row_factory = sql.Row  # Create rows for a table

        cur = conn.cursor()  # Initiate a cursor
        cur.execute("""Select * from AuctionItem""")  # Obtain data from our database table AuctionItem
        rows = cur.fetchall();
                         #  columns=['ItemName', 'ItemDesc', 'LowerBidLimit', 'HighestBidderId', 'HighestBidAmnt']

        return render_template('auctionItemList.html', rows=rows)  # Return a html page of a table with our data
    else:
        msg = "Page not found."
        return render_template('result.html', msg=msg)


if __name__ == '__main__':
    # a secret key os required for Flask.session
    app.secret_key = os.urandom(12)
    app.session_protection = "strong"
    # session = SecureCookieSession()
    app.run()
