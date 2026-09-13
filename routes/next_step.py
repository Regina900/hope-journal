from flask import (
    Blueprint,
    render_template,
    request
)

from flask_login import (
    login_required,
    current_user
)

from database.models import JournalEntry

from services.safety_service import (
    get_safety_response
)

from services.next_step_service import (
    generate_personalized_next_step
)


next_step = Blueprint(
    "next_step",
    __name__
)


def get_default_next_step(
    mood=None,
    emotional_state=None,
    main_concern=None
):
    """
    Create a safe guided next step without calling AI.
    """

    mood_text = str(
        mood or ""
    ).lower()

    state_text = str(
        emotional_state or ""
    ).lower()

    concern_text = str(
        main_concern or ""
    ).lower()

    combined = (
        mood_text
        + " "
        + state_text
        + " "
        + concern_text
    )

    # ----------------------------------------
    # ANXIETY / WORRY / OVERWHELM
    # ----------------------------------------

    if any(
        word in combined
        for word in [
            "anxious",
            "anxiety",
            "worried",
            "worry",
            "fear",
            "overwhelm",
            "nervous",
            "stress"
        ]
    ):

        return {
            "title":
                "Give your mind a moment to slow down",

            "text":
                "You do not have to solve everything right now. "
                "Take five slow breaths, notice what is around you, "
                "and choose one small part of today that you can "
                "actually control.",

            "alternatives": [
                {
                    "title":
                        "Name one worry",

                    "text":
                        "Write down one thing worrying you and "
                        "one part of it that you can influence today."
                },
                {
                    "title":
                        "Take a short pause",

                    "text":
                        "Step away from your screen for a few "
                        "minutes and give yourself some quiet."
                },
                {
                    "title":
                        "Reach out",

                    "text":
                        "Tell someone you trust that today feels "
                        "heavier than usual."
                }
            ]
        }

    # ----------------------------------------
    # SADNESS / LONELINESS
    # ----------------------------------------

    if any(
        word in combined
        for word in [
            "sad",
            "lonely",
            "alone",
            "hurt",
            "heartbroken",
            "discouraged",
            "disappointed",
            "empty"
        ]
    ):

        return {
            "title":
                "Reach toward connection",

            "text":
                "You do not have to carry a difficult feeling "
                "completely by yourself. Consider reaching out "
                "to someone you trust and letting them know you "
                "could use some company or conversation.",

            "alternatives": [
                {
                    "title":
                        "Send a simple message",

                    "text":
                        "Try saying, 'I'm having a difficult day. "
                        "Can we talk for a little while?'"
                },
                {
                    "title":
                        "Stay near supportive people",

                    "text":
                        "Spend a little time somewhere safe "
                        "where you do not have to be completely alone."
                },
                {
                    "title":
                        "Keep writing",

                    "text":
                        "Put one more honest thought into your "
                        "journal instead of keeping it all inside."
                }
            ]
        }

    # ----------------------------------------
    # ANGER / FRUSTRATION
    # ----------------------------------------

    if any(
        word in combined
        for word in [
            "angry",
            "anger",
            "frustrated",
            "frustration",
            "mad",
            "irritated",
            "unfair"
        ]
    ):

        return {
            "title":
                "Create some space before responding",

            "text":
                "Give yourself a few quiet minutes before "
                "responding to what happened. A short pause "
                "can help you choose your response instead "
                "of reacting from the strongest emotion.",

            "alternatives": [
                {
                    "title":
                        "Step away",

                    "text":
                        "Take a short break before sending a "
                        "message or making an important decision."
                },
                {
                    "title":
                        "Write it out",

                    "text":
                        "Write what you wish someone understood "
                        "about what happened."
                },
                {
                    "title":
                        "Talk when ready",

                    "text":
                        "When you feel calmer, consider talking "
                        "with someone you trust."
                }
            ]
        }

    # ----------------------------------------
    # CONFUSION / UNCERTAINTY
    # ----------------------------------------

    if any(
        word in combined
        for word in [
            "confused",
            "confusion",
            "uncertain",
            "uncertainty",
            "lost",
            "unclear",
            "direction"
        ]
    ):

        return {
            "title":
                "Choose one next decision",

            "text":
                "You do not need every answer at once. "
                "Choose one small decision you can make today "
                "and allow the rest to wait.",

            "alternatives": [
                {
                    "title":
                        "Write the choices",

                    "text":
                        "Put the situation into a few simple "
                        "options instead of carrying them all "
                        "in your head."
                },
                {
                    "title":
                        "Take one small action",

                    "text":
                        "Choose the smallest useful step you "
                        "could take next."
                },
                {
                    "title":
                        "Take a quiet moment",

                    "text":
                        "Pray, reflect, and give yourself permission "
                        "not to decide everything today."
                }
            ]
        }

    # ----------------------------------------
    # DEFAULT
    # ----------------------------------------

    return {
        "title":
            "Take one small step today",

        "text":
            "Choose one manageable thing you can do right now. "
            "It could be taking a short break, writing down what "
            "you are feeling, caring for your body, or reaching "
            "out to someone you trust.",

        "alternatives": [
            {
                "title":
                    "Pause and breathe",

                "text":
                    "Take five slow breaths and give yourself "
                    "a quiet moment."
            },
            {
                "title":
                    "Care for yourself",

                "text":
                    "Drink some water, stretch, or step away "
                    "from your screen for a few minutes."
            },
            {
                "title":
                    "Put it into words",

                "text":
                    "Write down one thing you are feeling "
                    "without worrying about making it perfect."
            }
        ]
    }


@next_step.route(
    "/next-step",
    methods=["GET", "POST"]
)
@login_required
def next_step_page():

    # --------------------------------------------------
    # Get latest journal entry
    # --------------------------------------------------

    latest_entry = (
        JournalEntry.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            JournalEntry.created_at.desc()
        )
        .first()
    )

    mood = None
    emotional_state = None
    main_concern = None

    safety_flagged = False
    safety_message = None

    personalized = None

    # --------------------------------------------------
    # Read existing saved journal analysis
    # --------------------------------------------------

    if latest_entry:

        mood = latest_entry.mood

        if latest_entry.response:

            emotional_state = (
                latest_entry
                .response
                .emotional_state
            )

            main_concern = (
                latest_entry
                .response
                .main_concern
            )

        # ------------------------------------------------
        # Existing safety service
        # ------------------------------------------------

        safety = get_safety_response(
            latest_entry.content
        )

        safety_flagged = safety["flagged"]

        safety_message = safety["message"]

    # --------------------------------------------------
    # Safe default
    # --------------------------------------------------

    default_step = get_default_next_step(
        mood=mood,
        emotional_state=emotional_state,
        main_concern=main_concern
    )

    # --------------------------------------------------
    # Optional Groq personalization
    # --------------------------------------------------

    if (
        request.method == "POST"
        and latest_entry
        and not safety_flagged
    ):

        personalized = (
            generate_personalized_next_step(
                journal_text=latest_entry.content,
                mood=mood,
                emotional_state=emotional_state,
                main_concern=main_concern
            )
        )

    return render_template(
        "next_step.html",

        latest_entry=latest_entry,

        mood=mood,

        emotional_state=emotional_state,

        main_concern=main_concern,

        safety_flagged=safety_flagged,

        safety_message=safety_message,

        default_step=default_step,

        personalized=personalized
    )