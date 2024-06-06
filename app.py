from flask import Flask, render_template, request
from app import create_app


# Configure application
app = create_app()
app.secret_key = '23021999'


if __name__ == '__main__':
    app.run(debug=True)
