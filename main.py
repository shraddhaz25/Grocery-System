####################################################
#######  Flask Model
from ast import Str
import re
import random
import pandas as pd
from csv import writer
import MySQLdb.cursors
from flask_mysqldb import MySQL
from difflib import get_close_matches
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, render_template, request, redirect, url_for, session,flash,send_file

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'
# Enter your database connection details below
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'movie'

####################################################

# Intialize MySQL
# mysql = MySQL(app)
import sqlite3
import os
cwd = os.getcwd()
database_path = cwd+'\\db.db'
conn = sqlite3.connect(database_path,check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

###########################################################
## Reccomendation Cosine Model
from difflib import get_close_matches
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

global df,product_list,vector_count,counter_matrix,similarity_of_cosine,cols

df = None
product_list = None
product_category = None
vector_count = None
counter_matrix = None
similarity_of_cosine = None

cols = ['productName',	'subCategory','image_url',	'productid','size',	'finalPrice',	'comb',	'available']
def load_reco_model():
    print('Loding Reccomendation Model Please Wait >>>>>>>>>>>>>>')
    global df,product_list,vector_count,counter_matrix,similarity_of_cosine,product_category

    df = pd.read_csv(cwd+'/products.csv',encoding='latin1')
    product_list = list(df['productName'])
    product_category = list(df['subCategory'])
    # create count matrix from this new combined column
    vector_count = CountVectorizer()
    counter_matrix = vector_count.fit_transform(df['comb'])
    # now compute the cosine similarity
    similarity_of_cosine = cosine_similarity(counter_matrix)
    ###########################################################


load_reco_model()

def get_book_dict_by_tittle(bookTittle_list):
    return df[df['productName'].isin(bookTittle_list)][cols].to_dict('records')

###########################################################
## Sentimental Model
print('Loding Sentimental Model Please Wait >>>>>>>>>>>>>>')
import bz2
from tensorflow.keras.models import load_model
from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences

model = load_model('LSTMmodel.h5')
print("model loaded")

train_file = bz2.BZ2File('dataset.bz2')

train_file_lines = train_file.readlines()
train_file_lines = [x.decode('utf-8') for x in train_file_lines]
train_labels = [0 if x.split(' ')[0] == '__label__1' else 1 for x in train_file_lines]
train_sentences = [x.split(' ', 1)[1][:-1].lower() for x in train_file_lines]
for i in range(len(train_sentences)):
    train_sentences[i] = re.sub('\d', '0', train_sentences[i])

for i in range(len(train_sentences)):
    if 'www.' in train_sentences[i] or 'http:' in train_sentences[i] or 'https:' in train_sentences[i] or '.com' in \
            train_sentences[i]:
        train_sentences[i] = re.sub(r"([^ ]+(?<=\.[a-z]{3}))", "<url>", train_sentences[i])
X_train, X_test, y_train, y_test = train_test_split(train_sentences, train_labels, train_size=0.80, test_size=0.20,
                                                    random_state=42)
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(X_train)
print('Tokenizer Done')

def rate(p):
    return (p * 5)

########################################################

# this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
# Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database

        print(account)
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['password'] = account['password']
            session['email'] = account['email']

            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html',title="Login")




@app.route("/prediction", methods=['POST', 'GET'])
def prediction():

    review = request.form.get('review')
    username = request.form.get('username')
    original_title = request.form.get('book_tittle')
    book_id = request.form.get('book_id')
    sentiment = "Neutral"

    # assign the review text to a variable
    a = [review]

    # predict the outcome
    pred = model.predict(pad_sequences(tokenizer.texts_to_sequences(a), maxlen=100))
    value = rate(pred.item(0, 0))

    if value <=2:
        print('**** Result Review is Negative Review  *****')
        sentiment = "Negative"
    if value>2 and value<=3.5:
        print('**** Result Review is Neutral Review  *****')
        sentiment = "Neutral"
    if value>3.5:
        print('**** Result Review is Positive Review  *****')
        sentiment = "Positive"


    c = cursor

    query = "Insert into reviews (`username`,`review`,`book_id`,`sentiment`,`original_title`) Values (" \
            + "'" + username + "','" + "" + review + "','" +  "" + book_id + "','" + "" + sentiment + "','" + "" + original_title+ "');"

    c.execute(query)
    
    conn.commit()


    return redirect('/viewBook?tittle=' + original_title)



@app.route("/buy", methods=['POST', 'GET'])
def buy():
    book_id = request.args.get('book_id')
    username = request.args.get('username')
    print(book_id)
    print(username)
    bookDetails = get_book_dict_by_tittle([book_id])[0] 
    c = cursor
	
    query = "Insert into orders (`productName`,`subCategory`,`image_url`,`username`,`status`,`productid`,`size`,`finalPrice`) Values (" \
            + "'" + bookDetails['productName'] + "','" + "" + bookDetails['subCategory'] + "','" +  "" + str(bookDetails['image_url']) + "','" + "" + username + "','" + "" + 'Pending'+ "','"  + "" + str(bookDetails['productid']) + "','" + "" + str(bookDetails['size']) + "','"+ "" + str(bookDetails['finalPrice']) + "');"

    c.execute(query)
    
    conn.commit()

    return redirect('/profile')


# This will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobile = request.form['mobile']
                
        # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        cursor.execute( "SELECT * FROM accounts WHERE username LIKE '" +username+"'" )
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        elif not username or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute("INSERT INTO `accounts` ("
                   "username,email,password,mobile) "
                   "VALUES(?, ?, ?, ?)",
                   (username,email,password,mobile))

            conn.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash("Please fill out the form!", "danger")
    # Show registration form with message (if any)
    return render_template('auth/register.html',title="Register")



# This will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:

        print('random')

        # User is loggedin show them the home page

        book_title = product_list[random.randint(1,100)]

        print('book_title',book_title)


        # correcting user input spell (close match from our book list)
        correct_title = get_close_matches(book_title, product_list, n=3, cutoff=0.6)[0]

        # get the index value of given movie title
        idx = df['productName'][df['productName'] == correct_title].index[0]

        # get the pairwise similarity scores of all movies with that book
        similarity_score = list(enumerate(similarity_of_cosine[idx]))

        # sort the book based on similarity scores
        similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)[0:20]

        # suggested book are storing into a list
        recommendated_product_list = []
        for i in similarity_score:
            book_index_from_dataset = i[0]
            recommendated_product_list.append(df['productName'][book_index_from_dataset])


        all_recc_books = get_book_dict_by_tittle(recommendated_product_list)

        return render_template('home/home.html', session=session,  all_recc_books=all_recc_books, username=session['username'],title="Home",movies_title_list=product_list)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))    



