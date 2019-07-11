import psycopg2
from datetime import datetime, timedelta

con = psycopg2.connect("dbname=netology_db user=netology_user password=1234")
cur = con.cursor()
now = datetime.now()
long_ago = now - timedelta(days=365 * 30)
students = {
    "name": "Ivanov",
    "gpa": 4,
    "birth": long_ago
}


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
    name = student
    cur.execute("insert into student (name, birth) values (%s, %s)",
                (name, long_ago))
    con.commit()
    print("Record inserted successfully")


def get_student(student_id):
    id_num = student_id
    cur.execute("select name from student where id = %s", (id_num, ))
    rows = cur.fetchall()
    if rows == []:
        print('Студента с таким номером нет')
    else:
        for row in rows:
                print(row[0])


def get_students(course_id):  # возвращает студентов определенного курса
    c_num = course_id
    cur.execute("""
    insert into student_course (student_id, course_id)
    values (%s, %s)
    """, (6, c_num))
    cur.execute("""select s.name from student_course sc
    join student s on s.id = sc.student_id
    join course c on c.id = sc.course_id
    """)
    rows = cur.fetchall()
    for row in rows:
        print(row[0])


def add_students(course_id, student):  # создает студентов и записывает их на курс
    name = student
    c_num = course_id
    cur.execute("insert into student (name) values (%s)",
                (name, ))
    cur.execute("select id from student where name = %s", (name, ))
    rows = cur.fetchall()
    st_id = rows[0][0]
    cur.execute("""
        insert into student_course (student_id, course_id)
        values (%s, %s)
        """, (st_id, c_num))
    con.commit()


# create_db()
# add_student("Solovik")
# get_student(5)
add_students(1, 'Alekseev')
get_students(1)
con.close()
