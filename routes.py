from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import SignupForm , LoginForm
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:asmaasma@localhost:5432/learningflask'
SQLALCHEMY_TRACK_MODIFICATIONS = True
db.init_app(app)

app.secret_key = "development key"

@app.route("/")
def index():
	return render_template("index.html")
@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/signup",methods=["GET","POST"])	
def signup():
	if 'email' in session:
		email = session['email']
		user = User.query.filter_by(email=email).first()
		if user.isactive:
			return redirect(url_for('home')) 

	form = SignupForm()
	if request.method == "POST":
		if form.validate() == False:
			return render_template("signup.html", form=form)
		else:	
			newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data, False)
			db.session.add(newuser)
			db.session.commit()
			return 'you can access your account as soon as it is activated by our users'
	elif request.method == "GET":	
		return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
	if 'email' in session:
		return redirect(url_for('home'))

	form = LoginForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("login.html", form=form)
		else:
			email = form.email.data
			password = form.password.data

			user = User.query.filter_by(email=email).first()
			if user is not None and user.check_password(password):
				session['email'] = form.email.data
				return redirect(url_for('home'))
			else:
				return redirect(url_for('login'))
	elif request.method == "GET":
		return render_template('login.html',form=form)					


@app.route("/home")
def home():
	email = session['email']
	user = User.query.filter_by(email=email).first()
	if 'email' not in session:
		return redirect(url_for('login'))
	if user.isactive:	
		users = User.query.all()
		return render_template("home.html", users=users)
	else:
		return 'you are not activated yet :p' 			
@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('index'))
@app.route('/<username>')
def active(username):
	user = User.query.filter_by(firstname=username).first()
	if user is not None:
		user.isactive = True
		db.session.commit()
	users = User.query.all()
	return redirect(url_for('home'))
if __name__ == "__main__":
	app.run(debug=True)	
