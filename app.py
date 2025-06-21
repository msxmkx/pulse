from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>PULSE - Working!</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
            h1 { color: #333; }
            .success { color: green; font-size: 24px; }
        </style>
    </head>
    <body>
        <h1>🚀 PULSE Financial App</h1>
        <div class="success">✅ DEPLOYMENT SUCCESSFUL!</div>
        <p>Your website is now live and working!</p>
        <p>This confirms that Render deployment is working correctly.</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True) 