from __future__ import annotations


from typing import Any, List
from agent.toolkits.git_integrator.base import create_git_integration_toolkit
from agent.toolkits.git_integrator.pompt import GIT_AGENT_DESCRIPTION
from agent.toolkits.git_integrator.toolkit import GitIntegratorToolkit
from agent.toolkits.gitlab_integration.prompt import GITLAB_AGENT_DESCRIPTION
from agent.toolkits.gitlab_integration.toolkit import GitlabIntegrationToolkit
from agent.toolkits.k8s_explorer.base import create_k8s_explorer_agent
from agent.toolkits.k8s_explorer.prompt import K8S_EXPLORER_AGENT_DESCRIPTION
from agent.toolkits.k8s_explorer.toolkit import K8sExplorerToolkit

from langchain.llms.base import BaseLLM
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from langchain.agents.tools import Tool

from tools.git_integrator.tool import GitModel
from tools.gitlab_integration.tool import GitlabModel
from tools.k8s_explorer.tool import KubernetesOpsModel


class K8sEngineerToolkit(BaseToolkit):
    """Toolkit for performing engineering tasks related to kubernetes."""

    git_agent: AgentExecutor
    gitlab_agent: AgentExecutor
    k8s_explorer_agent: AgentExecutor

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        git_agent_tool = Tool(
            name="git_integration_agent",
            func=self.git_agent.run,
            description=GIT_AGENT_DESCRIPTION,
        )
        k8s_explorer_agent_tool = Tool(
            name="k8s_explorer_agent",
            func=self.k8s_explorer_agent.run,
            description=K8S_EXPLORER_AGENT_DESCRIPTION,
        )
        gitlab_agent_tool = Tool(
            name="gitlab_agent",
            func=self.gitlab_agent.run,
            description=GITLAB_AGENT_DESCRIPTION,
        )
        return [git_agent_tool, k8s_explorer_agent_tool, gitlab_agent_tool]

    @classmethod
    def from_llm(
        cls,
        llm: BaseLLM,
        k8s_model: KubernetesOpsModel,
        git_model: GitModel,
        gitlab_model: GitlabModel,
        verbose: bool = False,
        **kwargs: Any,
    ) -> K8sEngineerToolkit:
        """Create a toolkit from an LLM."""
        git_agent = create_git_integration_toolkit(
            llm=llm, toolkit=GitIntegratorToolkit(model=git_model), verbose=verbose, **kwargs)
        k8s_explorer_agent = create_k8s_explorer_agent(
            llm=llm, toolkit=K8sExplorerToolkit(model=k8s_model), verbose=verbose, **kwargs)
        gitlab_agent = create_git_integration_toolkit(
            llm=llm, toolkit=GitlabIntegrationToolkit(model=gitlab_model), verbose=verbose, **kwargs)
        return cls(git_agent=git_agent, k8s_explorer_agent=k8s_explorer_agent, gitlab_agent=gitlab_agent, **kwargs)