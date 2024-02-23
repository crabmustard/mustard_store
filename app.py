from flask import (
    Flask,
    render_template,
    request,
    redirect
)
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
ff = Faker()


class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    citystate = db.Column(db.String(50))
    email = db.Column(db.String(50))
    college = db.Column(db.String(50))
    grade = db.Column(db.String(5))
    job = db.Column(db.String(50))

    def __repr__(self):
        return f'{self.name} - {self.email} - {self.job}'
    
def coverletter():
    letter = ff.paragraphs(nb=4)
    return letter

def make_applicant():
    name = ff.name()
    citystate = ff.city() +', '+ ff.state_abbr()
    email = ff.ascii_safe_email()
    college = ff.state() + ff.random.choice([' University', ' State', ' Polytech', ', University of'])
    grade = ff.random.choice(['A','A+','A-','B','B+','B-','F'])
    job = ff.job()
    applicant = Applicant(name=name, citystate=citystate, email=email,
                            college=college, grade=grade, job=job)
    return applicant


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        for _ in range(ff.random.randint(2,5)):
            new_applicant = make_applicant()
            try:
                db.session.add(new_applicant)
                db.session.commit()
            except:
                return 'there was an issue adding task'
        return redirect('/')
        
    else:
        applicants = Applicant.query.order_by(Applicant.id).all()
        return render_template('index.html', applicants=applicants)
    
@app.route('/delete/<int:id>')
def delete(id):
    applicant_to_delete = Applicant.query.get_or_404(id)

    try:
        db.session.delete(applicant_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'there was a problem deleting that applicant'

@app.route('/details/<int:id>')
def show_details(id):
    to_view = Applicant.query.filter_by(id=id).first()
    cover_letter = coverletter()
    return render_template('applicant.html', to_view=to_view, cover_letter=cover_letter)

@app.route('/update/')
def update_page():
    return render_template('update.html')



if __name__ == "__main__":
    app.run(debug=True)

