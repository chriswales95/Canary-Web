from app import create_app


app = create_app()
app.secret_key = b'change_me!'

if __name__ == "__main__":
    app.run()