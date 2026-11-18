"""Build Codex app-server turn/start overrides in the trusted submitting client."""


def speed_override(*, urgent, new_turn, inherited_tier, service_tiers, manual_choice=False):
    """An empty mapping inherits the user's selection, including unknown tiers.

    Pass the resolved inherited tier, including any manual per-turn choice.
    Only call after validating the accepted user event and session state.
    """
    if manual_choice or not urgent or not new_turn or inherited_tier != "default":
        return {}
    for tier in service_tiers or ():
        if tier.get("id") in ("priority", "fast") and tier.get("name", "").casefold() == "fast":
            return {"serviceTierForTurn": tier["id"]}
    return {}
