import sqlite3

def create_connection(db_file):
    """Crea una conexión a la base de datos SQLite especificada."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Conexión exitosa a SQLite")
    except sqlite3.Error as e:
        print("Error al conectar:", e)
    return conn

def create_tables(conn):
    """Crea las tablas 'students', 'materias', 'universidades' y 'student_materia' si no existen."""
    try:
        # Tabla estudiantes
        sql_create_students_table = '''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        );
        '''
        
        # Tabla universidades
        sql_create_universities_table = '''
        CREATE TABLE IF NOT EXISTS universidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        );
        '''
        
        # Tabla materias
        sql_create_materias_table = '''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            universidad_id INTEGER,
            FOREIGN KEY (universidad_id) REFERENCES universidades (id)
        );
        '''
        
        # Tabla de relación estudiantes-materias
        sql_create_student_materia_table = '''
        CREATE TABLE IF NOT EXISTS student_materia (
            student_id INTEGER,
            materia_id INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (materia_id) REFERENCES materias (id)
        );
        '''

        c = conn.cursor()
        c.execute(sql_create_students_table)
        c.execute(sql_create_universities_table)
        c.execute(sql_create_materias_table)
        c.execute(sql_create_student_materia_table)
        print("Tablas creadas o verificadas exitosamente.")
    except sqlite3.Error as e:
        print("Error al crear las tablas:", e)

def insert_student(conn):
    """Inserta un nuevo estudiante en la tabla."""
    name = input("Ingresa el nombre del estudiante: ")
    age = int(input("Ingresa la edad del estudiante: "))
    sql = '''INSERT INTO students(name, age) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (name, age))
    conn.commit()
    print(f"Estudiante {name} insertado con éxito.")

def insert_university(conn):
    """Inserta una nueva universidad en la tabla."""
    nombre = input("Ingresa el nombre de la universidad: ")
    sql = '''INSERT INTO universidades(nombre) VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, (nombre,))
    conn.commit()
    print(f"Universidad {nombre} insertada con éxito.")

def insert_materia(conn):
    """Inserta una nueva materia en la tabla."""
    nombre = input("Ingresa el nombre de la materia: ")
    university_id = int(input("Ingresa el ID de la universidad que ofrece esta materia: "))
    sql = '''INSERT INTO materias(nombre, universidad_id) VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (nombre, university_id))
    conn.commit()
    print(f"Materia {nombre} insertada con éxito.")

def assign_materia_to_student(conn):
    """Asigna una materia a un estudiante."""
    student_id = int(input("Ingresa el ID del estudiante: "))
    materia_id = int(input("Ingresa el ID de la materia: "))
    sql = '''INSERT INTO student_materia(student_id, materia_id) VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (student_id, materia_id))
    conn.commit()
    print(f"Materia asignada al estudiante con ID {student_id}.")

def select_all_students(conn):
    """Consulta todos los registros de la tabla 'students'."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    if rows:
        print("Estudiantes en la base de datos:")
        for row in rows:
            print(row)
    else:
        print("No hay estudiantes en la base de datos.")

def select_all_universities(conn):
    """Consulta todas las universidades disponibles."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM universidades")
    rows = cur.fetchall()
    if rows:
        print("Universidades disponibles:")
        for row in rows:
            print(f"ID: {row[0]}, Nombre: {row[1]}")
    else:
        print("No hay universidades en la base de datos.")

def select_all_materias(conn):
    """Consulta todas las materias disponibles."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM materias")
    rows = cur.fetchall()
    if rows:
        print("Materias disponibles:")
        for row in rows:
            print(f"ID: {row[0]}, Nombre de la materia: {row[1]}")
    else:
        print("No hay materias en la base de datos.")

def select_students_by_materia(conn):
    """Consulta los estudiantes inscritos en una materia específica."""
    materia_id = int(input("Ingresa el ID de la materia: "))
    
    # Consulta para obtener los estudiantes inscritos en la materia
    sql = '''
    SELECT s.id, s.name
    FROM students s
    JOIN student_materia sm ON s.id = sm.student_id
    WHERE sm.materia_id = ?
    '''
    cur = conn.cursor()
    cur.execute(sql, (materia_id,))
    rows = cur.fetchall()
    
    if rows:
        print(f"Estudiantes inscritos en la materia con ID {materia_id}:")
        for row in rows:
            print(f"ID: {row[0]}, Nombre del estudiante: {row[1]}")
    else:
        print(f"No hay estudiantes inscritos en la materia con ID {materia_id}.")


