from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/survey", methods=["GET", "POST"])
def survey():
    return render_template("survey.html")


@app.route("/sumbit", methods=["GET", "POST"])
def submit():
    try:

        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')
        q4 = request.form.get('q4')
        q5 = request.form.get('q5')
        q6 = request.form.get('q6')
        q7 = request.form.get('q7')
        q8 = request.form.get('q8')

        if not q1 or not q2 or not q3 or not q4 or not q5 or not q6 or not q7 or not q8:
            return "Error: All questions must be answered.", 400

        with conn = sqlite3.connect('questions.db') as conn:
            cursor = conn.cursor()

            cursor.execute("INSERT INTO user_responses (question_id, answer_id) VALUES (?, ?)", (1, q1))
            user_id = cursor.lastrowid

            
            cursor.execute("INSERT INTO user_responses (question_id, answer_id) VALUES (?, ?)", (2, q2))
            cursor.execute("INSERT INTO user_responses (question_id, answer_id) VALUES (?, ?)", (3, q3))
            cursor.execute("INSERT INTO user_responses (question_id, answer_id) VALUES (?, ?)", (4, q4))
            cursor.execute("INSERT INTO user_responses (question_id, answer_id) VALUES (?, ?)", (5, q5))
            cursor.execute("INSERT INTO user_responses (question_id, answer_id) VALUES (?, ?)", (6, q6))
            cursor.execute("INSERT INTO user_responses (question_id, answer_id) VALUES (?, ?)", (7, q7))
            cursor.execute("INSERT INTO user_responses (question_id, answer_id) VALUES (?, ?)", (8, q8))
            
            user_id = cursor.lastrowid

            conn.commit()
            

        return redirect(url_for('results', user_id=user_id))
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/results')
def results():
    user_id = request.args.get('user_id')  # Get user ID from URL

    # Connect to database
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()

    # Get the user's answers from the `user_responses` table
    cursor.execute("SELECT answer_id FROM user_responses WHERE id = ?", (user_id,))
    user_answers = [row[0] for row in cursor.fetchall()]

    # Find all matching destinations and count occurrences
    cursor.execute("""
        SELECT d.name, COUNT(*) AS score 
        FROM recommendations r
        JOIN destinations d ON r.destination_id = d.id
        WHERE r.answer_id IN ({})
        GROUP BY d.name
        ORDER BY score DESC
    """.format(','.join(['?']*len(user_answers))), tuple(user_answers))

    all_destinations = cursor.fetchall()  # List of (destination, score)

    # Close database connection
    conn.close()

    # Categorize destinations into 3 groups
    top_recommendations = [d for d in all_destinations if d[1] >= 5]  # Score ≥ 5
    good_matches = [d for d in all_destinations if 3 <= d[1] <= 4]  # Score 3-4
    consider_visiting = [d for d in all_destinations if d[1] <= 2]  # Score ≤ 2

    return render_template("results.html", top_recommendations=top_recommendations, good_matches=good_matches, consider_visiting=consider_visiting)





if __name__ == "__main__":
    app.run(debug=True)