import hashlib
import os

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.transport_security import TransportSecuritySettings


EMAIL = "23f3001167@ds.study.iitm.ac.in".strip().lower()

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
    Solve the exam challenge using the challenge supplied
    in the HTTP request header.
    """

    headers = ctx.request_context.headers

    if not headers:
        raise ValueError("HTTP request headers are missing")

    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("X-Exam-Challenge header is missing")

    value = f"{challenge}:{EMAIL}"

    digest = hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
