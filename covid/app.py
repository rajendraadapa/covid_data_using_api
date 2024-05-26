from flask import Flask,render_template,redirect,url_for,request
import requests 
from flask_mysqldb import MySQL

app= Flask(__name__)


app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="covid_db"


mysql=MySQL(app)



@app.route("/")
def home():
    return render_template('home.html')

@app.route("/country",methods=['GET','POST'])
def country():
    if request.method== 'POST':
        country = request.form['country']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM covid WHERE country=%s",[country])
        data=cur.fetchone()
        cur.close()
        return render_template("country_data.html",data=data)
    
    return render_template('country.html')





@app.route('/index',methods=['GET','POST'])
def index():
    response = requests.get("https://disease.sh/v3/covid-19/countries")
    if response.status_code == 200:
        data = response.json()
        store_db(data)
        
        
    
    cur= mysql.connection.cursor()
    cur.execute("SELECT * FROM covid")
    covid_data= cur.fetchall()
    return render_template('covid_data.html',covid_data=covid_data)
    
        
def store_db(data):
    cur= mysql.connection.cursor()
    cur.execute("TRUNCATE TABLE covid")
    for i in data:

        country=i['country']
        continent=i['continent']
        cases=i['cases']
        deaths=i['deaths']
        recovered=(cases-deaths)
        
        cur.execute("INSERT INTO covid (country,continent,cases,deaths,recovered) VALUES(%s,%s,%s,%s,%s)",(country,continent,cases,deaths,recovered))
        
    mysql.connection.commit()
        
    
    

if __name__ =="__main__":
    app.run(debug=True)



