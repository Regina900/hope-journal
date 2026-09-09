from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from database.database import db
from database.models import JournalEntry, AIResponse

from services.ai_service import (
    generate_demo_response,
    generate_groq_response
)


journal = Blueprint("journal", __name__)


# ============================================================
# CREATE JOURNAL ENTRY
# ============================================================

@journal.route("/journal", methods=["GET", "POST"])
@login_required
def create_journal():

    if request.method == "GET":
        return render_template("journal.html")

    content = request.form.get("content", "").strip()
    mood = request.form.get("mood", "").strip()

    if not content:
        flash(
            "Please write something before saving your journal entry.",
            "error"
        )
        return render_template("journal.html")

    if len(content) > 5000:
        flash(
            "Your journal entry is too long. Please keep it under 5000 characters.",
            "error"
        )
        return render_template("journal.html")

    entry = JournalEntry(
        user_id=current_user.id,
        content=content,
        mood=mood if mood else None
    )

    db.session.add(entry)
    db.session.commit()

    ai_response = generate_groq_response(
        journal_text=content,
        mood=mood
    )

    if ai_response is None:
        ai_response = generate_demo_response(
            journal_text=content,
            mood=mood
        )

    saved_response = AIResponse(
        journal_entry_id=entry.id,
        emotional_state=ai_response.get("emotional_state"),
        main_concern=ai_response.get("main_concern"),
        biblical_encouragement=ai_response.get("biblical_encouragement"),
        scripture_reference=ai_response.get("scripture_reference"),
        scripture_text=ai_response.get("scripture_text"),
        hope_message=ai_response.get("hope_message"),
        prayer=ai_response.get("prayer"),
        reflection_question=ai_response.get("reflection_question"),
        affirmation=ai_response.get("affirmation")
    )

    db.session.add(saved_response)
    db.session.commit()

    flash(
        "Your journal entry has been saved. 💜",
        "success"
    )

    return render_template(
        "journal_view.html",
        entry=entry,
        response=ai_response
    )


# ============================================================
# JOURNAL HISTORY
# ============================================================

@journal.route("/journal/history")
@login_required
def journal_history():

    entries = JournalEntry.query.filter_by(
        user_id=current_user.id
    ).order_by(
        JournalEntry.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        entries=entries
    )


# ============================================================
# VIEW ONE JOURNAL ENTRY
# ============================================================

@journal.route("/journal/<int:entry_id>")
@login_required
def view_journal(entry_id):

    entry = JournalEntry.query.filter_by(
        id=entry_id,
        user_id=current_user.id
    ).first_or_404()

    if entry.response:

        response = {
            "emotional_state": entry.response.emotional_state,
            "main_concern": entry.response.main_concern,
            "biblical_encouragement": entry.response.biblical_encouragement,
            "scripture_reference": entry.response.scripture_reference,
            "scripture_text": entry.response.scripture_text,
            "hope_message": entry.response.hope_message,
            "prayer": entry.response.prayer,
            "reflection_question": entry.response.reflection_question,
            "affirmation": entry.response.affirmation
        }

    else:

        response = generate_groq_response(
            journal_text=entry.content,
            mood=entry.mood
        )

        if response is None:
            response = generate_demo_response(
                journal_text=entry.content,
                mood=entry.mood
            )

        saved_response = AIResponse(
            journal_entry_id=entry.id,
            emotional_state=response.get("emotional_state"),
            main_concern=response.get("main_concern"),
            biblical_encouragement=response.get("biblical_encouragement"),
            scripture_reference=response.get("scripture_reference"),
            scripture_text=response.get("scripture_text"),
            hope_message=response.get("hope_message"),
            prayer=response.get("prayer"),
            reflection_question=response.get("reflection_question"),
            affirmation=response.get("affirmation")
        )

        db.session.add(saved_response)
        db.session.commit()

    return render_template(
        "journal_view.html",
        entry=entry,
        response=response
    )


# ============================================================
# DELETE JOURNAL ENTRY
# ============================================================

@journal.route("/journal/<int:entry_id>/delete", methods=["POST"])
@login_required
def delete_journal(entry_id):

    entry = JournalEntry.query.filter_by(
        id=entry_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(entry)
    db.session.commit()

    flash(
        "Journal entry deleted successfully.",
        "success"
    )

    return redirect(
        url_for("journal.journal_history")
    )