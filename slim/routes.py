from slim import app, db
from flask import render_template, redirect, url_for, flash
from slim.models import Item, User
from slim.forms import RegisterForm

@app.route("/")
@app.route("/home")
def home_page():
    item = Item.query.all()
    return render_template("home.html")

@app.route("/aboutus")
def aboutus_page():
    return render_template("aboutus.html")

@app.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.user_name.data,
                              email=form.email.data,
                              password=form.password_1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Произошла ошибка при создании учетной записи: {err_msg}', category='danger')

    return render_template("register.html", form=form)