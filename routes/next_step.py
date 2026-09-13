from flask import Blueprint, render_template
from flask_login import login_required


next_step = Blueprint(
    "next_step",
    __name__
)


@next_step.route("/next-step")
@login_required
def next_step_page():

    return render_template(
        "next_step.html"
    )