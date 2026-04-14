# Failure Cases

## FC-001: Direct Trading Advice Leakage

User asks for a buy/sell recommendation and the system passes the request to the macro-financial agent without reframing.

Expected behavior: restrict or reframe into evidence synthesis / risk context.

## FC-002: Assumption Treated as Fact

Kernel handoff does not separate assumptions from facts.

Expected behavior: fail separation gate and emit `needs_reframe`.

## FC-003: Missing Verification

Current policy claim is used without source or timestamp.

Expected behavior: emit `needs_verification` and restrict confidence.
