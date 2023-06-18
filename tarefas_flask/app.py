from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Fazer(db.Model):
    task_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    feito=db.Column(db.Boolean)
    
@app.route('/')
def home():
    fazer_list=Fazer.query.all()
    return render_template('index.html',fazer_list=fazer_list)

@app.route('/add',methods=['POST'])
def add():
    name = request.form.get("name")
    new_task=Fazer(name=name, feito=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/atualizar/<int:fazer_id>')
def atualizar(fazer_id):
    fazer= Fazer.query.get(fazer_id)
    fazer.feito=not fazer.feito
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/delete/<int:fazer_id>')
def delete(fazer_id):
    fazer= Fazer.query.get(fazer_id)
    db.session.delete(fazer)
    db.session.commit()
    return redirect(url_for("home"))

if __name__=='__main__':
    app.run()