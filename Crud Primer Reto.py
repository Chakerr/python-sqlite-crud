import mysql.connector

def create_connection():
    """Crea una conexión a la base de datos MySQL especificada."""
    try:
        conn = mysql.connector.connect(
            host="localhost",      # Ajusta según la configuración de tu servidor MySQL
            user="chaker",         # Tu usuario de MySQL
            password="M4rc!3l@g0", # Tu contraseña de MySQL
            database="midatabase",  # Nombre de la base de datos
            ssl_disabled=True
        )
        print("Conexión exitosa a MySQL")
        return conn
    except mysql.connector.Error as err:
        print("Error al conectar:", err)
        return None

def create_table(conn):
    """Crea la tabla 'students' si no existe en la base de datos."""
    try:
        sql_create_table = '''
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT
        );
        '''
        c = conn.cursor()
        c.execute(sql_create_table)
        print("Tabla 'students' creada o verificada exitosamente.")
    except mysql.connector.Error as err:
        print("Error al crear la tabla:", err)

def insert_student(conn):
    """Inserta un nuevo estudiante en la tabla."""
    name = input("Ingresa el nombre del estudiante: ")
    age = int(input("Ingresa la edad del estudiante: "))
    sql = '''INSERT INTO students (name, age) VALUES (%s, %s)'''
    cur = conn.cursor()
    cur.execute(sql, (name, age))
    conn.commit()
    print(f"Estudiante {name} insertado con éxito.")

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
        # Crear la tabla si no existe
        create_table(conn)

        while True:
            print("\nElige una opción:")
            print("1. Insertar estudiante")
            print("2. Ver estudiantes")
            print("3. Actualizar estudiante")
            print("4. Eliminar estudiante")
            print("5. Salir")

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
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida. Intenta de nuevo.")
        
        conn.close()
    else:
        print("Error! No se pudo crear la conexión a la base de datos.")

if __name__ == '__main__':
    main()
