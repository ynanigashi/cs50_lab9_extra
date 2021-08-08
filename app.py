import os
import re
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#use in flash
app.config['SECRET_KEY'] = b'\x08\x14\x15\xde\x041h5\x1b\xd8\xc0Wb\x8e\x83\x1f\xbd\xec\xfb\xce\x85\xd2\xae\xeb'

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

# create sqlalchemy engin
# create_engine.future flag set to True so that we make full use of 2.0 style usage:
# create_engine.echo, which will instruct the Engine to log all of the SQL it emits to a Python logger that will write to standard out. This flag is a shorthand way of setting up Python logging more formally and is useful for experimentation in scripts.
engine = create_engine('sqlite+pysqlite:///birthdays.db', future=True, echo=True)

DATE_PATTERN = '^\d{4}(-\d{2}){2}$'


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        bday = request.form.get("birthday")
        print(f"{name}: {bday}")

        # validate form
        if not name:
            flash('name is missing.', 'failed')
        elif not re.match(DATE_PATTERN, bday):
            flash('date is invalid.', 'failed')
        else:
            month, day = int(bday[5:7]), int(bday[-2:])
            with Session(engine) as ss:
                result = ss.execute(text("INSERT INTO birthdays (name, month, day) VALUES(:name, :month, :day)"), 
                                    {'name': name, 'month': month, 'day': day})
                print(result)
                ss.commit()
                flash(f"{name}'s birthday has saved", 'success')

        return redirect("/")

    else:
        # Display the entries in the database on index.html
        birthdays = []
        with Session(engine) as ss:
            rows = ss.execute(text("SELECT * FROM birthdays ORDER BY id DESC"))
            for row in rows:
                birthdays.append(row)

        return render_template("index.html", birthdays=birthdays)


