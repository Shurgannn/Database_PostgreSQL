import psycopg2

con = psycopg2.connect("dbname=netology_db user=netology_user password=1234") #password=1234
cur = con.cursor()

def create_db(): # создает таблицы
    cur.execute("""CREATE TABLE student(
    id serial PRIMARY KEY,
    name varchar(100),
    gpa numeric(10, 2),
    birth timestamp with time zone);
    """)
    con.commit()
    cur.execute("""CREATE TABLE course(
    id serial PRIMARY KEY,
    name varchar(100));
    """)
    con.commit()
    print('Tables created successfully')
    con.close()

def add_student(student): # просто создает студента
    name = student
    cur.execute("insert into student (name) values (%s)",
                (name, ))
    con.commit()
    print("Record inserted successfully")
    con.close()

def get_student(student_id):
    id_num = student_id
    cur.execute("select * from student")
    rows = cur.fetchall()
    for row in rows:
        if id_num == row[0]:
            print(row[1])
    else:
        print('Студента с таким номером нет')

def get_students(course_id): # возвращает студентов определенного курса
    pass

def add_students(course_id, students):  # создает студентов и
                                        # записывает их на курс
    pass

# create_db()
# add_student("Leonov")
# get_student(12)