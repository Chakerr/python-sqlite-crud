import mysql.connector

def create_connection():
    """Crea una conexión a la base de datos MySQL especificada."""
    try:
        conn = mysql.connector.connect(
            host="localhost",      # Ajusta según la configuración de tu servidor MySQL
            user="chaker",         # Tu usuario de MySQL
            password="Qwerty123", # Tu contraseña de MySQL
            database="midatabase",  # Nombre de la base de datos
            ssl_disabled=True
        )
        print("Conexión exitosa a MySQL")
        return conn
    except mysql.connector.Error as err:
        print("Error al conectar:", err)
        return None

def create_tables(conn):
    """Crea las tablas 'students', 'materias' y 'student_materia' si no existen."""
    try:
        # Tabla estudiantes
        sql_create_students_table = '''
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT
        );
        '''
        
        # Tabla materias
        sql_create_materias_table = '''
        CREATE TABLE IF NOT EXISTS materias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        );
        '''
        
        # Tabla de relación estudiantes-materias
        sql_create_student_materia_table = '''
        CREATE TABLE IF NOT EXISTS student_materia (
            student_id INT,
            materia_id INT,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (materia_id) REFERENCES materias (id)
        );
        '''

        c = conn.cursor()
        c.execute(sql_create_students_table)
        c.execute(sql_create_materias_table)
        c.execute(sql_create_student_materia_table)
        print("Tablas creadas o verificadas exitosamente.")
    except mysql.connector.Error as err:
        print("Error al crear las tablas:", err)

def insert_student(conn):
    """Inserta un nuevo estudiante en la tabla."""
    name = input("Ingresa el nombre del estudiante: ")
    age = int(input("Ingresa la edad del estudiante: "))
    sql = '''INSERT INTO students(name, age) VALUES(%s, %s)'''
    cur = conn.cursor()
    cur.execute(sql, (name, age))
    conn.commit()
    print(f"Estudiante {name} insertado con éxito.")

def insert_materia(conn):
    """Inserta una nueva materia en la tabla."""
    nombre = input("Ingresa el nombre de la materia: ")
    sql = '''INSERT INTO materias(nombre) VALUES(%s)'''
    cur = conn.cursor()
    cur.execute(sql, (nombre,))
    conn.commit()
    print(f"Materia {nombre} insertada con éxito.")

def assign_materia_to_student(conn):
    """Asigna una materia a un estudiante."""
    student_id = int(input("Ingresa el ID del estudiante: "))
    materia_id = int(input("Ingresa el ID de la materia: "))
    sql = '''INSERT INTO student_materia(student_id, materia_id) VALUES(%s, %s)'''
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

def select_all_materias(conn):
    """Consulta todas las materias disponibles."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM materias")
    rows = cur.fetchall()
    if rows:
        print("Materias disponibles:")
        for row in rows:
            print(row)
    else:
        print("No hay materias en la base de datos.")

def select_materias_by_student(conn):
    """Consulta las materias de un estudiante específico."""
    student_id = int(input("Ingresa el ID del estudiante: "))
    
    # Consulta para obtener las materias del estudiante
    sql = '''
    SELECT m.id, m.nombre
    FROM materias m
    JOIN student_materia sm ON m.id = sm.materia_id
    WHERE sm.student_id = %s
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

def select_students_by_materia(conn):
    """Consulta los estudiantes inscritos en una materia específica."""
    materia_id = int(input("Ingresa el ID de la materia: "))
    
    # Consulta para obtener los estudiantes inscritos en la materia
    sql = '''
    SELECT s.id, s.name
    FROM students s
    JOIN student_materia sm ON s.id = sm.student_id
    WHERE sm.materia_id = %s
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

def update_student(conn):
    """Actualiza los datos de un estudiante en la tabla."""
    student_id = int(input("Ingresa el ID del estudiante a actualizar: "))
    name = input("Ingresa el nuevo nombre del estudiante: ")
    age = int(input("Ingresa la nueva edad del estudiante: "))
    sql = '''UPDATE students SET name = %s, age = %s WHERE id = %s'''
    cur = conn.cursor()
    cur.execute(sql, (name, age, student_id))
    conn.commit()
    print(f"Estudiante con ID {student_id} actualizado con éxito.")

def delete_student(conn):
    """Elimina un estudiante de la tabla según su ID."""
    student_id = int(input("Ingresa el ID del estudiante a eliminar: "))
    sql = '''DELETE FROM students WHERE id = %s'''
    cur = conn.cursor()
    cur.execute(sql, (student_id,))
    conn.commit()
    print(f"Estudiante con ID {student_id} eliminado con éxito.")

def main():
    # Crear conexión a la base de datos MySQL
    conn = create_connection()
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
            print("10. Salir")

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
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")
        
        conn.close()
    else:
        print("Error! No se pudo crear la conexión a la base de datos.")

if __name__ == '__main__':
    main()
