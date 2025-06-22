from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/oneplus')
def oneplus():
    return render_template('oneplus.html')

@app.route('/apple')
def apple():
    return render_template('apple.html')

@app.route('/xiaomi')
def xiaomi():
    return render_template('redmi.html')

@app.route('/vivo')
def vivo():
    return render_template('vivo.html')

@app.route('/huawei')
def huawei():
    return render_template('huawei.html')

if __name__ == '__main__':
    app.run(debug=True)
