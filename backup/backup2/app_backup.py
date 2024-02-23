from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<{self.id} {self.content}>'
    

class ShopMustard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric, default=0)
    quantity = db.Column(db.Integer, nullable=False)
    delivered = db.Column(db.DateTime, default=datetime.utcnow)
    has_image = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<{self.id} {self.name} {self.quantity}>'


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        mustard_content = request.form['content']
        new_mustard = Todo(content=mustard_content)

        try:
            db.session.add(new_mustard)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding task'
        
    else:
        mustard = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', mustards=mustard)
    
@app.route('/delete/<int:id>')
def delete(id):
    mustard_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(mustard_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'there was a problem deleting that mustard'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    mustard_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        mustard_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was an issue.'
    else:
        return render_template('update.html', mustard=mustard_to_update)
    

if __name__ == "__main__":
    app.run(debug=True)

