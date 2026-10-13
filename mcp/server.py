
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("dev-agent-tools")

MISSIONS = {
    "TASK-001": {
        "title": "Add task priority",
        "status": "planned",
        "owner": "developer-agent",
    },
    "TASK-002": {
        "title": "Add unit tests",
        "status": "in_review",
        "owner": "reviewer-agent",
    },
}


@mcp.tool()
def get_mission_status(mission_id: str) -> dict:
    """Return the status of a known development task."""
    mission = MISSIONS.get(mission_id)

    if mission is None:
        return {
            "found": False,
            "message": "Task not found",
        }

    return {
        "found": True,
        "mission": mission,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
