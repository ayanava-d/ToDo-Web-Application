from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.content}'


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo(content= title, desc=desc)
        db.session.add(todo)
        db.session.commit()    
    allToDo = ToDo.query.all()
    return render_template('index.html', allToDo=allToDo)


@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):  
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.content = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = ToDo.query.filter_by(sno=sno).first()    
    return render_template('update.html', todo=todo)  


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__=='__main__':
    app.run(debug=True)