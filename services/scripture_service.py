# ============================================================
# HOPE JOURNAL
# Scripture Service
# ============================================================


# ============================================================
# DEFAULT SCRIPTURES
# ============================================================

SCRIPTURES = [

    {
        "reference": "Psalm 34:18",
        "text": "The Lord is close to the brokenhearted."
    },

    {
        "reference": "Isaiah 41:10",
        "text": "Do not fear, for I am with you; do not be dismayed, for I am your God."
    },

    {
        "reference": "Jeremiah 29:11",
        "text": "For I know the plans I have for you, plans to prosper you and not to harm you, plans to give you hope and a future."
    },

    {
        "reference": "Psalm 46:1",
        "text": "God is our refuge and strength, an ever-present help in trouble."
    },

    {
        "reference": "Matthew 11:28",
        "text": "Come to me, all you who are weary and burdened, and I will give you rest."
    },

    {
        "reference": "Romans 15:13",
        "text": "May the God of hope fill you with all joy and peace as you trust in him."
    },

    {
        "reference": "Philippians 4:6-7",
        "text": "Do not be anxious about anything, but present your requests to God."
    },

    {
        "reference": "Psalm 23:4",
        "text": "Even though I walk through the darkest valley, I will fear no evil, for you are with me."
    }

]


# ============================================================
# GET ALL SCRIPTURES
# ============================================================

def get_scriptures():

    """
    Return the available Scripture collection.
    """

    return SCRIPTURES.copy()


# ============================================================
# GET ONE SCRIPTURE
# ============================================================

def get_scripture(reference):

    """
    Find a Scripture by its reference.

    Example:
        get_scripture("Psalm 34:18")
    """

    if not reference:
        return None


    for scripture in SCRIPTURES:

        if scripture["reference"].lower() == reference.lower():

            return scripture


    return None


# ============================================================
# SEARCH SCRIPTURES
# ============================================================

def search_scriptures(keyword):

    """
    Search the Scripture collection by reference or text.
    """

    if not keyword:

        return get_scriptures()


    keyword = keyword.lower().strip()


    results = []


    for scripture in SCRIPTURES:

        reference = scripture["reference"].lower()

        text = scripture["text"].lower()


        if keyword in reference or keyword in text:

            results.append(scripture)


    return results