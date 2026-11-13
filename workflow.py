"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    missing = sorted(name for name, passed in data['checks'].items() if passed is not True)
    assessment = await agent.ask('readiness', 'Summarize readiness from these checks. Do not claim production readiness if a required check is false.', data,
                                 'The rollback plan is missing; this prototype is not ready for production release.')
    return {'ready': not missing, 'missing_checks': missing, 'assessment': assessment,
            'configured_limits': {'max_turns': agent.max_turns, 'timeout_seconds': agent.timeout, 'budget_usd': agent.budget}, 'deployed': False}
