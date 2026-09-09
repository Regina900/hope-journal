import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def generate_demo_response(journal_text, mood=None):
    """
    Generate a Hope Journal response without using a real AI API.

    Demo Mode uses simple keyword matching to identify
    the main emotional theme.
    """

    text = journal_text.lower()

    # Default response
    response = {
        "emotional_state": "Uncertain",
        "main_concern": (
            "It sounds like you are carrying something that may "
            "feel difficult right now."
        ),
        "biblical_encouragement": "Hope",
        "scripture_reference": "Romans 15:13",
        "scripture_text": (
            "May the God of hope fill you with all joy and peace "
            "as you trust in Him."
        ),
        "hope_message": (
            "You do not have to figure everything out at once. "
            "Take today one step at a time and remember that "
            "difficult seasons can change."
        ),
        "prayer": (
            "God, please give me peace for what I cannot control, "
            "wisdom for the decisions ahead, and strength for today. "
            "Help me remember that I am not alone. Amen."
        ),
        "reflection_question": (
            "What is one small thing within your control that "
            "you can focus on today?"
        ),
        "affirmation": (
            "I can take one step at a time and hold on to hope."
        )
    }

    # -----------------------------
    # WORRY / ANXIETY / FEAR
    # -----------------------------

    worry_words = [
        "worried",
        "worry",
        "anxious",
        "anxiety",
        "nervous",
        "scared",
        "fear",
        "afraid",
        "overthinking",
        "uncertain"
    ]

    if any(word in text for word in worry_words):

        response = {
            "emotional_state": "Worried or anxious",

            "main_concern": (
                "It sounds like uncertainty or fear may be "
                "weighing heavily on you right now."
            ),

            "biblical_encouragement": "Trust",

            "scripture_reference": "Proverbs 3:5-6",

            "scripture_text": (
                "Trust in the Lord with all your heart and lean "
                "not on your own understanding."
            ),

            "hope_message": (
                "You do not need to know exactly how everything "
                "will work out before taking your next step. "
                "Give yourself permission to focus on what "
                "you can do today."
            ),

            "prayer": (
                "God, when I feel worried about what lies ahead, "
                "help me place my concerns in Your hands. "
                "Give me peace, wisdom, and courage for today. Amen."
            ),

            "reflection_question": (
                "What is one worry you could release today, "
                "and what is one small action you can take instead?"
            ),

            "affirmation": (
                "I do not have to know everything about tomorrow "
                "to move forward today."
            )
        }

    # -----------------------------
    # SADNESS / LONELINESS
    # -----------------------------

    elif any(word in text for word in [
        "sad",
        "unhappy",
        "lonely",
        "alone",
        "hurt",
        "heartbroken",
        "discouraged",
        "disappointed",
        "cry",
        "crying",
        "empty"
    ]):

        response = {
            "emotional_state": "Sad or discouraged",

            "main_concern": (
                "It sounds like you may be carrying disappointment, "
                "loneliness, or emotional heaviness."
            ),

            "biblical_encouragement": "Comfort",

            "scripture_reference": "Psalm 34:18",

            "scripture_text": (
                "The Lord is close to the brokenhearted and saves "
                "those who are crushed in spirit."
            ),

            "hope_message": (
                "You do not have to pretend that everything is fine. "
                "Your feelings deserve space, and this difficult "
                "moment does not define your whole story."
            ),

            "prayer": (
                "God, please meet me in this difficult moment. "
                "Bring comfort to my heart and help me remember "
                "that I am not alone. Give me strength for today. Amen."
            ),

            "reflection_question": (
                "What is something or someone that has brought you "
                "even a small sense of comfort recently?"
            ),

            "affirmation": (
                "It is okay to have difficult days, and I can still "
                "hold on to hope."
            )
        }

    # -----------------------------
    # ANGER / FRUSTRATION
    # -----------------------------

    elif any(word in text for word in [
        "angry",
        "anger",
        "mad",
        "frustrated",
        "frustration",
        "annoyed",
        "irritated",
        "unfair"
    ]):

        response = {
            "emotional_state": "Angry or frustrated",

            "main_concern": (
                "It sounds like something has left you feeling "
                "frustrated, hurt, or treated unfairly."
            ),

            "biblical_encouragement": "Peace",

            "scripture_reference": "James 1:19",

            "scripture_text": (
                "Everyone should be quick to listen, slow to speak "
                "and slow to become angry."
            ),

            "hope_message": (
                "Your feelings can tell you that something matters "
                "to you. Give yourself space to respond thoughtfully "
                "rather than letting one difficult moment control "
                "what happens next."
            ),

            "prayer": (
                "God, help me handle my frustration with wisdom. "
                "Give me patience, clarity, and peace as I respond "
                "to what has happened. Amen."
            ),

            "reflection_question": (
                "What do you wish someone understood about "
                "what happened today?"
            ),

            "affirmation": (
                "I can pause, breathe, and choose my response."
            )
        }

    # -----------------------------
    # CONFUSION / LACK OF DIRECTION
    # -----------------------------

    elif any(word in text for word in [
        "confused",
        "confusion",
        "lost",
        "don't know",
        "not sure",
        "unclear",
        "direction"
    ]):

        response = {
            "emotional_state": "Confused or uncertain",

            "main_concern": (
                "You may be searching for clarity or direction "
                "about what to do next."
            ),

            "biblical_encouragement": "Guidance",

            "scripture_reference": "James 1:5",

            "scripture_text": (
                "If any of you lacks wisdom, you should ask God, "
                "who gives generously to all without finding fault."
            ),

            "hope_message": (
                "You do not need to have every answer right now. "
                "Sometimes clarity comes one decision at a time."
            ),

            "prayer": (
                "God, please give me wisdom and clarity. "
                "Help me recognize the next right step and give "
                "me patience while I seek direction. Amen."
            ),

            "reflection_question": (
                "What is one decision you could break into a "
                "smaller and more manageable step?"
            ),

            "affirmation": (
                "I can seek wisdom and take the next step with courage."
            )
        }

    return response

