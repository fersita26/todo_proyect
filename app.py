from flask import Flask, render_template, redirect, url_for, request, session
from models import db, User, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)  # Inicializar db con la app

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('todo_list'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not User.query.filter_by(username=username).first():
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/todo', methods=['GET', 'POST'])
def todo_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()
    if request.method == 'POST':
        new_task = Task(content=request.form['task'], user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
    return render_template('todo_list.html', tasks=tasks)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('todo_list'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect(url_for('todo_list'))

    if request.method == 'POST':
        task.content = request.form['task_content']
        db.session.commit()
        return redirect(url_for('todo_list'))

    return render_template('edit_task.html', task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear tablas si no existen
    app.run(debug=True)
