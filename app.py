from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Bracelet, Order
from forms import BraceletForm, OrderForm
import os
from dotenv import load_dotenv

load_dotenv()

# Path setup
basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, 'data')
os.makedirs(data_dir, exist_ok=True)

# App config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(data_dir, 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD'):
            session['admin_logged_in'] = True
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

# HOME PAGE – PUBLIC ORDER FORM
@app.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    form.bracelet_id.choices = [(b.id, f"{b.name} (${b.price:.2f})") for b in Bracelet.query.all()]

    if form.validate_on_submit():
        bracelet = Bracelet.query.get(form.bracelet_id.data)
        if bracelet and bracelet.quantity >= form.quantity.data:
            order = Order(
                buyer_name=form.buyer_name.data,
                student_name=form.student_name.data,
                grade=form.grade.data,
                bracelet_id=form.bracelet_id.data,
                quantity=form.quantity.data,
                payment_note=form.payment_note.data
            )

            bracelet.quantity -= form.quantity.data
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('confirm'))
        else:
            flash('Not enough bracelets in stock!', 'danger')
    return render_template('index.html', form=form)

# CONFIRMATION PAGE
@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

# ADMIN PAGE – INVENTORY MANAGEMENT
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    form = BraceletForm()
    bracelets = Bracelet.query.all()

    if form.validate_on_submit():
        existing = next((b for b in bracelets if b.name.lower() == form.name.data.lower()), None)
        if existing:
            existing.price = form.price.data
            existing.quantity = form.quantity.data
        else:
            new_bracelet = Bracelet(
                name=form.name.data,
                price=form.price.data,
                quantity=form.quantity.data
            )
            db.session.add(new_bracelet)
        db.session.commit()
        flash('Bracelet added or updated!', 'success')
        return redirect(url_for('admin'))

    return render_template('admin.html', form=form, bracelets=bracelets)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
