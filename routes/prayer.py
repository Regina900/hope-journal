from flask import Blueprint, render_template
from flask_login import login_required, current_user

from database.database import db
from database.models import JournalEntry, AIResponse


prayer = Blueprint("prayer", __name__)


# ============================================================
# PRAYER PAGE
# ============================================================

@prayer.route("/prayer")
@login_required
def prayer_page():

    # --------------------------------------------------------
    # GET THE USER'S JOURNAL ENTRIES
    # --------------------------------------------------------

    entries = JournalEntry.query.filter_by(
        user_id=current_user.id
    ).order_by(
        JournalEntry.created_at.desc()
    ).all()


    # --------------------------------------------------------
    # GET SAVED PRAYERS
    # --------------------------------------------------------

    prayers = []

    for entry in entries:

        if entry.response and entry.response.prayer:

            prayers.append({

                "entry_id": entry.id,

                "created_at": entry.created_at,

                "mood": entry.mood,

                "prayer": entry.response.prayer

            })


    # --------------------------------------------------------
    # SHOW PRAYER PAGE
    # --------------------------------------------------------

    return render_template(
        "prayer.html",
        prayers=prayers
    )