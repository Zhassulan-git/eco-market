from app import app
@app.route('/')
def index():
    return 'Hello, Flask!' 

@app.route('/basket')
def basket():
    return '<h1>Basket is empty</h1>'