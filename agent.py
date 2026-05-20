import os
from enum import Enum

GITHUB_TOKEN_ENV_VAR = "GITHUB_TOKEN"


class AgentType(Enum):
    IMPLEMENTER = "implementer"
    REVIEWER = "reviewer"
    SECURITY = "security"
    ARCHITECT = "architect"
    QA = "qa"
    PR_AUTHOR = "pr_author"
    PR_REVIEWER = "pr_reviewer"


def execute_task(task: dict) -> AgentType:
    try:
        agent = AgentType(task["agent"])
    except ValueError:
        agent = AgentType.IMPLEMENTER
    return agent


class PRReviewWorkflow:
    def run(self, pr_number: int, repo: str | None = None) -> str:
        """Returns a prompt string for reviewing the given PR."""
        prompt = f"Review PR #{pr_number}"
        if repo is not None:
            prompt += f" in repository {repo}"
        return prompt


def build_docker_env(agent_type: AgentType) -> dict:
    env = {}
    if agent_type is AgentType.PR_REVIEWER:
        env[GITHUB_TOKEN_ENV_VAR] = os.environ[GITHUB_TOKEN_ENV_VAR]
    return env
