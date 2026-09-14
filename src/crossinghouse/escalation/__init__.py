"""Bounded retry and escalation decisions."""

from crossinghouse.escalation.policy import EscalationAction, EscalationDecision, decide

__all__ = ["EscalationAction", "EscalationDecision", "decide"]
