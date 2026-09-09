# ============================================================
# HOPE JOURNAL
# Mood Service
# ============================================================


# ============================================================
# AVAILABLE MOODS
# ============================================================

MOODS = [

    "Hopeful",

    "Happy",

    "Peaceful",

    "Grateful",

    "Okay",

    "Confused",

    "Worried",

    "Sad",

    "Lonely",

    "Overwhelmed",

    "Angry",

    "Tired"

]


# ============================================================
# GET ALL MOODS
# ============================================================

def get_moods():

    """
    Return the list of available journal moods.
    """

    return MOODS.copy()


# ============================================================
# CHECK WHETHER A MOOD IS VALID
# ============================================================

def is_valid_mood(mood):

    """
    Check whether a supplied mood exists
    in the available mood list.
    """

    if not mood:

        return False


    mood = mood.strip().lower()


    return any(
        available_mood.lower() == mood
        for available_mood in MOODS
    )


# ============================================================
# NORMALIZE MOOD
# ============================================================

def normalize_mood(mood):

    """
    Return the correctly formatted version of a mood.

    Example:
        "hopeful" -> "Hopeful"
    """

    if not mood:

        return None


    mood = mood.strip().lower()


    for available_mood in MOODS:

        if available_mood.lower() == mood:

            return available_mood


    return None


# ============================================================
# GET MOOD CATEGORY
# ============================================================

def get_mood_category(mood):

    """
    Group moods into broad emotional categories.

    This is used for future insights and statistics.
    """

    normalized = normalize_mood(mood)


    if not normalized:

        return "Unknown"


    positive = [

        "Hopeful",
        "Happy",
        "Peaceful",
        "Grateful"

    ]


    neutral = [

        "Okay",
        "Confused",
        "Tired"

    ]


    difficult = [

        "Worried",
        "Sad",
        "Lonely",
        "Overwhelmed",
        "Angry"

    ]


    if normalized in positive:

        return "Positive"


    if normalized in neutral:

        return "Neutral"


    if normalized in difficult:

        return "Difficult"


    return "Unknown"