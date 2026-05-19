import os
from enum import Enum


class AgentType(Enum):
    implementer = "implementer"
    reviewer = "reviewer"
    security = "security"
    architect = "architect"
    qa = "qa"
    pr_author = "pr_author"
    pr_reviewer = "pr_reviewer"


def _execute_task(task: dict):
    try:
        agent = AgentType(task["agent"])
    except ValueError:
        agent = AgentType.implementer
    return agent


class PRReviewWorkflow:
    def run(self, pr_number: int, repo: str | None = None) -> str:
        prompt = f"Review PR #{pr_number}"
        if repo is not None:
            prompt += f" in repository {repo}"
        return prompt


def _build_docker_env(agent_type: AgentType) -> dict:
    env = {}
    if agent_type is AgentType.pr_reviewer:
        env["GITHUB_TOKEN"] = os.environ["GITHUB_TOKEN"]
    return env
