from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from matcher import SessionMatcher
from generator import generate_invitation

app = FastAPI(title="AccelAlpha Oracle — TF-IDF Event Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

matcher = SessionMatcher(agenda_path="agenda.txt")
print(f"[startup] TF-IDF index ready — {len(matcher.sessions)} sessions indexed.")


class InviteRequest(BaseModel):
    name:       str
    email:      str
    focus:      str
    challenges: str = ""
    industry:   str = ""


def send_draft_via_mcp(email_address: str, email_body: str) -> None:
    utc_time = datetime.now(timezone.utc).isoformat()
    print("\n" + "=" * 56)
    print("[MCP AUTOMATION TRIGGERED]")
    print(f"Recipient : {email_address}")
    print(f"Timestamp : {utc_time}")
    print("\nGenerated Draft:\n")
    print(email_body)
    print("=" * 56 + "\n")


@app.post("/generate-invite")
async def generate_invite(req: InviteRequest):
    query = f"{req.focus} {req.challenges} {req.industry}".strip()
    result = matcher.match(query)

    if result["matched"] is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No session matched your profile "
                f"(best cosine score: {result['score']:.4f}). "
                "Try describing your professional focus in more detail."
            ),
        )

    session = result["matched"]

    invitation = generate_invitation(
        user={
            "name":       req.name,
            "focus":      req.focus,
            "challenges": req.challenges,
            "industry":   req.industry,
        },
        session=session,
    )

    send_draft_via_mcp(req.email, invitation)

    return {
        "matchedSession":  session,
        "similarityScore": result["score"],
        "invitation":      invitation,
    }


@app.get("/health")
def health():
    return {"status": "running", "sessions_indexed": len(matcher.sessions)}


@app.get("/debug/scores")
async def debug_scores(q: str):
    result = matcher.match(q)
    return {
        "query":      q,
        "best_score": result["score"],
        "rankings": [
            {
                "rank":  i + 1,
                "title": r["session"]["title"],
                "score": round(r["score"], 4),
            }
            for i, r in enumerate(result["ranked"])
        ],
    }