def generate_groq_response(journal_text, mood=None):
    """
    Generate a personalized Hope Journal response using Groq.

    Returns None if Groq is unavailable so that the application
    can fall back to Demo Mode.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    try:

        client = Groq(api_key=api_key)

        prompt = f"""
You are the compassionate AI assistant inside a Christian
reflection application called Hope Journal.

A user has written about how they are feeling.

Your job is to respond with gentle, supportive,
non-judgmental encouragement.

User's journal entry:
{journal_text}

User's selected mood:
{mood if mood else "Not specified"}

Return ONLY valid JSON with these exact keys:

{{
    "emotional_state": "",
    "main_concern": "",
    "biblical_encouragement": "",
    "scripture_reference": "",
    "scripture_text": "",
    "hope_message": "",
    "prayer": "",
    "reflection_question": "",
    "affirmation": ""
}}

Guidelines:

1. Identify the main emotional theme of the entry.
2. Give ONE short biblical encouragement word.
3. Give one relevant Bible verse reference.
4. Give a short Scripture quotation.
5. Give a personalized hope message.
6. Give a short prayer.
7. Give one gentle reflection question.
8. Give one encouraging affirmation.
9. Do not shame or judge the user.
10. Do not claim to know exactly what the user is thinking.
11. Keep the response warm and appropriate for a general audience.
12. Do not diagnose mental-health conditions.
13. Do not give medical advice.
14. Do not make promises about the future.
15. Keep each section concise.
"""

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate structured Christian "
                        "encouragement for Hope Journal."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_completion_tokens=1200
        )

        content = completion.choices[0].message.content.strip()

        # Remove accidental markdown code fences
        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        response = json.loads(content)

        required_keys = [
            "emotional_state",
            "main_concern",
            "biblical_encouragement",
            "scripture_reference",
            "scripture_text",
            "hope_message",
            "prayer",
            "reflection_question",
            "affirmation"
        ]

        # Make sure the AI returned everything we need
        for key in required_keys:
            if key not in response:
                return None

        return response

    except Exception as error:

        print("Groq AI error:", error)

        return None