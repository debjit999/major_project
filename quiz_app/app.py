from flask import Flask, render_template, request, redirect, url_for, session, flash
import mariadb
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_simple_college_project_secret_key_123'

# Database configuration
db_config = {
    'host': '127.0.0.1',
    'port': 50011,
    'user': 'root',
    'password': 'nothing123',
    'database': 'quiz_app_db'
}

# Quiz questions data structure
quiz_data = {
    1: {
        'id': 1,
        'title': 'Python Quiz',
        'description': 'Test your Python programming knowledge',
        'questions': [
            {
                'id': 1,
                'question': 'What is the output of print(type([]) is list) in Python?',
                'options': ['True', 'False', 'Error', 'None'],
                'answer': 'True'
            },
            {
                'id': 2,
                'question': 'Which of these is not a core data type in Python?',
                'options': ['Dictionary', 'Tuple', 'Class', 'List'],
                'answer': 'Class'
            },
            {
                'id': 3,
                'question': 'What does PEP 8 refer to?',
                'options': [
                    'Python Enhancement Proposal for coding standards',
                    'Python Extension Package',
                    'Python Execution Protocol',
                    'Python Error Prevention'
                ],
                'answer': 'Python Enhancement Proposal for coding standards'
            },
            {
                'id': 4,
                'question': 'Which keyword is used for function definition in Python?',
                'options': ['def', 'function', 'define', 'func'],
                'answer': 'def'
            },
            {
                'id': 5,
                'question': 'What is the purpose of __init__ in Python classes?',
                'options': [
                    'To initialize the class attributes',
                    'To create a new instance',
                    'To import modules',
                    'To terminate the class'
                ],
                'answer': 'To initialize the class attributes'
            },
            {
                'id': 6,
                'question': 'Which of these is used to handle exceptions in Python?',
                'options': ['try-except', 'do-catch', 'try-catch', 'handle-except'],
                'answer': 'try-except'
            },
            {
                'id': 7,
                'question': 'Which operator is used for floor division in Python?',
                'options': ['/', '//', '%', '**'],
                'answer': '//'
            },
            {
                'id': 8,
                'question': 'What is the output of: print(2 ** 3)?',
                'options': ['6', '8', '9', '5'],
                'answer': '8'
            },
            {
                'id': 9,
                'question': 'How do you start a comment in Python?',
                'options': ['//', '/*', '#', '--'],
                'answer': '#'
            },
            {
                'id': 10,
                'question': 'Which function converts a string to an integer in Python?',
                'options': ['int()', 'str()', 'float()', 'char()'],
                'answer': 'int()'
            }
        ]
    },
    2: {
        'id': 2,
        'title': 'Java Quiz',
        'description': 'Test your Java programming knowledge',
        'questions': [
            {
                'id': 1,
                'question': 'Which of these is not a Java keyword?',
                'options': ['const', 'goto', 'instanceof', 'unsigned'],
                'answer': 'unsigned'
            },
            {
                'id': 2,
                'question': 'What is the default value of a local variable in Java?',
                'options': [
                    'null',
                    '0',
                    'Depends on data type',
                    'Local variables have no default value'
                ],
                'answer': 'Local variables have no default value'
            },
            {
                'id': 3,
                'question': 'Which collection cannot contain duplicate elements?',
                'options': ['List', 'Set', 'Map', 'Array'],
                'answer': 'Set'
            },
            {
                'id': 4,
                'question': 'What is the size of int data type in Java?',
                'options': ['16-bit', '32-bit', '64-bit', 'Depends on system architecture'],
                'answer': '32-bit'
            },
            {
                'id': 5,
                'question': 'Which is the parent class of all classes in Java?',
                'options': ['Object', 'Class', 'Main', 'Super'],
                'answer': 'Object'
            },
            {
                'id': 6,
                'question': 'Which keyword is used to inherit a class in Java?',
                'options': ['extends', 'implements', 'inherits', 'super'],
                'answer': 'extends'
            },
            {
                'id': 7,
                'question': 'Which of these is not an access modifier in Java?',
                'options': ['public', 'protected', 'private', 'friendly'],
                'answer': 'friendly'
            },
            {
                'id': 8,
                'question': 'Which operator is used to compare two values in Java?',
                'options': ['=', '==', '!=', '<>'],
                'answer': '=='
            },
            {
                'id': 9,
                'question': 'Which package contains the Scanner class?',
                'options': ['java.util', 'java.io', 'java.lang', 'java.net'],
                'answer': 'java.util'
            },
            {
                'id': 10,
                'question': 'Which method is called when an object is created?',
                'options': ['constructor', 'finalize', 'main', 'start'],
                'answer': 'constructor'
            }
        ]
    },
    3: {
        'id': 3,
        'title': 'Networking Quiz',
        'description': 'Test your Computer Networking knowledge',
        'questions': [
            {
                'id': 1,
                'question': 'What does HTTP stand for?',
                'options': [
                    'HyperText Transfer Protocol',
                    'High Transfer Text Protocol',
                    'Hyper Transfer Text Protocol',
                    'HyperText Transmission Protocol'
                ],
                'answer': 'HyperText Transfer Protocol'
            },
            {
                'id': 2,
                'question': 'Which port does HTTPS typically use?',
                'options': ['80', '22', '443', '8080'],
                'answer': '443'
            },
            {
                'id': 3,
                'question': 'What is the purpose of DNS?',
                'options': [
                    'To translate domain names to IP addresses',
                    'To secure network connections',
                    'To manage email servers',
                    'To create web pages'
                ],
                'answer': 'To translate domain names to IP addresses'
            },
            {
                'id': 4,
                'question': 'Which protocol is used for sending email?',
                'options': ['SMTP', 'POP3', 'IMAP', 'FTP'],
                'answer': 'SMTP'
            },
            {
                'id': 5,
                'question': 'What does LAN stand for?',
                'options': [
                    'Local Area Network',
                    'Large Area Network',
                    'Linked Area Network',
                    'Logical Area Network'
                ],
                'answer': 'Local Area Network'
            },
            {
                'id': 6,
                'question': 'Which device connects different networks together?',
                'options': ['Switch', 'Router', 'Hub', 'Repeater'],
                'answer': 'Router'
            },
            {
                'id': 7,
                'question': 'Which layer of the OSI model handles routing?',
                'options': ['Data Link', 'Network', 'Transport', 'Session'],
                'answer': 'Network'
            },
            {
                'id': 8,
                'question': 'What does IP stand for?',
                'options': [
                    'Internet Protocol',
                    'Internal Process',
                    'Internet Packet',
                    'Interconnected Path'
                ],
                'answer': 'Internet Protocol'
            },
            {
                'id': 9,
                'question': 'Which protocol is used to retrieve emails from a server?',
                'options': ['POP3', 'SMTP', 'FTP', 'HTTP'],
                'answer': 'POP3'
            },
            {
                'id': 10,
                'question': 'Which cable type is used for most Ethernet networks?',
                'options': ['Coaxial', 'Fiber optic', 'Twisted pair', 'Serial'],
                'answer': 'Twisted pair'
            }
        ]
    }
}


