from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ToDo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

    
with app.app_context():
    db.create_all()

@app.route('/', methods =['GET', 'POST'])
def hello_world():
    if request.method== 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = ToDo(title = title, description = description)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('hello_world'))
    

    allToDo = ToDo.query.all()
    return render_template('index.html', allToDo = allToDo)
    #return'Hello, World!'

@app.route('/show')
def products():
    allToDo = ToDo.query.all()
    print(allToDo)
    return'this is product page.'

@app.route('/update/<int:sno>', methods =['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.description=description
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

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', code=404, message="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    db.session.rollback()
    return render_template('error.html', code=500, message="Something went wrong"), 500

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
    #app.run(debug = False, port = 8000)

