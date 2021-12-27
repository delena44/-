from flask import Flask, render_template, request, url_for, flash
from flask_login.utils import logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
import bd
import pyshorteners
import pyperclip
bd.connect()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hgee32thf1hr1th77h42k5fl3jr'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизируйтесь для доступа к данной странице'

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, bd)

menu = [
{'name': 'Регистрация', 'url': 'register'},
{'name': 'Авторизация', 'url': 'login'},
{'name': 'Мои ссылки', 'url': 'office'},
{'name': 'Priv ссылки', 'url': 'Priv'},]

@app.route('/l', methods=['POST', 'GET']) 
def index(): 
    print(url_for('index'))
    links = bd.getLinkPublic()
    if request.method == 'POST':
        url = request.form.get('link')
        link = pyshorteners.Shortener().tinyurl.short(url)
        pyperclip.copy(link)
        flash(f'Ваша новая ссылка: {link}')
    return render_template('index.html', links = links,  menu = menu) 


@app.route('/register', methods=['POST', 'GET']) 
def register(): 
    print(url_for('register'))
    if request.method == 'POST': 
        if len(request.form['password']) >= 4 and len(request.form['login'])>0:
            login = request.form['login'] 
            password = request.form['password'] 
            hash = generate_password_hash(password)
            reg = bd.login(login)
            if reg == 1:
                flash("Такой логин уже есть!")
            elif reg == 0:
                bd.register(login, hash)
                flash("Вы зарегистрировались!")
                return redirect(url_for('login'))
        else:
            flash('Неверное заполнение полей! (Пароль>3 и Логин>0)')

    return render_template('register.html', title='Регистрация', menu = menu) 

@app.route('/login', methods=['POST', 'GET']) 
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('office'))

    print(url_for('login'))
    if request.method == 'POST': 
        user = bd.getUser(request.form['login']) 
        if user and check_password_hash(user[2], request.form['password']):
            userLogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userLogin, remember=rm)
            return redirect(request.args.get('next') or url_for('office'))
            
        flash('Неверный пароль или логин')
     
    return render_template('login.html', title='Авторизация', menu = menu) 


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта')
    return redirect(url_for('login'))

@app.route('/office',  methods=['POST', 'GET']) 
@login_required
def office(): 
    try:
        user = bd.getUser(current_user.get_id())
        login = user[1]
        status = request.form.get('status')
        psevdonim = request.form.get('psevdonim')
        url = request.form.get('link')
        link = pyshorteners.Shortener().tinyurl.short(url)
        pyperclip.copy(link)
        bd.short(user[0], psevdonim, link, status)
        flash(f'Ваша новая ссылка: {link}')
    except:
         flash('Неверная ссылка')

    links = bd.getLinkPrivate(user[0])
    return render_template('office.html', title='Личный кабинет', login = login, links = links, menu = menu) 


@app.route('/office/<int:id>/delete') 
def delete(id):
    user = bd.getUser(current_user.get_id())
    try:
        bd.deleteLink(user[0], id)
        flash('Ссылка удалена')
        return redirect('/office')
    except:
        flash('При удалении произошла ошибка')


@app.route('/office/<int:id>/update',  methods=['POST', 'GET']) 
def update(id):
    link = bd.getLink(id)
    if request.method == "POST":
        status = request.form.get('status')
        psevdonim = request.form.get('psevdonim')
        try:
            bd.updateLink(psevdonim, status, id)
            flash('Изменение прошло успешно')
            return redirect('/office')
        except:
            flash('При изменении произошла ошибка')
    else:
        return render_template('update.html', title='Редактирование', link = link) 


@app.route('/priv') 
@login_required
def vip(): 
    linksOB = bd.getLinkOBD()
    return render_template('priv.html', title='Ссылки общего доступа', linksOB = linksOB, menu = menu) 


if __name__ == "__main__": 
    app.run()