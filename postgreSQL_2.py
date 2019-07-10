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


def create_db(): # создает таблицы
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

def add_student(student): # просто создает студента
    name = student
    cur.execute("insert into student (name, birth) values (%s, %s)",
                (name, long_ago))
    con.commit()
    print("Record inserted successfully")

def get_student(student_id):
    id_num = student_id
    cur.execute("select * from student")
    rows = cur.fetchall()
    for row in rows:
        if id_num == row[0]:
            print(row[1])
            break
    else:
        print('Студента с таким номером нет')

def get_students(course_id): # возвращает студентов определенного курса
    c_num = course_id
    cur.execute("select * from course")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == c_num:
            print(row)
            cur.execute("""select s.id, s.name, c.name from student_cource sc
            join student s on s.id = sc.student_id
            join cource c on c.id = sc.cource_id
            """)
            print(cur.fetchall)
            cur.execute("select * from student")
            nws = cur.fetchall()
            print(nws)
        # if id_num == row[0]:
        #     print(row[1])

def add_students(): #course_id, students):  # создает студентов и
                                        # записывает их на курс
    key = ''
    value = ''
    for k, v in students.items():
        print(k)
        key += k + ', '
        value += str(v) + ', '
    value = value.rstrip(', ').split(',')
    key = key.rstrip(',')
    print(key, value)
    cur.execute("insert into student (key) values (%s)",
                (value[0], int(value[1]), value[2]))
    con.commit()
    #cur.execute("""
        # insert into student_course (student_id, course_id)
        # values (%s, %s)
        # """, (1, 0))

# create_db()
# add_student("Ivannova")
get_student(5)
# add_students()
# get_students(1)
con.close()