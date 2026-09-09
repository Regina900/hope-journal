from flask import Blueprint, render_template
from flask_login import login_required, current_user

from database.models import JournalEntry


scriptures = Blueprint("scriptures", __name__)


# ============================================================
# SCRIPTURES PAGE
# ============================================================

@scriptures.route("/scriptures")
@login_required
def scriptures_page():

    # --------------------------------------------------------
    # GET ONLY THE CURRENT USER'S JOURNAL ENTRIES
    # --------------------------------------------------------

    entries = JournalEntry.query.filter_by(
        user_id=current_user.id
    ).order_by(
        JournalEntry.created_at.desc()
    ).all()


    # --------------------------------------------------------
    # COLLECT SAVED SCRIPTURES
    # --------------------------------------------------------

    scriptures_list = []

    for entry in entries:

        if entry.response:

            reference = entry.response.scripture_reference
            text = entry.response.scripture_text

            # Only include entries that actually
            # contain Scripture information.

            if reference or text:

                scriptures_list.append({

                    "entry_id": entry.id,

                    "created_at": entry.created_at,

                    "mood": entry.mood,

                    "reference": reference,

                    "text": text

                })


    # --------------------------------------------------------
    # DISPLAY SCRIPTURES PAGE
    # --------------------------------------------------------

    return render_template(
        "scriptures.html",
        scriptures=scriptures_list
    )