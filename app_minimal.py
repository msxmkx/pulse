from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>PULSE - Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 PULSE Financial App - Test Deployment</h1>
            <p>If you can see this page, the deployment is working!</p>
            <p>✅ Flask is running</p>
            <p>✅ Gunicorn is working</p>
            <p>✅ Render deployment successful</p>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True) 