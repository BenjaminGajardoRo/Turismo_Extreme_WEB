from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'turismo_user'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'turismo_extremo_sur'

mysql = MySQL(app)

app.secret_key = 'your_secret_key'

# Formularios
class RegistroForm(FlaskForm):
    rut = StringField('RUT', validators=[DataRequired()])
    nombre_completo = StringField('Nombre Completo', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class QuejaForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if request.method == 'POST' and form.validate_on_submit():
        rut = form.rut.data
        nombre_completo = form.nombre_completo.data
        direccion = form.direccion.data
        telefono = form.telefono.data
        email = form.email.data

        cursor = mysql.connection.cursor()
        try:
            cursor.execute('INSERT INTO clientes (rut, nombre_completo, direccion, telefono, email) VALUES (%s, %s, %s, %s, %s)', (rut, nombre_completo, direccion, telefono, email))
            mysql.connection.commit()
            return redirect(url_for('registro', status='success'))
        except Exception as e:
            print(f"Error al registrar: {e}")
            return redirect(url_for('registro', status='error'))

    return render_template('registro_cliente.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg = ''
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            return redirect(url_for('dashboard'))
        else:
            msg = 'Correo o contraseña incorrectos'
    return render_template('login_admin.html', form=form, msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        if request.method == 'POST':
            if 'delete' in request.form:
                cliente_id = request.form['delete']
                try:
                    cursor.execute('DELETE FROM clientes WHERE id = %s', (cliente_id,))
                    mysql.connection.commit()
                    return redirect(url_for('dashboard', status='eliminado'))
                except:
                    return redirect(url_for('dashboard', status='errorEliminar'))
            
            if 'filter' in request.form:
                fecha_inicio = request.form['fecha_inicio']
                fecha_fin = request.form['fecha_fin']
                query = 'SELECT * FROM clientes WHERE fecha_creacion BETWEEN %s AND %s'
                cursor.execute(query, (fecha_inicio, fecha_fin))
            else:
                cursor.execute('SELECT * FROM clientes')
        else:
            cursor.execute('SELECT * FROM clientes')
        
        clientes = cursor.fetchall()
        
        cursor.execute('SELECT * FROM quejas')
        quejas = cursor.fetchall()
        
        return render_template('dashboard_admin.html', clientes=clientes, quejas=quejas)
    return redirect(url_for('login'))

@app.route('/queja_sugerencia', methods=['GET', 'POST'])
def queja_sugerencia():
    form = QuejaForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        descripcion = form.descripcion.data
        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('INSERT INTO quejas (email, descripcion) VALUES (%s, %s)', (email, descripcion))
            mysql.connection.commit()
            return redirect(url_for('queja_sugerencia', status='success'))
        except Exception as e:
            print(f"Error al enviar queja: {e}")
            return redirect(url_for('queja_sugerencia', status='error'))
    return render_template('queja_sugerencia_cliente.html', form=form)

@app.route('/responder_queja', methods=['POST'])
def responder_queja():
    if 'loggedin' in session:
        queja_id = request.form['queja_id']
        email_cliente = request.form['email']
        mensaje_personalizado = request.form['mensaje']
        mensaje_final = f"{mensaje_personalizado}\n\nAtentamente,\nTurismo Extremo Sur\nContacto: turismoextremotest@proton.me\nTeléfono: +56 9 2344 4443"
        asunto = f"Reclamo o Sugerencia #{queja_id}"

        # Configurar el correo
        remitente = 'turismoextremotest@proton.me'
        password = 'turismo1234'
        
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = email_cliente
        msg['Subject'] = asunto
        msg.attach(MIMEText(mensaje_final, 'plain'))

        try:
            server = smtplib.SMTP('smtp.protonmail.com', 587)
            server.starttls()
            server.login(remitente, password)
            text = msg.as_string()
            server.sendmail(remitente, email_cliente, text)
            server.quit()
            return redirect(url_for('dashboard', status='respuestaEnviada'))
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return redirect(url_for('dashboard', status='errorRespuesta'))

    return redirect(url_for('login'))

@app.route('/eliminar_queja', methods=['POST'])
def eliminar_queja():
    if 'loggedin' in session:
        queja_id = request.form['delete_queja']
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('DELETE FROM quejas WHERE id = %s', (queja_id,))
            mysql.connection.commit()
            return redirect(url_for('dashboard', status='quejaEliminada'))
        except Exception as e:
            print(f"Error al eliminar queja: {e}")
            return redirect(url_for('dashboard', status='errorQueja'))

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)