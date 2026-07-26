import hashlib
import os
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
EMAIL = "23f3001167@ds.study.iitm.ac.in"
PUBLIC_HOST = "mcp-exam-server-bmxt.onrender.com"
mcp = FastMCP(
    "Exam Challenge MCP",

    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8000")),
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            PUBLIC_HOST,
            f"{PUBLIC_HOST}:*",
            "localhost:*",
            "127.0.0.1:*",
        ],
    ),
)
@mcp.tool()
async def solve_challenge(ctx: Context) -> str:
    """
    Return the first 16 lowercase hex characters of
    SHA-256(challenge:normalizedEmail).
    """

    # Get the actual HTTP request
    request = ctx.request_context.request

    if not isinstance(request, Request):
        raise ValueError("HTTP request is unavailable")

    # HTTP header names are case-insensitive
    challenge = request.headers.get("X-Exam-Challenge")

    if not challenge:
        raise ValueError("X-Exam-Challenge header is missing")

    # Email required by the assignment
    normalized_email = EMAIL.strip().lower()

    # EXACT required input:
    # challenge:normalizedEmail
    raw = f"{challenge}:{normalized_email}"

    # SHA-256 -> lowercase hex -> first 16 characters
    answer = hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()[:16]

    return answer


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
