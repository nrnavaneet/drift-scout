## Operations Guide

This document captures the minimum operational runbook for Drift Scout. It is
intentionally incomplete in a few areas to introduce realistic ambiguity for
the Ambiguous Coding Task project. When extending the system, clarify the gaps
below with your stakeholder.

### Daily Workflow
1. CI job exports the active infrastructure inventory into JSON.
2. `drift-scout scan configs/baseline.yaml -i inventory.json --history state.json`
   runs as part of the post-deploy step.
3. If drift is detected, Slack notifications alert the owning team. They choose
   whether to remediate or accept the drift by updating the baseline hash.

### On-Call Expectations
- A human needs to acknowledge alerts within 15 minutes for `critical` services.
- The severity normalization between numeric and textual scales is still under
  debate. For now, pagers should trigger for `critical` and numeric levels `>=4`.
- If the Azure DevOps integration is enabled (pending security review), the
  runbook will auto-open work items. This document does not yet describe the
  item format—coordinate with the platform guild before enabling it.

### Known Gaps
- Email/ticketing delivery is not implemented even though configuration allows
  specifying recipients and labels.
- Multiple cron formats are accepted, but the SRE team expects second-level
  precision for some services. Decide whether to enforce 6-field cron or support
  a custom scheduler extension.
- Baseline metadata may include both numeric and textual drift thresholds, but
  only textual severity currently influences reporting.

