from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class ToDo(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    issueDate = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def greet():
    if request.method == "POST":
        todo = ToDo(title=request.form['title'], desc=request.form['desc'])
        db.session.add(todo)
        db.session.commit()
        
    showAllRec = ToDo.query.all()
    return render_template('index.html', showAllRec=showAllRec)

@app.route('/update/<int:sr_no>', methods=['GET', 'POST'])
def update(sr_no):
    if request.method == 'POST':
        updateRec = ToDo.query.filter_by(sr_no=sr_no).first()
        updateRec.title = request.form['title']
        updateRec.desc = request.form['desc']
        db.session.add(updateRec)
        db.session.commit()
        return redirect('/')

    updateRec = ToDo.query.filter_by(sr_no=sr_no).first()
    return render_template('update.html', updateRec=updateRec)

@app.route('/delete/<int:sr_no>')
def delete(sr_no):
    delRec = ToDo.query.filter_by(sr_no=sr_no).first()
    db.session.delete(delRec)
    db.session.commit()
    return redirect('/')
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run()
