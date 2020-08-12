from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ahgarawani:6898@localhost:5432/todoapp'
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    
    def __repr__():
        return f'<Todo {self.id} {self.description}>'

db.create_all()


@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description': todo.description
    })

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

if __name__ == '__main__':
    app.run()