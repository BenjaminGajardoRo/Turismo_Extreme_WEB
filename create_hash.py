from werkzeug.security import generate_password_hash

# Genera el hash de la contraseña
hashed_password = generate_password_hash('admin', method='pbkdf2:sha256')
print(hashed_password)
