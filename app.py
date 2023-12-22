from flask import Flask,render_template,request
import pandas as pd
import mysql.connector
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error,mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import ExtraTreeRegressor




mydb = mysql.connector.connect(host='localhost',user='root',password='',port='3306',database='Crop_yield')
cur = mydb.cursor()


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        psw = request.form['psw']
        sql = "SELECT * FROM crop WHERE Email=%s and Password=%s"
        val = (email, psw)
        cur = mydb.cursor()
        cur.execute(sql, val)
        results = cur.fetchall()
        mydb.commit()
        if len(results) >= 1:
            return render_template('loginhome.html', msg='login succesful')
        else:
            return render_template('login.html', msg='Invalid Credentias')

    return render_template('login.html')

@app.route('/loginhome')
def loginhome():
    return render_template('loginhome.html')






@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method == "POST":
        print('a')
        name = request.form['name']
        print(name)
        email = request.form['email']
        pws = request.form['psw']
        print(pws)
        cpws = request.form['cpsw']
        if pws == cpws:
            sql = "select * from crop"
            print('abcccccccccc')
            cur = mydb.cursor()
            cur.execute(sql)
            all_emails = cur.fetchall()
            mydb.commit()
            all_emails = [i[2] for i in all_emails]
            if email in all_emails:
                return render_template('registration.html', msg='success')
            else:
                sql = "INSERT INTO crop(name,email,password) values(%s,%s,%s)"
                values = (name, email, pws)
                cur.execute(sql, values)
                mydb.commit()
                cur.close()
                return render_template('login.html', msg='success')
        else:
            return render_template('login.html', msg='password not matched')

    return render_template('registration.html')


@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == "POST":
        file = request.files['file']
        print(file)
        global df
        df = pd.read_csv(file)
        print(df)
        return render_template('upload.html', columns=df.columns.values, rows=df.values.tolist(),msg='Data is uploaded')
    return render_template('upload.html')
@app.route('/viewdata')
def viewdata():
    print(df.columns)
    df_sample = df.head(70000)
    return render_template('viewdata.html', columns=df_sample.columns.values, rows=df_sample.values.tolist())


@app.route('/preprocessing',methods=['POST','GET'])
def preprocessing():
    global X, y, X_train, X_test, y_train, y_test
    if request.method == "POST":
        size = int(request.form['split'])
        size = size / 100
        print(size)

        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=52)
        print(X_train)
        print(X_train.columns)
        return render_template('preprocessing.html', msg='Data Preprocessed and It Splits Succesfully')

    return render_template('preprocessing.html')



@app.route('/model',methods=['POST','GET'])
def model():
    if request.method=='POST':
        models = int(request.form['algo'])
        if models==1:
            print("==")
            model = RandomForestRegressor()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            acc = r2_score(y_pred,y_test)
            acc = acc*100
            msg = 'R2_score  for Random Forest is ' + str(acc) + str('%')

        elif models== 2:
            print("======")
            model = DecisionTreeRegressor()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            acc = r2_score(y_pred, y_test)
            acc = acc * 100
            msg = 'R2_score  for Decision Tree is ' + str(acc) + str('%')

        elif models==3:
            print("===============")
            model = SVR()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            acc = r2_score(y_pred,y_test)
            acc = acc*100
            msg = 'R2_score  for SVR is ' + str(acc) + str('%')
        elif models == 4:
            print("===============")
            model = BaggingRegressor()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = r2_score(y_pred, y_test)
            acc = acc * 100
            msg = 'R2_score  for Bagging Regressor is ' + str(acc) + str('%')
        elif models == 5:
            print("===============")
            model = GradientBoostingRegressor()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = r2_score(y_pred, y_test)
            acc = acc * 100
            msg = 'R2_score  for Gradient Boosting is ' + str(acc) + str('%')
        elif models == 6:
            print("===============")
            model = KNeighborsRegressor()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = r2_score(y_pred, y_test)
            acc = acc * 100
            msg = 'R2_score  for KNN is ' + str(acc) + str('%')
        elif models == 7:
            print("===============")
            model = ExtraTreeRegressor()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = r2_score(y_pred, y_test)
            acc = acc * 100
            msg = 'R2_score  for ExtraTreeRegressor is ' + str(acc) + str('%')
        return render_template('model.html',msg=msg)

    return render_template('model.html')
@app.route('/prediction',methods=['POST','GET'])
def prediction():
    print('111111')
    if  request.method == 'POST':
        print('2222')
        State = request.form['State']
        print(State)
        Year =request.form['Year']
        print(Year)
        Crop =request.form['Crop']
        print(Crop)
        Area = request.form['Area']
        print(Area)
        Rain = request.form['Rain']
        print(Rain)

        m = [State,Year,Crop,Area,Rain]
        model = RandomForestRegressor()
        model.fit(X_train,y_train)
        result = model.predict([m])
        print(result)
        msg = 'The prediction value is ' + str(result)
        return render_template('prediction.html',msg=msg)

    return render_template('prediction.html')

@app.route("/graph",methods=['GET','POST'])
def graph():
    if request.method=="POST":
        modelname=request.form['modelgraph']
        print(modelname)
        if modelname=="r2score":
            return render_template("graph.html",modelname="r2score")
        elif modelname=='Mean_squared':
            return render_template("graph.html",modelname='Mean_squared')
        elif modelname=='mean_absolute':
            return render_template("graph.html",modelname='mean_absolute')

            pass
    return render_template('graph.html')


if __name__=="__main__":
    app.run(debug=True)

