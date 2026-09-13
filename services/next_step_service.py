import os
import json

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def generate_personalized_next_step(
    journal_text,
    mood=None,
    emotional_state=None,
    main_concern=None
):
    """
    Generate one personalized, practical next step using Groq.

    This is separate from the main journal AI response so that
    Your Next Step can be requested only when the user chooses
    to personalize it.

    Returns None if Groq is unavailable or the response is invalid.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    try:

        client = Groq(
            api_key=api_key
        )

        prompt = f"""
You are assisting a Christian reflection application called Hope Journal.

The user has already written a journal entry and received an
emotional reflection.

Your task is to suggest ONE small, practical, safe and manageable
next step the person could choose for themselves.

Do not diagnose the person.
Do not provide medical advice.
Do not make promises about the future.
Do not claim to know exactly what the person is thinking.
Do not shame, judge, pressure, or command the user.
Do not suggest anything dangerous or extreme.

The goal is not to solve the person's whole problem.
The goal is to suggest one realistic action that may help them
move through the present moment.

Journal entry:
{journal_text}

Selected mood:
{mood if mood else "Not specified"}

Emotional state from the journal reflection:
{emotional_state if emotional_state else "Not specified"}

Main concern from the journal reflection:
{main_concern if main_concern else "Not specified"}

Return ONLY valid JSON in this exact structure:

{{
    "title": "",
    "text": "",
    "alternatives": [
        {{
            "title": "",
            "text": ""
        }},
        {{
            "title": "",
            "text": ""
        }},
        {{
            "title": "",
            "text": ""
        }}
    ]
}}

Guidelines:

1. Make the main step specific to the journal entry.
2. Make it something the user could reasonably do today.
3. Keep it small and practical.
4. Preserve the user's choice and autonomy.
5. Include three alternative small steps.
6. Prefer actions such as:
   - reaching out to someone trusted
   - taking a short break
   - breathing or grounding
   - drinking water or caring for basic needs
   - writing down one manageable task
   - spending time near supportive people
   - taking one small constructive action
7. Keep every section concise.
"""

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate safe, practical, "
                        "supportive next-step suggestions "
                        "for Hope Journal."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_completion_tokens=600
        )

        content = (
            completion
            .choices[0]
            .message
            .content
            .strip()
        )

        # Remove accidental markdown fences
        if content.startswith("```"):

            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            )

            content = content.strip()

        response = json.loads(content)

        if not isinstance(response, dict):
            return None

        if not response.get("title"):
            return None

        if not response.get("text"):
            return None

        alternatives = response.get(
            "alternatives",
            []
        )

        if not isinstance(alternatives, list):
            return None

        if len(alternatives) < 3:
            return None

        for alternative in alternatives[:3]:

            if not isinstance(alternative, dict):
                return None

            if not alternative.get("title"):
                return None

            if not alternative.get("text"):
                return None

        return {
            "title": response["title"],
            "text": response["text"],
            "alternatives": alternatives[:3]
        }

    except Exception as error:

        print(
            "Personalized Next Step AI error:",
            error
        )

        return None