from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/survey", methods=["GET", "POST"])
def survey():
    return render_template("survey.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        # Get user responses from the form
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

        # Use `with` block to handle database connection properly
        with sqlite3.connect('questions.db') as conn:
            cursor = conn.cursor()

            # Insert a user record without providing user_id (it will be generated automatically)
            cursor.execute("INSERT INTO users DEFAULT VALUES")
            user_id = cursor.lastrowid  # Get the last generated user_id

            # Insert the user's answers into the `user_responses` table, using the generated user_id
            cursor.execute("INSERT INTO user_responses (user_id, question_id, answer_id) VALUES (?, ?, ?)", (user_id, 1, q1))
            cursor.execute("INSERT INTO user_responses (user_id, question_id, answer_id) VALUES (?, ?, ?)", (user_id, 2, q2))
            cursor.execute("INSERT INTO user_responses (user_id, question_id, answer_id) VALUES (?, ?, ?)", (user_id, 3, q3))
            cursor.execute("INSERT INTO user_responses (user_id, question_id, answer_id) VALUES (?, ?, ?)", (user_id, 4, q4))
            cursor.execute("INSERT INTO user_responses (user_id, question_id, answer_id) VALUES (?, ?, ?)", (user_id, 5, q5))
            cursor.execute("INSERT INTO user_responses (user_id, question_id, answer_id) VALUES (?, ?, ?)", (user_id, 6, q6))
            cursor.execute("INSERT INTO user_responses (user_id, question_id, answer_id) VALUES (?, ?, ?)", (user_id, 7, q7))
            cursor.execute("INSERT INTO user_responses (user_id, question_id, answer_id) VALUES (?, ?, ?)", (user_id, 8, q8))

            conn.commit()

        # Redirect the user to the results page with their user_id
        return redirect(url_for('results', user_id=user_id))

    except Exception as e:
        return f"An error occurred: {str(e)}", 500



@app.route('/results')
def results():
    user_id = request.args.get('user_id')  # Get user ID from URL

    # Connect to database
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()

    # Get user's answers (currently stored as answer_text, convert to answer_id)
    cursor.execute("SELECT answer_id FROM user_responses WHERE user_id = ?", (user_id,))
    user_answer_texts = [row[0] for row in cursor.fetchall()]  # These are still answer_text, need conversion

    print("User selected answer TEXTS:", user_answer_texts)  # Debugging

    if not user_answer_texts:
        return "No answers found for this user. Please try again.", 400

    # 🔹 Convert answer_text to answer_id
    placeholders = ', '.join(['?'] * len(user_answer_texts))  # Create placeholders for SQL query
    cursor.execute(f"SELECT id FROM answers WHERE answer_text IN ({placeholders})", tuple(user_answer_texts))
    user_answer_ids = [row[0] for row in cursor.fetchall()]  # Get a list of answer_id values

    print("Converted answer IDs:", user_answer_ids)  # Debugging

    if not user_answer_ids:
        return "No matching answers found in the database.", 400

    # 🔹 Query for matching destinations using answer_id
    try:
        placeholders = ', '.join(['?'] * len(user_answer_ids))  # Create placeholders again
        cursor.execute(f"""
            SELECT d.name, COUNT(*) AS score 
            FROM recommendations r
            JOIN destinations d ON r.destination_id = d.id
            WHERE r.answer_id IN ({placeholders})
            GROUP BY d.name
            ORDER BY score DESC
        """, tuple(user_answer_ids))

        all_destinations = cursor.fetchall()  # List of (destination, score)

        print("Matching Destinations:", all_destinations)  # Debugging

    except Exception as e:
        print("Error during query execution:", str(e))
        return "An error occurred while fetching destinations.", 500

    conn.close()

    if not all_destinations:
        return "No matching destinations found.", 400

    # Categorize destinations
    top_recommendations = [d for d in all_destinations if d[1] >= 5]  # Score ≥ 5
    good_matches = [d for d in all_destinations if 3 <= d[1] <= 4]  # Score 3-4
    consider_visiting = [d for d in all_destinations if d[1] <= 2]  # Score ≤ 2

    return render_template("results.html", 
                           top_recommendations=top_recommendations, 
                           good_matches=good_matches, 
                           consider_visiting=consider_visiting)



@app.route('/destination/<name>')
def destination_details(name):
    destination_templates = {
        "Tokyo": "destination_tokyo.html",
        "Kyoto": "destination_kyoto.html",
        "Osaka": "destination_osaka.html",
        "Hokkaido": "destination_hokkaido.html",
        "Sapporo": "destination_sapporo.html",
        "Hiroshima": "destination_hiroshima.html",
        "Fukuoka": "destination_fukuoka.html",
        "Nara": "destination_nara.html",
        "Hakone": "destination_hakone.html",
        "Kanazawa": "destination_kanazawa.html",
        "Shikoku": "destination_shikoku.html", 
        "Okinawa": "destination_okinawa.html"   

    }

    if name in destination_templates:
        return render_template(destination_templates[name])
    else:
        return "Destination not found", 404





if __name__ == "__main__":
    app.run(debug=True)