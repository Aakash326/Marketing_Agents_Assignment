"""
AutoGen-based 6-Agent Trading Analysis System

This module contains specialized trading agents built using Microsoft's AutoGen AgentChat framework.
Each agent focuses on a specific aspect of investment analysis.
"""

from .research_agent import create_organiser_agent
from .risk_manager import create_risk_manager
from .data_analyst import create_data_analyst
from .quantitative_analyst import create_quantitative_analyst
from .strategy_developer import create_strategy_developer
from .report_agent import create_report_agent

__all__ = [
    'create_organiser_agent',
    'create_risk_manager',
    'create_data_analyst',
    'create_quantitative_analyst',
    'create_strategy_developer',
    'create_report_agent'
]
