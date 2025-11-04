from app import create_app, db
# Ya no necesitamos importar 'Usuario' aquí
# from app.models import Usuario 

app = create_app()

# HEMOS ELIMINADO TODA LA FUNCIÓN @app.before_request
# que creaba el usuario 'admin'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Base de datos creada correctamente")
    app.run(debug=True, host='0.0.0.0', port=5000)