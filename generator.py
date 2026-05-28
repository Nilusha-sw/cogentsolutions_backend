from datetime import date

def generate_invitation(user: dict, session: dict) -> str:
    name       = user.get("name", "")
    focus      = user.get("focus", "")
    challenges = user.get("challenges", "")
    industry   = user.get("industry", "")

    title       = session["title"]
    speaker     = session["speaker"]
    time_slot   = session["time"]
    description = session["description"]

    challenge_line = ""
    if challenges.strip():
        challenge_line = (
            f"We understand that professionals in your position often face "
            f"challenges such as {challenges.lower().rstrip('.')}. "
            f"This session speaks directly to those concerns.\n\n"
        )

    industry_line = f" in {industry}" if industry.strip() else ""

    email = f"""Subject: Your Personalised Invitation — {title} | AccelAlpha × Oracle Summit

Dear {name},

On behalf of AccelAlpha and Oracle, we are pleased to extend an exclusive invitation to the executive summit:

    Troubled Waters: Sailing with AI in Supply Chain
    13 November 2024 · 09:30 AM – 01:00 PM
    Marriott Resort, The Palm, Dubai

─────────────────────────────────────────
YOUR MATCHED SESSION
─────────────────────────────────────────
Title   : {title}
Speaker : {speaker}
Time    : {time_slot}

{description}
─────────────────────────────────────────

Given your professional focus{industry_line} in the area of {focus.lower().rstrip('.')}, we believe this session is particularly relevant to you.

{challenge_line}This is a closed-door, invitation-only event designed for senior executives and operational leaders. Seats are strictly limited.

To confirm your attendance, please register at your earliest convenience. We look forward to welcoming you to The Palm.

Warm regards,
The AccelAlpha × Oracle Events Team
accelalpha.com · oracle.com
"""
    return email.strip()
