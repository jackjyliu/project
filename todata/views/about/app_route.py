from todata import app
from flask import render_template, request
from todata.data.sql.functions import sql_write


@app.route("/about", methods=['POST', 'GET'])
def about():
    if request.method == 'POST':
        email = request.form.get('email')
        comment = request.form.get("comment")
        
        # write to email and comment and timestamp to db
        write_db = "toronto"
        query = """
                BEGIN;
                INSERT INTO website_comments (ts, email, user_comment) VALUES (CURRENT_TIMESTAMP, %s, %s);
                COMMIT;
                """
        records = (email, comment)
        sql_write(write_db, query, records, single_insert=True)

        return render_template("thanks.html")

    return render_template("about.html")