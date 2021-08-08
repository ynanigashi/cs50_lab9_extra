import os
import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Birthdays, Base
from sqlalchemy import select


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#use in flash
app.config['SECRET_KEY'] = b'\x08\x14\x15\xde\x041h5\x1b\xd8\xc0Wb\x8e\x83\x1f\xbd\xec\xfb\xce\x85\xd2\xae\xeb'

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
                birthday = Birthdays(name=name, month=month, day=day)
                ss.add(birthday)
                ss.commit()
        flash(f"{name}'s birthday has saved", 'success')
        return redirect("/")

    else:
        # Display the entries in the database on index.html
        birthdays = []
        with Session(engine) as ss:
            stmt = select(Birthdays.name, Birthdays.month, Birthdays.day).order_by(Birthdays.id.desc())
            for name, month, day in ss.execute(stmt):
                birthdays.append({'name': name, 'month': month, 'day': day})

        return render_template("index.html", birthdays=birthdays)

@app.route('/init_db')
def init_db():
    try:
        Base.metadata.drop_all(engine)
    except Exception as e:
        print('drop error! but continue')

    Base.metadata.create_all(engine)
    return {"result": "ok"}


if __name__ == '__main__':
    app.run()