@app.route('/home', methods=['POST', 'GET'])  # route to show the recommendation in web UI
def recommendation():
    
    if request.method == 'POST':
        try:

            print('searched')
            # reading the inputs given by the user
            book_title = request.form['search']

            # correcting user input spell (close match from our book list)
            try:
                correct_title = get_close_matches(book_title, product_list, n=3, cutoff=0.4)[0]
                # get the index value of given movie title
                idx = df['productName'][df['productName'] == correct_title].index[0]

            except Exception as e:
                print(e)
                correct_title = get_close_matches(book_title, product_category, n=3, cutoff=0.4)[0]
                # get the index value of given movie title
                idx = df['subCategory'][df['subCategory'] == correct_title].index[0]


            print(correct_title)


            # get the pairwise similarity scores of all movies with that book
            similarity_score = list(enumerate(similarity_of_cosine[idx]))

            # sort the book based on similarity scores
            similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)[0:20]

            # suggested book are storing into a list
            recommendated_product_list = []
            for i in similarity_score:
                book_index_from_dataset = i[0]
                recommendated_product_list.append(df['productName'][book_index_from_dataset])
            

            all_recc_books = get_book_dict_by_tittle(recommendated_product_list)
            all_recc_books.reverse()


            return render_template('auth/recommended.html', rec_books=all_recc_books,username=session['username'],title="Home")

        except Exception as e:
            print(e)
            return render_template("auth/error.html",username=session['username'], session=session)
            # return redirect('/home')


@app.route('/viewBook', methods=['POST', 'GET'])  # route to show the recommendation in web UI
def viewBook():
    bookTittle = request.args.get('tittle')
    bookDetails = get_book_dict_by_tittle([bookTittle])

    # Fetch the reviews and their corresponding ratings for a product
    cursor.execute("SELECT * FROM reviews where original_title='" + bookTittle + "' ORDER BY review_id DESC ")
    data = cursor.fetchall()
    print(data)
    print('bookDetails',bookDetails)

    return render_template('auth/viewBook.html',data=data, bookDetails=bookDetails[0],session=session)  


@app.route("/sellBook", methods=['POST', 'GET'])
def sellBook():
    if request.method == 'POST': 
        
        productName = request.form['productName']
        image_url = request.form['image_url']
        size = request.form['size']
        finalPrice = request.form['finalPrice']
        subCategory = request.form['subCategory']

        id = request.form['id']
        username = request.form['username']
        productid = random.randint(9000,200000)
        

        data =	[ productid,productName,subCategory,size,finalPrice,image_url,str(productName).lower()+str(subCategory).lower(),'yes']
        # Open our existing CSV file in append mode
        # Create a file object for this file
        with open(cwd+'/products.csv', 'a') as f_object:
        
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)
        
            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(data)
        
            #Close the file object
            f_object.close()

        load_reco_model()



    return render_template('auth/sellBook.html',data=None, bookDetails=None,session=session)
    # ,data=data, bookDetails=bookDetails[0],session=session)  
    # order_id = request.args.get('order_id')
    # username = request.args.get('username')


@app.route("/sell", methods=['POST', 'GET'])
def sell():
    order_id = request.args.get('order_id')
    username = request.args.get('username')

    c = cursor
    


    query =  "UPDATE orders SET status = 'Delivered' WHERE order_id = '"+str(order_id)+"';"
    c.execute(query)
    
    conn.commit()

    return redirect('/profile')


@app.route('/logout')
def logout():
    session.clear
    return redirect(url_for('login'))    



@app.route('/profile')
def profile():
    page = 'auth/profile.html'
    # Check if user is loggedin
    if 'loggedin' in session:
        
        if 'admin' in session['username']:
            cursor.execute( "SELECT * FROM orders WHERE status LIKE ?", ['Pending'] )
            page = 'auth/admin.html'
        else:
            cursor.execute( "SELECT * FROM orders WHERE username LIKE ?", [session['username']] )
       
        data = cursor.fetchall()


        return render_template(page,books=data,username=session['username'],account=session, session=session,title="Profile")
    # User is not loggedin redirect to login page

    return redirect(url_for('login'))  




if __name__ =='__main__':
	app.run(debug=False)
