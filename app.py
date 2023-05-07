from flask import Flask, render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onlinejournal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class OnlineJournal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    author = db.Column(db.String(200), nullable = False)
    contact = db.Column(db.String(50), nullable = True)
    published = db.Column(db.DateTime, default = datetime.utcnow)
    journal = db.Column(db.String(2000), nullable = False)

    def __repr__(self):
        return '<Journal %r>' %self.id
    

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        author = request.form['author']
        contact = request.form['contact']
        journal = request.form['journal']
        new_journal = OnlineJournal(id = id, title = title, author = author, contact = contact, journal = journal)
        try:
            db.session.add(new_journal)
            db.session.commit()
            return redirect('/')
        except :
            return "There was a Probelm Adding new Journal!"
    else:
        journals = OnlineJournal.query.order_by(OnlineJournal.published).all()
        return render_template('index.html', journals = journals)
    

@app.route('/delete/<int:id>')
def delete(id):
    journal_to_delete = OnlineJournal.query.get_or_404(id)
    try:
        db.session.delete(journal_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a Probelm Deleting the Journal!"
    

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    journal = OnlineJournal.query.get_or_404(id)
    if request.method == 'POST':
        journal.id = request.form['id']
        journal.title = request.form['title']
        journal.author = request.form['author']
        journal.contact = request.form['contact']
        journal.journal = request.form['journal']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a Probelm Updating the Journal!"
    else:
        return render_template('update.html',journal = journal)
    

@app.route('/read/<int:id>',methods=['GET','POST'])
def read(id):
    journal = OnlineJournal.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('read.html',journal = journal)
    elif request.method == 'POST':
        return redirect('/')
    else:
        return "There was a Probelm Fetching the Journal!"
        


if __name__ == "__main__":
    app.run(debug=True)