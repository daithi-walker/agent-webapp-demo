import pytest
from agent import AgentType, PRReviewWorkflow, build_docker_env, execute_task


# ── execute_task: unknown agent falls back to IMPLEMENTER ─────────────────────


@pytest.mark.parametrize("bad_agent", ["bogus", "", "IMPLEMENTER"])
def test_execute_task_unknown_agent_falls_back_to_implementer(bad_agent):
    result = execute_task({"agent": bad_agent})
    assert result == AgentType.IMPLEMENTER


# ── PRReviewWorkflow.run ──────────────────────────────────────────────────────


def test_pr_review_workflow_run_includes_pr_number():
    pr_number = 42
    prompt = PRReviewWorkflow().run(pr_number)
    assert str(pr_number) in prompt


def test_pr_review_workflow_run_includes_repo_clause():
    repo = "acme/myrepo"
    prompt = PRReviewWorkflow().run(pr_number=7, repo=repo)
    assert repo in prompt


def test_pr_review_workflow_run_repo_absent_when_none():
    prompt = PRReviewWorkflow().run(pr_number=7, repo=None)
    assert "repository" not in prompt


# ── build_docker_env: GITHUB_TOKEN only for PR_REVIEWER ──────────────────────


def test_build_docker_env_github_token_present_for_pr_reviewer(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "tok-abc123")
    env = build_docker_env(AgentType.PR_REVIEWER)
    assert env["GITHUB_TOKEN"] == "tok-abc123"


@pytest.mark.parametrize(
    "agent_type",
    [m for m in AgentType if m is not AgentType.PR_REVIEWER],
)
def test_build_docker_env_github_token_absent_for_non_pr_reviewer(monkeypatch, agent_type):
    monkeypatch.setenv("GITHUB_TOKEN", "tok-abc123")
    env = build_docker_env(agent_type)
    assert "GITHUB_TOKEN" not in env
