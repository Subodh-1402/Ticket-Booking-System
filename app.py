from flask import Flask, render_template, request, url_for, redirect, flash
from flask.globals import app_ctx
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = "Secret Key"

# connection to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/train'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


class BookTicket(db.Model):
    idno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(200))
    lname = db.Column(db.String(200))
    from1 = db.Column(db.String(200))
    to1 = db.Column(db.String(200))
    DepartDate = db.Column(db.Date)
    seats = db.Column(db.Integer)

    def __init__(self, fname, lname, from1, to1, DepartDate, seats):
        self.fname = fname
        self.lname = lname
        self.from1 = from1
        self.to1 = to1
        self.DepartDate = DepartDate
        self.seats = seats

# URL for home page
@app.route('/', methods=['GET', 'POST'])
def login():
    print('inside login1')

    if request.method == 'POST':

        username1=request.form.get('username')
        pwd1= request.form.get('password')

        print('usename')
        if username1 =='subodh' and pwd1=='123':
            print('enter login')

            return redirect(url_for('index'))

        else:
            # flash('uname or pwd wrong')
            return render_template('login.html')
    print('inside login')
    return render_template('login.html')



@app.route('/index')
def index():

        return render_template('index.html')


#  execute store function while click on Let's Book button
@app.route('/store', methods=['POST'])
def store():
    if request.method == 'POST':

        firstname = request.form['FirstName']
        lastname = request.form['LastName']
        from1 = request.form['from1']
        to1 = request.form['to1']
        date = request.form['date']
        seats = request.form['seats']

        my_data = BookTicket(firstname, lastname, from1, to1, date, seats)

        try:
            db.session.add(my_data)
            db.session.commit()

            flash('Booked Successfully')

            return redirect(url_for('index'))

        except Exception:
            flash('Please fill all fields')
            return redirect(url_for('index'))
        return redirect(url_for('index'))

    else:
        return render_template('index.html', response='Something Wrong 1')


# execute this function while click on show bookings button
@app.route('/fetch', methods=['GET'])
def fetch():
    if request.method == 'GET':

        try:
            all_Data=BookTicket.query.all()
            print(all_Data)
            return render_template('index.html', BookingPanel=all_Data)

        except Exception:
            return render_template('index.html', response='Something wrong 2')
    else:
        return render_template('index.html', response='Something Wrong 3')


# execute update function while click on edit button
@app.route('/update', methods=['POST','GET'])
def update():
    id = request.form.get('id')

    updatedata = BookTicket.query.get(id)

    updatedata.fname=request.form['firstname']
    updatedata.lname=request.form['lastname']
    updatedata.from1=request.form['fromdest']
    updatedata.to1=request.form['todest']
    updatedata.DepartDate=request.form['departuredate']
    updatedata.seats=request.form['seats1']

    try:
        db.session.commit()
        flash('Book updated successfully')
        return redirect(url_for('index'))
    except Exception:
        db.session.rollback()
        flash('An error occurred while updating the book')
        return redirect(url_for('index'))


# execute this function while click on delete button
@app.route('/delete/<id>/', methods=['POST','GET'])
def delete(id):
    mydata=BookTicket.query.get(id)
    db.session.delete(mydata)
    db.session.commit()
    flash('Ticket deleted succesfully')
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
