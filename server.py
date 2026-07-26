import hashlib
from mcp.server.fastmcp import FastMCP, Context


EMAIL = "23f3001167@ds.study.iitm.ac.in".strip().lower()


mcp = FastMCP(
    "Exam Challenge MCP",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
async def solve_challenge(ctx: Context) -> str:
    """
    Solve the exam challenge using the X-Exam-Challenge
    header from the current HTTP tool-call request.
    """

    headers = ctx.request_context.headers

    if not headers:
        raise ValueError("HTTP request headers are missing")

    challenge = headers.get("x-exam-challenge")

    if not challenge:
        challenge = headers.get("X-Exam-Challenge")

    if not challenge:
        raise ValueError("X-Exam-Challenge header is missing")

    value = f"{challenge}:{EMAIL}"

    digest = hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", "8000"))

    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = port

    mcp.run(transport="streamable-http")
