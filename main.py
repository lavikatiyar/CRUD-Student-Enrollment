from flask import Flask, request, render_template, redirect
from db_model import db, StudentModel

app = Flask(__name__, template_folder="templates")

# database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_track_modifications'] = False
db.init_app(app)

# create table

# flask has depreciated @app.before_first_request
#@app.before_first_request
#def create_table():
#  db.create_all()

with app.app_context():
  db.create_all()


@app.route('/create', methods=["GET", "POST"])
def create():
  if request.method == "GET":
    return render_template("create.html")

  if request.method == 'POST':
    #print("post")
    course = request.form.getlist("course_name")
    course_list = ', '.join(map(str, course))
    first_name = request.form.get('first_name')
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    country = request.form['country']
    gender = request.form['gender']
    #print(course_list)
    students = StudentModel(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            password=password,
                            gender=gender,
                            course_name=course_list,
                            country=country)
    db.session.add(students)
    db.session.commit()
    return redirect('/')


@app.route('/', methods=['GET'])
def retrieveStudents():
  students_list = StudentModel.query.all()
  #print("Retrieve")
  #print(students_list)
  return render_template("index.html", students_list=students_list)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
  student = StudentModel.query.filter_by(id=id).first()
  if request.method == 'POST':
    if student:
      db.session.delete(student)
      db.session.commit()
      return redirect('/')
    abort(404)
  return render_template('delete.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  student = StudentModel.query.filter_by(id=id).first()
  db.session.delete(student)
  db.session.commit()
  if request.method == 'POST':
    if student:
      course = request.form.getlist("course_name")
      course_list = ', '.join(map(str, course))
      first_name = request.form.get('first_name')
      last_name = request.form['last_name']
      email = request.form['email']
      password = request.form['password']
      country = request.form['country']
      gender = request.form['gender']

      students = StudentModel(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            password=password,
                            gender=gender,
                            course_name=course_list,
                            country=country)
      db.session.update(students)
      db.session.commit()
      return redirect('/')

    return f'Sorry! Student "{first_name + last_name}" with id "{id}" does not exist.'
    
  return render_template('edit.html', student = student)
  

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
