# Connecting a Codex app-server client

This optional Python module belongs in a client that constructs `turn/start` requests. Installing the portable skill in the desktop app loads Markdown instructions. To use native Fast in that app, use its speed picker. Desktop installation does not run Python.

In a custom client, use the active model's `serviceTiers` from `model/list`. Resolve the user's inherited speed using the host. Track the urgent state separately for each conversation at the trusted user-input entry. The reference reducer and its event contract are in the delivery guide at the repository root.

```python
from adapters.codex_speed import speed_override

# turn_params is the client's existing turn/start payload.
# A user's explicit per-turn choice, including Standard, always wins.
override = speed_override(
    urgent=session.mode == "ON",
    new_turn=starting_new_turn,
    inherited_tier=resolved_thread_tier,
    service_tiers=active_model.get("serviceTiers", []),
    manual_choice=user_selected_speed or "serviceTierForTurn" in turn_params,
)
payload = {**turn_params, **override}
```

Build a fresh payload for each turn. An empty override preserves the current selection. Steering an in-flight turn, ending urgent mode, starting a separate session, or receiving an unknown tier generates no automatic override. Pass the correct session and its latest accepted state before sending. Log the requested tier separately from any actual serving-tier receipt. A completed turn alone does not prove a billing rate or a speedup.