def select_materias_by_university(conn):
    """Consulta las materias de una universidad específica."""
    university_id = int(input("Ingresa el ID de la universidad: "))
    
    sql = '''
    SELECT m.id, m.nombre
    FROM materias m
    WHERE m.universidad_id = ?
    '''
    cur = conn.cursor()
    cur.execute(sql, (university_id,))
    rows = cur.fetchall()
    
    if rows:
        print(f"Materias ofrecidas por la universidad con ID {university_id}:")
        for row in rows:
            print(f"ID: {row[0]}, Nombre de la materia: {row[1]}")
    else:
        print(f"No hay materias ofrecidas por la universidad con ID {university_id}.")

def enroll_in_external_materia(conn):
    """Permite a un estudiante inscribir una materia de otra universidad."""
    student_id = int(input("Ingresa el ID del estudiante: "))
    materia_id = int(input("Ingresa el ID de la materia de otra universidad: "))
    
    sql = '''INSERT INTO student_materia(student_id, materia_id) VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (student_id, materia_id))
    conn.commit()
    print(f"Estudiante con ID {student_id} inscrito en la materia con ID {materia_id}.")

def select_materias_by_student(conn):
    """Consulta las materias de un estudiante específico."""
    student_id = int(input("Ingresa el ID del estudiante: "))
    
    sql = '''
    SELECT m.id, m.nombre
    FROM materias m
    JOIN student_materia sm ON m.id = sm.materia_id
    WHERE sm.student_id = ?
    '''
    cur = conn.cursor()
    cur.execute(sql, (student_id,))
    rows = cur.fetchall()
    
    if rows:
        print(f"Materias inscritas para el estudiante con ID {student_id}:")
        for row in rows:
            print(f"ID: {row[0]}, Nombre de la materia: {row[1]}")
    else:
        print(f"El estudiante con ID {student_id} no tiene materias inscritas.")

def update_student(conn):
    """Actualiza los datos de un estudiante en la tabla."""
    student_id = int(input("Ingresa el ID del estudiante a actualizar: "))
    name = input("Ingresa el nuevo nombre del estudiante: ")
    age = int(input("Ingresa la nueva edad del estudiante: "))
    sql = '''UPDATE students SET name = ?, age = ? WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (name, age, student_id))
    conn.commit()
    print(f"Estudiante con ID {student_id} actualizado con éxito.")

def delete_student(conn):
    """Elimina un estudiante de la tabla según su ID."""
    student_id = int(input("Ingresa el ID del estudiante a eliminar: "))
    sql = '''DELETE FROM students WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (student_id,))
    conn.commit()
    print(f"Estudiante con ID {student_id} eliminado con éxito.")

def main():
    # Nombre de la base de datos (se creará en el directorio actual)
    database = "school.db"

    # Crear conexión a la base de datos
    conn = create_connection(database)
    if conn is not None:
        # Crear las tablas si no existen
        create_tables(conn)

        while True:
            print("\nElige una opción:")
            print("1. Insertar estudiante")
            print("2. Ver estudiantes")
            print("3. Actualizar estudiante")
            print("4. Eliminar estudiante")
            print("5. Insertar materia")
            print("6. Ver materias")
            print("7. Asignar materia a estudiante")
            print("8. Ver materias de un estudiante")
            print("9. Ver estudiantes inscritos en una materia")
            print("10. Insertar universidad")
            print("11. Ver universidades")
            print("12. Ver materias de otras universidades")
            print("13. Inscribir en materia de otra universidad")
            print("14. Salir")

            opcion = input("Opción: ")

            if opcion == '1':
                insert_student(conn)
            elif opcion == '2':
                select_all_students(conn)
            elif opcion == '3':
                update_student(conn)
            elif opcion == '4':
                delete_student(conn)
            elif opcion == '5':
                insert_materia(conn)
            elif opcion == '6':
                select_all_materias(conn)
            elif opcion == '7':
                assign_materia_to_student(conn)
            elif opcion == '8':
                select_materias_by_student(conn)
            elif opcion == '9':
                select_students_by_materia(conn)
            elif opcion == '10':
                insert_university(conn)
            elif opcion == '11':
                select_all_universities(conn)
            elif opcion == '12':
                select_materias_by_university(conn)
            elif opcion == '13':
                enroll_in_external_materia(conn)
            elif opcion == '14':
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")
        
        conn.close()
    else:
        print("Error! No se pudo crear la conexión a la base de datos.")

if __name__ == '__main__':
    main()
