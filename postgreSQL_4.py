import psycopg2
from datetime import datetime, timedelta

con = psycopg2.connect("dbname=netology_db user=netology_user password=1234")
cur = con.cursor()
now = datetime.now()
long_ago = now - timedelta(days=365 * 30)
student = {
    "name": "Ivanov",
    "gpa": 4,
    "birth": long_ago
}
students = \
    [{"name": "Sokolov",
      "gpa": 4.5,
      "birth": long_ago},
     {"name": "Dovlatov",
      "gpa": 3,
      "birth": long_ago}]


def create_db():  # создает таблицы
    cur.execute("""CREATE TABLE student(
    id serial PRIMARY KEY,
    name varchar(100),
    gpa numeric(10, 2),
    birth timestamp with time zone);
    """)
    cur.execute("""CREATE TABLE course(
    id serial PRIMARY KEY,
    name varchar(100));
    """)
    cur.execute("""CREATE TABLE student_course (
    id serial PRIMARY KEY,
    student_id INTEGER REFERENCES student(id),
    course_id INTEGER REFERENCES course(id));
    """)
    con.commit()
    print('Tables created successfully')


def add_student(student):  # просто создает студента
    name = student["name"]
    gpa = student["gpa"]
    birth = student["birth"]
    cur.execute("insert into student (name, gpa, birth) values (%s, %s, %s)",
                (name, gpa, birth))
    con.commit()
    print("Record inserted successfully")


def get_student(student_id):
    id_num = student_id
    cur.execute("select name from student where id = %s", (id_num, ))
    rows = cur.fetchall()
    if rows == list:
        print('Студента с таким номером нет')
    else:
        for row in rows:
                print(row[0])


def get_students(course_id):  # возвращает студентов определенного курса
    c_num = course_id
    cur.execute("""select s.name from student_course sc
    join student s on s.id = sc.student_id
    join course c on c.id = sc.course_id
    where c.id = %s
    """, (c_num, ))
    rows = cur.fetchall()
    for row in rows:
        print(row[0])


def add_students(course_id, students):  # создает студентов и записывает их на курс
    c_num = course_id
    for student in students:
        name = student["name"]
        gpa = student["gpa"]
        birth = student["birth"]
        cur.execute("insert into student (name, gpa, birth) values (%s, %s, %s)",
                    (name, gpa, birth))
        cur.execute("select id from student where name = %s", (name, ))
        rows = cur.fetchall()
        st_id = rows[0][0]
        cur.execute("""
            insert into student_course (student_id, course_id)
            values (%s, %s)
            """, (st_id, c_num))
    con.commit()


# create_db()
# add_student(student)
# get_student(13)
# add_students(2, students)
# get_students(1)
con.close()