def get_db_connection():
    try:
        conn = mariadb.connect(**db_config)
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            # Create users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create quiz_results table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    quiz_id INT NOT NULL,
                    score INT NOT NULL,
                    total_questions INT NOT NULL,
                    percentage FLOAT NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            conn.commit()
        except mariadb.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html', 
                           username=session['username'],
                           quizzes=quiz_data)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", 
                          (username, password))
                user = cur.fetchone()
                
                if user:
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    flash('Login successful!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password', 'error')
            except mariadb.Error as e:
                print(f"Error during login: {e}")
                flash('Database error occurred', 'error')
            finally:
                conn.close()
        else:
            flash('Database connection error', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if len(username) < 4 or len(password) < 6:
            flash('Username must be at least 4 characters and password at least 6 characters', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                          (username, password))
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except mariadb.Error as e:
                print(f"Error during registration: {e}")
                flash('Username already exists', 'error')
            finally:
                conn.close()
        else:
            flash('Database connection error', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if quiz_id not in quiz_data:
        flash('Quiz not found', 'error')
        return redirect(url_for('index'))
    
    quiz = quiz_data[quiz_id]
    
    if request.method == 'POST':
        score = 0
        for question in quiz['questions']:
            user_answer = request.form.get(f'question_{question["id"]}')
            if user_answer == question['answer']:
                score += 1
        
        percentage = (score / len(quiz['questions'])) * 100
        
        # Save score to database
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO quiz_results 
                    (user_id, quiz_id, score, total_questions, percentage) 
                    VALUES (?, ?, ?, ?, ?)
                """, (session['user_id'], quiz_id, score, len(quiz['questions']), percentage))
                conn.commit()
            except mariadb.Error as e:
                print(f"Error saving quiz results: {e}")
            finally:
                conn.close()
        
        return redirect(url_for('results', quiz_id=quiz_id, score=score))
    
    return render_template('quiz.html', quiz=quiz)

@app.route('/results')
def results():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    quiz_id = int(request.args.get('quiz_id', 0))
    score = int(request.args.get('score', 0))
    
    if quiz_id not in quiz_data:
        flash('Invalid quiz', 'error')
        return redirect(url_for('index'))
    
    quiz = quiz_data[quiz_id]
    total = len(quiz['questions'])
    percentage = (score / total) * 100
    
    return render_template('results.html', 
                         quiz_title=quiz['title'],
                         score=score, 
                         total=total,
                         percentage=percentage)

@app.route('/leaderboard')
def leaderboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            # Get leaderboard data
            cur.execute("""
                SELECT 
                    u.username, 
                    qr.quiz_id, 
                    qr.score, 
                    qr.total_questions,
                    qr.percentage,
                    qr.completed_at
                FROM quiz_results qr
                JOIN users u ON qr.user_id = u.id
                ORDER BY qr.percentage DESC, qr.completed_at DESC
                LIMIT 20
            """)
            leaderboard_data = cur.fetchall()
            
            # Get user's best scores
            cur.execute("""
                SELECT 
                    quiz_id, 
                    MAX(percentage) as best_percentage,
                    MAX(score) as best_score
                FROM quiz_results
                WHERE user_id = ?
                GROUP BY quiz_id
            """, (session['user_id'],))
            user_best_scores = {row[0]: {'percentage': row[1], 'score': row[2]} for row in cur.fetchall()}
            
            return render_template('leaderboard.html',
                               leaderboard_data=leaderboard_data,
                               user_best_scores=user_best_scores,
                               quiz_data=quiz_data,
                               current_user=session['username'])
        except mariadb.Error as e:
            print(f"Error fetching leaderboard data: {e}")
            flash('Error loading leaderboard', 'error')
            return render_template('leaderboard.html',
                               leaderboard_data=[],
                               user_best_scores={},
                               quiz_data=quiz_data,
                               current_user=session['username'])
        finally:
            conn.close()
    
    return render_template('leaderboard.html',
                         leaderboard_data=[],
                         user_best_scores={},
                         quiz_data=quiz_data,
                         current_user=session['username'])

# @app.route('/profile')
# def profile():
#     if 'username' not in session:
#         return redirect(url_for('login'))
    
#     conn = get_db_connection()
#     if conn:
#         try:
#             cur = conn.cursor()
            
#             # Get user's quiz history
#             cur.execute("""
#                 SELECT 
#                     qr.quiz_id,
#                     qr.score,
#                     qr.total_questions,
#                     qr.percentage,
#                     qr.completed_at
#                 FROM quiz_results qr
#                 WHERE qr.user_id = ?
#                 ORDER BY qr.completed_at DESC
#             """, (session['user_id'],))
#             quiz_history = cur.fetchall()
            
#             # Get user stats
#             cur.execute("""
#                 SELECT 
#                     COUNT(DISTINCT quiz_id) as quizzes_taken,
#                     COUNT(*) as total_attempts,
#                     AVG(percentage) as avg_percentage,
#                     MAX(percentage) as max_percentage
#                 FROM quiz_results
#                 WHERE user_id = ?
#             """, (session['user_id'],))
#             stats = cur.fetchone()
            
#             return render_template('profile.html',
#                                username=session['username'],
#                                quiz_history=quiz_history,
#                                stats=stats,
#                                quiz_data=quiz_data)
#         except mariadb.Error as e:
#             print(f"Error fetching profile data: {e}")
#             flash('Error loading profile', 'error')
#             return render_template('profile.html',
#                                username=session['username'],
#                                quiz_history=[],
#                                stats=None,
#                                quiz_data=quiz_data)
#         finally:
#             conn.close()
    
#     return render_template('profile.html',
#                          username=session['username'],
#                          quiz_history=[],
#                          stats=None,
#                          quiz_data=quiz_data)


@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            # Get user's quiz history
            cur.execute("""
                SELECT 
                    qr.quiz_id,
                    qr.score,
                    qr.total_questions,
                    qr.percentage,
                    qr.completed_at
                FROM quiz_results qr
                WHERE qr.user_id = ?
                ORDER BY qr.completed_at DESC
            """, (session['user_id'],))
            quiz_history = cur.fetchall()
            
            # Get user stats - handle NULL cases
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT quiz_id) as quizzes_taken,
                    COUNT(*) as total_attempts,
                    COALESCE(AVG(percentage), 0) as avg_percentage,
                    COALESCE(MAX(percentage), 0) as max_percentage
                FROM quiz_results
                WHERE user_id = ?
            """, (session['user_id'],))
            stats = cur.fetchone()
            
            return render_template('profile.html',
                               username=session['username'],
                               quiz_history=quiz_history,
                               stats=stats,
                               quiz_data=quiz_data)
        except mariadb.Error as e:
            print(f"Error fetching profile data: {e}")
            flash('Error loading profile', 'error')
            # Return default stats if error occurs
            return render_template('profile.html',
                               username=session['username'],
                               quiz_history=[],
                               stats=(0, 0, 0, 0),  # Default values
                               quiz_data=quiz_data)
        finally:
            conn.close()
    
    return render_template('profile.html',
                         username=session['username'],
                         quiz_history=[],
                         stats=(0, 0, 0, 0),  # Default values
                         quiz_data=quiz_data)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
