# Turismo Extremo Sur

Aplicación web para la empresa de turismo "Turismo Extremo Sur", desarrollada con Flask, Bootstrap 5, MariaDB y PHPMyAdmin, implementada en una máquina virtual Ubuntu. Permite el registro de clientes, envío de quejas o sugerencias, y gestión de clientes y quejas por parte de administradores.

## Características

- Registro de clientes
- Envío de quejas y sugerencias
- Gestión de clientes y quejas
- Envío de respuestas por correo electrónico

## Requisitos

- Python 3.8+
- Flask
- Flask-WTF
- Flask-MySQLdb
- MySQL
- Bootstrap 5
- smtplib
- email.mime
- ProtonMail

## Instalación

1. **Clonar el repositorio**

    ```bash
    git clone https://github.com/BenjaminGajardoRo/Turismo_Extreme_WEB.git
    cd Turismo_Extreme_WEB
    ```

2. **Crear y activar un entorno virtual**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Crear el archivo `requirements.txt`**

    Crea un archivo llamado `requirements.txt` y añade las siguientes líneas:

    ```plaintext
    Flask==2.0.1
    Flask-WTF==0.15.1
    Flask-MySQLdb==0.2.0
    mysqlclient==2.0.3
    Werkzeug==2.0.1
    ```

4. **Instalar dependencias**

    ```bash
    pip install -r requirements.txt
    ```

5. **Configurar la base de datos**

    ```sql
    sudo mysql -u root -p
    CREATE DATABASE turismo_extremo_sur;
    CREATE USER 'turismo_user'@'localhost' IDENTIFIED BY 'admin';
    GRANT ALL PRIVILEGES ON turismo_extremo_sur.* TO 'turismo_user'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;
    ```

6. **Configurar tablas de la base de datos**

    ```sql
    USE turismo_extremo_sur;

    CREATE TABLE clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rut VARCHAR(12) NOT NULL,
        nombre_completo VARCHAR(255) NOT NULL,
        direccion VARCHAR(255) NOT NULL,
        telefono VARCHAR(15) NOT NULL,
        email VARCHAR(255) NOT NULL,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    CREATE TABLE quejas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        descripcion TEXT NOT NULL,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

7. **Añadir usuario administrador**

    Genera un hash para la contraseña:

    ```python
    from werkzeug.security import generate_password_hash

    hashed_password = generate_password_hash('admin', method='pbkdf2:sha256', salt_length=16)
    print(hashed_password)
    ```

    Usa el hash generado para crear un usuario administrador:

    ```sql
    INSERT INTO usuarios (email, password) VALUES ('admin@turismo.com', '<hashed_password>');
    ```

8. **Ejecutar la aplicación**

    ```bash
    flask run
    ```

## Uso

- Accede a la aplicación en [http://localhost:5000](http://localhost:5000)
- Inicia sesión como administrador con `admin@turismo.com` y `admin`
- Gestiona clientes y quejas desde el dashboard

## Licencia



Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

```plaintext
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
