from slim import app, db
from flask import render_template, redirect, url_for, flash, request
from slim.models import Item, User
from slim.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    item = Item.query.all()
    return render_template("home.html")

@app.route("/aboutus")
def aboutus_page():
    return render_template("aboutus.html")

@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form=PurchaseItemForm()
    selling_form=SellItemForm()
    if request.method == "POST":
        print('post ' * 20)
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            p_item_object.owner = current_user.id
            db.session.commit()
            flash(f'Вы приобрели программу {p_item_object.name} за {p_item_object.price} руб!')
            print(p_item_object.owner)


        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            s_item_object.owner = None
            db.session.commit()
            flash(f'Вы вернули программу {s_item_object.name} за {s_item_object.price} руб. обратно в магазин')
        return redirect(url_for('market_page'))

    if request.method == "GET":
        print('*'*60)

        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items= items, owned_items=owned_items,
                               purchase_form=purchase_form, selling_form=selling_form)



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
