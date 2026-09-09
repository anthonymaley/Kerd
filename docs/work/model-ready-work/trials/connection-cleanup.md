# Connection cleanup observation — 2026-09-08

During the model-selection/adoption update, the fake-provider suite produced a
concrete intermittent failure. This narrows the open reliability question; it
does not prove the cause of Claude's earlier unrecorded one-in-six error.
No real model jobs were launched. Runtime code was not changed.

## Observed

On macOS with Python 3.14.7:

- First full run: 33 pass, one failure; 34 tests in 31.839 seconds.
- Failing test: `test_timeout_optional_and_local_logs_private` expected
  `timed_out`, received `interrupted`.
- Second full run: 34/34 pass in 32.077 seconds, without a runtime change.
- A targeted series returned `timed_out` 20/20 times.
- A second targeted series, bounded at 150 attempts, stopped on the 103rd
  attempt when it captured the same unexpected status and its cleanup cause.

Captured call path and result (private IDs and temporary paths omitted):

```text
Bridge.run: communicate(timeout=0.2) -> subprocess.TimeoutExpired
Bridge.stop: os.killpg(proc.pid, 0)
PermissionError: [Errno 1] Operation not permitted

status: interrupted
error: Process cleanup could not be confirmed; session reuse blocked
cleanup_error: [Errno 1] Operation not permitted
exit_code: -15
```

The targeted probe used the existing `TransportTests` setup and fake CLI, with
`prompt="SLEEP", timeout=0.1`. It wrapped `Bridge.stop` only to print the actual
exception traceback, re-raised it unchanged, and did not alter process handling.
Temporary test repositories were removed by their existing cleanup mechanism.

## Interpretation and remaining work

The immediate cause is observed: a process-group existence probe was denied
after termination was requested. The leader's exit code does not prove all
descendants stopped. `stop_and_collect` deliberately preserves this uncertainty
and blocks reuse. Treating permission denial as an absent process group would
weaken that protection; no such runtime change was made.

Why this host intermittently denies the probe is not established. A race around
leader/group exit or host restrictions is a hypothesis, not a finding. Daily-use
cleanup reliability remains open. The timeout assertion now includes the full
fake-provider result on failure so future failures retain the diagnostic fields;
its expected status and pass/fail behavior are unchanged.
After that diagnostic-only change, the final full suite passed 34/34 in 32.001
seconds. This does not resolve the captured intermittent OS denial.

Next investigation: capture the denied probe together with contemporaneous
owned-process lifecycle evidence and host restrictions. Any platform-specific
correction must still distinguish a genuinely gone group from permission-denied
survivors, retain the failure state and verify no duplicate work can start.
Do not replace this evidence with a later green run or label the old review's
unknown error fixed.

## Follow-on correction — 2026-09-08

After the user's “okay lets do it”, a minimal owned-process experiment ran 350
short-lived Python workers. It sent TERM to each owned group, reaped the leader
while probing with signal zero, and retried observation for at most half a second.
118 runs produced a permission-denied probe; all 118 subsequently produced
ProcessLookupError, confirming disappearance. All 350 workers were reaped.
This demonstrates a transient observation in this environment, not its kernel cause.

The runtime correction stays inside the existing three-second stop grace period:
retry a denied existence probe, return on confirmed disappearance, and retain the
denial if disappearance is not confirmed before the deadline. After a denial it
does not escalate to another termination signal. An initially denied TERM still
fails immediately. No extra service, permission or configurable limit was added.
The normal no-denial force-stop path is otherwise unchanged.

Three regression tests cover denied-then-gone, denial without disappearance
(including a later readable-but-live group), and denied termination itself.
They were run against the old implementation first: the recovery case errored,
and both bounded-recheck subcases failed. After the correction all three pass;
the full connection suite passes 37/37 in 32.006 seconds. Existing tests still
check that cleanup uncertainty is saved and prevents session reuse.

The meaning of permission denial versus an absent group is supported by
[Apple's killpg manual](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/killpg.2.html).
The manual does not explain the observed transient denial. The narrow correction
is not a claim of universal process containment or a fix for every earlier
unrecorded test failure. Historical observations above remain intact.

Post-change checks: 150/150 real fake-provider timeout requests returned
`timed_out`; all 190 Switch tests pass in 34.900 seconds. These are local checks,
not paid provider jobs or a cross-machine/process-security guarantee. Conductor's
skill validation passes, and the changed runtime/tests match the candidate mirror.
Skill Creator kept the correction and its tests within the existing helper;
no additional setup machinery or global setting was introduced.
