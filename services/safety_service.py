# ============================================================
# HOPE JOURNAL
# Safety Service
# ============================================================

import re


# ============================================================
# SAFETY MESSAGE
# ============================================================

SAFETY_MESSAGE = (
    "If what you're experiencing feels overwhelming or you "
    "feel unsafe, please consider reaching out to a trusted "
    "person or a qualified professional who can support you."
)


# ============================================================
# CONCERN KEYWORDS
# ============================================================

CONCERN_KEYWORDS = [

    "unsafe",

    "in danger",

    "hurt myself",

    "hurting myself",

    "want to die",

    "kill myself",

    "suicide",

    "suicidal",

    "self harm",

    "self-harm"

]


# ============================================================
# CHECK JOURNAL TEXT
# ============================================================

def contains_safety_concern(text):

    """
    Check whether journal text contains language
    that may require additional safety attention.
    """

    if not text:

        return False


    normalized_text = text.lower().strip()


    for keyword in CONCERN_KEYWORDS:

        if keyword in normalized_text:

            return True


    return False


# ============================================================
# GET SAFETY RESPONSE
# ============================================================

def get_safety_response(text):

    """
    Return a simple safety status for journal processing.
    """

    if contains_safety_concern(text):

        return {

            "flagged": True,

            "message": SAFETY_MESSAGE

        }


    return {

        "flagged": False,

        "message": None

    }


# ============================================================
# CLEAN TEXT FOR BASIC CHECKING
# ============================================================

def normalize_text(text):

    """
    Normalize text before safety checks.
    """

    if not text:

        return ""


    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()