import math
import time

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:////Users/Sudharsan/Desktop/TCS/midaas/trialapp/prime.db'
# 'C:/Users/Sudharsan/Desktop/TCS/midaas/trialapp/prime.db'
db = SQLAlchemy(app)

app.secret_key = 'hello'


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    star_number = db.Column(db.BigInteger())
    end_number = db.Column(db.BigInteger())
    algorithm = db.Column(db.String(80))
    time_elapse = db.Column(db.BigInteger())


## Basic, Medium, Advance Algorithm ##
def adv_alg(n):
  for i in range(2,int(math.sqrt(n))+1):
    if (n%i) == 0:
      return False
  return True


def medium_alg(n):
  for i in range(2,int(n/2)+1):
    if (n%i) == 0:
      return False
  return True


def basic_alg(n):
  for i in range(2,n):
    if (n%i) == 0:
      return False
  return True

## Basic, Medium, Advance Algorithm ##

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":

        star_number = request.form.get("star_number",type=int)
        end_number = request.form.get("end_number",type=int)
        algorithm = request.form["algorithm"]

        if star_number > end_number:
            numb = list(range(star_number, end_number, -1))
        else:
            numb = list(range(star_number, end_number))

        # numb = list(range(star_number, end_number))
        if algorithm=="basic":
            start = time.time()
            result = list(filter(basic_alg, numb))
            end = time.time()
            time_elapse = end - start
            print(result)
            print(time_elapse, "basic_alg")
        elif algorithm=="medium":
            start = time.time()
            result = list(filter(medium_alg, numb))
            end = time.time()
            time_elapse = end - start
            print(result)
            print(time_elapse, "basic_alg")
        else:
            start = time.time()
            result = list(filter(adv_alg, numb))
            end = time.time()
            time_elapse = end - start
            print(result)
            print(time_elapse, "adv_alg")

        messg = f'''Prime number between the selected range {star_number} to {end_number} are: 
                    {result} \n
                    and the time-elapsed is {time_elapse} '''

        # print(select(user_table.c.name, user_table.c.fullname))
        # ok = user.query.filter(user.id).all()
        # print(ok,type(ok),'*********')



        uplode = user(star_number=star_number, end_number=end_number, algorithm=algorithm, time_elapse=time_elapse)
        db.session.add(uplode)
        db.session.commit()


        database = user.query.all()
        print(database, type(database))
        full_db = []
        for i in database:
            # full = i.id,i.algorithm,i.star_number,i.end_number,i.time_elapse
            full_db.append(f'''{i.id},{i.algorithm},{i.star_number},{i.end_number},{i.time_elapse}''')
            print(i.id, i.algorithm, i.star_number, i.end_number, i.time_elapse)



        return render_template('app.html',messg=messg,database=database)
    return render_template('app.html')











if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5027)