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

def create_table(conn):
    """Crea la tabla 'students' si no existe."""
    try:
        sql_create_table = '''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        );
        '''
        c = conn.cursor()
        c.execute(sql_create_table)
        print("Tabla 'students' creada o verificada exitosamente.")
    except sqlite3.Error as e:
        print("Error al crear la tabla:", e)

def insert_student(conn, student):
    """Inserta un nuevo estudiante en la tabla."""
    sql = '''INSERT INTO students(name, age) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()
    return cur.lastrowid

def select_all_students(conn):
    """Consulta todos los registros de la tabla 'students'."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def update_student(conn, student):
    """Actualiza los datos de un estudiante en la tabla."""
    sql = '''UPDATE students SET name = ?, age = ? WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()

def delete_student(conn, student_id):
    """Elimina un estudiante de la tabla según su ID."""
    sql = '''DELETE FROM students WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (student_id,))
    conn.commit()

def main():
    # Nombre de la base de datos (se creará en el directorio actual)
    database = "school.db"

    # Crear conexión a la base de datos
    conn = create_connection(database)
    if conn is not None:
        # Crear la tabla si no existe
        create_table(conn)

        # 1. Crear: Insertar un estudiante
        student_id = insert_student(conn, ("Juan Pérez", 21))
        print(f"Estudiante insertado con id {student_id}\n")

        # 2. Leer: Mostrar todos los estudiantes
        print("Estudiantes después de la inserción:")
        select_all_students(conn)
        print()

        # 3. Actualizar: Modificar el estudiante insertado
        update_student(conn, ("Juan Carlos Pérez", 22, student_id))
        print("Estudiantes después de la actualización:")
        select_all_students(conn)
        print()

        # 4. Borrar: Eliminar el estudiante
        delete_student(conn, student_id)
        print("Estudiantes después de la eliminación:")
        select_all_students(conn)

        conn.close()
    else:
        print("Error! No se pudo crear la conexión a la base de datos.")

if __name__ == '__main__':
    main()
