from app import create_app

# Gunicorn sẽ nhìn vào biến app này để chạy
app = create_app()

if __name__ == '__main__':

    app.run(debug=False)