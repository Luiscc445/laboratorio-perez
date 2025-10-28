from app import create_app, db
from app.models import Usuario

app = create_app()

@app.before_request
def init_db():
    with app.app_context():
        db.create_all()
        if not Usuario.query.filter_by(username='admin').first():
            admin = Usuario(username='admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuario admin creado")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Base de datos creada correctamente")
    app.run(debug=True, host='0.0.0.0', port=5000)
