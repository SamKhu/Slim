from slim import app, db
from flask import render_template, redirect, url_for, flash
from slim.models import Item, User
from slim.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home_page():
    item = Item.query.all()
    return render_template("home.html")

@app.route("/aboutus")
def aboutus_page():
    return render_template("aboutus.html")

@app.route("/market")
@login_required
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
        login_user(user_to_create)
        flash(f"Регистрация прошла успешно! Вы вошли в систему под именем "
              f"{user_to_create.username}", category="success")

        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Произошла ошибка при создании учетной записи: {err_msg}', category='danger')

    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.user_name.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Вы успешно  авторизовались, как {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Неудачная авторизация', category='danger')

    return render_template("login.html", form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("Вы успешно вышли из аккаунта", category='info')
    return redirect(url_for('home_page'))
