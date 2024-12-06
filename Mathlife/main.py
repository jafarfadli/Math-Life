from database_function import utility 
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = "1234321"

user_signedin = []

@app.route('/', methods = ['POST', 'GET'])
def index():
    global user_signedin 
    
    message = ""
    if request.method == 'POST':
        if 'signUp' in request.form:
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not utility.username_exists(username):
                utility.insert_user(username, password)
                
                user_signedin = utility.get_user(username)
                return redirect('homepage')
            else:
                message = "Username Sudah Ada!"
        
        elif 'signIn' in request.form:
            # Proses data untuk Sign In
            username = request.form.get('username')
            password = request.form.get('password')
            
            if utility.username_exists(username):
                user_signedin = utility.get_user(username)
                if user_signedin[2] == password:
                    return redirect('homepage')
                else:     # wrong pass 
                    message = "Password Salah"
            else:     # username not found 
                message = "Username Tidak Ditemukan"
    return render_template('index.html', message = message)

@app.route('/homepage', methods = ['POST', 'GET'])
def homepage():
    global user_signedin

    if request.method == 'POST':
        if 'mailBox' in request.form:
            # Proses data untuk kirim mail
            title = request.form.get('title')
            content = request.form.get('content')
            
            utility.insert_mail(user_signedin[1], title, content)
            
    if user_signedin[1] == 'kepsek':
        mail_messages = utility.get_mail_all()
    else:
        mail_messages = utility.get_mail(user_signedin[1])
        
    return render_template('homepage.html', coins = user_signedin[3], hintPotion = user_signedin[4], toolPotion = user_signedin[5], lifePotion = user_signedin[6], name = user_signedin[1], mail_messages = mail_messages)

@app.route('/principalroom', methods = ['POST', 'GET'])
def principalroom():
    global user_signedin
    
    if request.method == 'POST':
        if 'manageUser' in request.form:
            
            userUsername = request.form.get('userUsername')
            userCoins = request.form.get('userCoins')
            userHintPotion = request.form.get('userHintPotion')
            userToolPotion = request.form.get('userToolPotion')
            userLifePotion = request.form.get('userLifePotion')
            
        utility.update_user(userCoins, userHintPotion, userToolPotion, userLifePotion, userUsername)
        
    user_list = utility.get_user_all()
    
    return render_template('principalroom.html', name = user_signedin[1], user_list = user_list)

@app.route('/geometryclass', methods = ['POST', 'GET'])
def geometryclass():
    global user_signedin
    
    if request.method == 'POST':
        if 'insertGeo' in request.form:
            
            problemText = request.form.get('problemText')
            problemHint = request.form.get('problemHint')
            problemTool = request.form.get('problemTool')
            problemAnswer = request.form.get('problemAnswer')
            
            utility.insert_problem('geometry_problem',problemText,problemHint,problemTool,problemAnswer)
    return render_template('geometryclass.html', coins = user_signedin[3], hintPotion = user_signedin[4], toolPotion = user_signedin[5], lifePotion = user_signedin[6], name = user_signedin[1])

@app.route('/cafetaria', methods = ['POST', 'GET'])
def cafetaria():
    global user_signedin
        
    if request.method == 'POST':
        if 'shop' in request.form:
            # Proses data untuk shop
            coinsValue = request.form.get('newCoins')
            hintPotionValue = request.form.get('newHintPotion')
            toolPotionValue = request.form.get('newToolPotion')
            lifePotionValue = request.form.get('newLifePotion')
            
            user_signedin[3] = coinsValue
            user_signedin[4] = hintPotionValue
            user_signedin[5] = toolPotionValue
            user_signedin[6] = lifePotionValue
            
            hintPotionPrice = request.form.get('newHintPotionPrice')
            toolPotionPrice = request.form.get('newToolPotionPrice')
            lifePotionPrice = request.form.get('newLifePotionPrice')
            
            utility.update_user(user_signedin[3], user_signedin[4], user_signedin[5], user_signedin[6], user_signedin[1]) 
            utility.update_shop(hintPotionPrice, toolPotionPrice, lifePotionPrice)
            
    shop_price = utility.get_shop_price()
    
    return render_template('cafetaria.html', coins = user_signedin[3], hintPotion = user_signedin[4], toolPotion = user_signedin[5], lifePotion = user_signedin[6], name = user_signedin[1], shop_price = shop_price)

@app.route('/geometryquiz', methods = ['POST', 'GET'])
def geometryquiz():
    global user_signedin
    
    if request.method == 'POST':
        if 'finish' in request.form:
            # Proses data untuk finish
            coinsValue = request.form.get('newCoins')
            hintPotionValue = request.form.get('newHintPotion')
            toolPotionValue = request.form.get('newToolPotion')
            lifePotionValue = request.form.get('newLifePotion')
            
            user_signedin[3] = coinsValue
            user_signedin[4] = hintPotionValue
            user_signedin[5] = toolPotionValue
            user_signedin[6] = lifePotionValue
            
            utility.update_user(user_signedin[3], user_signedin[4], user_signedin[5], user_signedin[6], user_signedin[1]) 
            return render_template('geometryclass.html', coins = user_signedin[3], hintPotion = user_signedin[4], toolPotion = user_signedin[5], lifePotion = user_signedin[6], name = user_signedin[1])
    
    problem_id = utility.random_number(5,1,utility.length('geometry_problem'))
    problems = [utility.get_problem('geometry_problem',id) for id in problem_id]
    
    return render_template('geometryquiz.html', coins = user_signedin[3], hintPotion = user_signedin[4], toolPotion = user_signedin[5], lifePotion = user_signedin[6], name = user_signedin[1], problems = problems)

if __name__ == "__main__":
    app.run(debug=True,port=5000)