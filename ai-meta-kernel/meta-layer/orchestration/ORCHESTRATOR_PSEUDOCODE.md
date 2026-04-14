# Orchestrator Pseudocode

Source of truth: `../../META_LAYER_MASTER_SPEC.md`.

```text
function run_meta_cognitive_kernel(raw_request):
    intake = normalize(raw_request)

    frame = frame_objective(intake)
    if frame.core_goal_is_unclear:
        return emit_status("needs_reframe", frame)

    classification = classify_task(frame)
    risk = calibrate_risk(frame, classification)

    triggers = select_habits(classification, risk, frame)
    structure = decompose(frame)

    required_checks = determine_required_checks(
        classification,
        risk,
        triggers,
        structure
    )

    module_outputs = []
    for habit in triggers:
        module_outputs.append(
            run_habit_module(habit, frame, structure, risk)
        )

    challenge = run_challenge_loop(
        frame,
        structure,
        module_outputs,
        risk,
        required_checks
    )

    gates = apply_decision_gates(
        frame,
        classification,
        triggers,
        structure,
        required_checks,
        challenge,
        risk
    )

    status_flags = derive_status_flags(gates, risk, challenge)
    downstream_recommendation = route_downstream(
        classification,
        triggers,
        status_flags,
        risk
    )

    if gates.block_unrestricted_handoff:
        downstream_recommendation.mode = "restricted_handoff"

    if gates.block_all_handoff:
        downstream_recommendation.mode = "do_not_handoff"

    task_object = emit_task_object(
        raw_request,
        frame,
        classification,
        risk,
        triggers,
        structure,
        required_checks,
        status_flags,
        downstream_recommendation,
        challenge
    )

    return task_object
```
