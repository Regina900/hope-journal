from collections import Counter

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from database.models import JournalEntry


insights = Blueprint("insights", __name__)


# ============================================================
# INSIGHTS PAGE
# ============================================================

@insights.route("/insights")
@login_required
def insights_page():

    # --------------------------------------------------------
    # GET ONLY THE CURRENT USER'S JOURNAL ENTRIES
    # --------------------------------------------------------

    entries = JournalEntry.query.filter_by(
        user_id=current_user.id
    ).order_by(
        JournalEntry.created_at.desc()
    ).all()


    # --------------------------------------------------------
    # TOTAL JOURNAL ENTRIES
    # --------------------------------------------------------

    total_entries = len(entries)


    # --------------------------------------------------------
    # FIND THE MOST COMMON MOOD
    # --------------------------------------------------------

    moods = [
        entry.mood
        for entry in entries
        if entry.mood
    ]


    if moods:

        mood_counts = Counter(moods)

        common_mood = mood_counts.most_common(1)[0][0]

    else:

        common_mood = None


    # --------------------------------------------------------
    # COUNT SAVED HOPE RESPONSES
    # --------------------------------------------------------

    response_count = sum(
        1
        for entry in entries
        if entry.response
    )


    # --------------------------------------------------------
    # GET MOST RECENT ENTRY
    # --------------------------------------------------------

    if entries:

        recent_entry = entries[0]

    else:

        recent_entry = None


    # --------------------------------------------------------
    # DISPLAY INSIGHTS PAGE
    # --------------------------------------------------------

    return render_template(
        "insights.html",

        total_entries=total_entries,

        common_mood=common_mood,

        response_count=response_count,

        recent_entry=recent_entry
    )