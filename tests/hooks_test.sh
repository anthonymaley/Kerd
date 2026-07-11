#!/bin/bash
# Kerd hooks test harness
#
# Exercises the three session-boundary hooks (session-start.sh, stop.sh,
# skill-complete.sh) against the failure classes that have actually bitten us:
#
#   - Path resolution: the hook must degrade SILENTLY (exit 0, no stderr) when
#     CLAUDE_PROJECT_DIR is unset or empty — i.e. when the ${CLAUDE_PLUGIN_ROOT}/
#     env-var wiring did not resolve. This is the v0.29.1 regression class: a
#     hook that crashes instead of staying quiet leaks errors into every session.
#   - Missing-file branches: no .git, no kivna/, no TODO.md, no .active-modes.
#   - Behind-remote branch: local HEAD behind its upstream tracking ref.
#   - SessionStart staleness report: last-session date + interrupted mode output.
#
# Pure bash 3.2 (macOS system bash). No external deps beyond git and coreutils.
# Run:  bash tests/hooks_test.sh
# Exit: 0 if all green, 1 if any test fails.

# Test and helper functions are dispatched indirectly (see the runner at the
# bottom: `declare -F | grep '^test_'`), so shellcheck's static "never invoked"
# check can't see the calls. The directive must precede the first command to
# apply file-wide.
# shellcheck disable=SC2329
set -uo pipefail   # NOT -e: we run every test and tally failures.

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$SCRIPT_DIR/.." && pwd)
HOOKS="$REPO/hooks"

PASS=0
FAIL=0
FAILURES=""   # newline-separated "name: reason"

# Deterministic, config-free git so tests don't depend on the user's ~/.gitconfig.
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=test@example.com
export GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=test@example.com
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null

# --- assertion helpers -------------------------------------------------------
# Each test sets TNAME, then calls assertions. A failed assertion records the
# reason and short-circuits the rest of that test via the `return 1` the caller
# propagates with `|| return`.

fail() {  # reason
  FAIL=$((FAIL + 1))
  FAILURES+="  ✗ $TNAME: $1"$'\n'
  printf '  \033[31m✗\033[0m %s\n     %s\n' "$TNAME" "$1"
  return 1
}

pass() {
  PASS=$((PASS + 1))
  printf '  \033[32m✓\033[0m %s\n' "$TNAME"
}

assert_exit() {  # expected actual
  [ "$1" = "$2" ] || fail "expected exit $1, got $2"
}

assert_empty() {  # value label
  [ -z "$1" ] || fail "$2 should be empty, got: $(printf '%q' "$1")"
}

assert_contains() {  # haystack needle
  case "$1" in
    *"$2"*) return 0 ;;
    *) fail "expected to contain «$2», got: $(printf '%q' "$1")" ;;
  esac
}

assert_matches() {  # value extended-regex label
  if printf '%s' "$1" | grep -Eq "$2"; then return 0; fi
  fail "$3: «$1» did not match /$2/"
}

# Run a hook with a given project dir and optional stdin; capture stdout, stderr,
# and exit code into globals OUT / ERR / RC. Pass project dir as $1 ("UNSET" to
# leave CLAUDE_PROJECT_DIR unset), hook filename as $2, optional stdin as $3.
run_hook() {  # projectdir hookfile [stdin]
  local pdir="$1" hook="$2" stdin="${3:-}"
  local errfile; errfile=$(mktemp)
  if [ "$pdir" = "UNSET" ]; then
    OUT=$(printf '%s' "$stdin" | env -u CLAUDE_PROJECT_DIR bash "$HOOKS/$hook" 2>"$errfile")
  else
    OUT=$(printf '%s' "$stdin" | CLAUDE_PROJECT_DIR="$pdir" bash "$HOOKS/$hook" 2>"$errfile")
  fi
  RC=$?
  ERR=$(cat "$errfile")
  rm -f "$errfile"
}

# Make a fresh temp dir that looks like a Kerd repo (git + kivna). Echoes path.
make_kerd_repo() {
  local d; d=$(mktemp -d)
  ( cd "$d" && git init -q && mkdir kivna && git commit -q --allow-empty -m init ) >/dev/null 2>&1
  echo "$d"
}

# --- path-resolution tests (the v0.29.1 regression class) --------------------

test_session_start_unset_projectdir_is_silent() {
  TNAME="session-start: unset CLAUDE_PROJECT_DIR exits silently"
  run_hook UNSET session-start.sh
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  assert_empty "$ERR" stderr || return
  pass
}

test_session_start_empty_projectdir_is_silent() {
  TNAME="session-start: empty CLAUDE_PROJECT_DIR exits silently"
  run_hook "" session-start.sh
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  assert_empty "$ERR" stderr || return
  pass
}

test_stop_unset_projectdir_is_silent() {
  TNAME="stop: unset CLAUDE_PROJECT_DIR exits silently"
  run_hook UNSET stop.sh
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  assert_empty "$ERR" stderr || return
  pass
}

test_skill_complete_unset_projectdir_is_silent() {
  TNAME="skill-complete: unset CLAUDE_PROJECT_DIR exits silently"
  run_hook UNSET skill-complete.sh '{"tool_response":{"success":true}}'
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  assert_empty "$ERR" stderr || return
  pass
}

test_template_references_existing_executable_scripts() {
  # ${CLAUDE_PLUGIN_ROOT}/hooks/X.sh must resolve to a real, runnable script.
  # If a referenced path is wrong, the hook silently never runs — exactly the
  # class of bug that left hooks dead after the path rewrite.
  TNAME="template: every referenced hook script exists and is executable"
  local tmpl="$HOOKS/hooks.template.json" refs missing=""
  # The literal ${CLAUDE_PLUGIN_ROOT}/ is the prefix we strip — not a var to expand.
  # shellcheck disable=SC2016
  refs=$(grep -oE '\$\{CLAUDE_PLUGIN_ROOT\}/hooks/[A-Za-z0-9._-]+\.sh' "$tmpl" \
           | sed 's#${CLAUDE_PLUGIN_ROOT}/##' | sort -u)
  [ -n "$refs" ] || { fail "no hook script references found in template"; return; }
  local rel
  while IFS= read -r rel; do
    [ -f "$REPO/$rel" ] || missing+="$rel(absent) "
    [ -x "$REPO/$rel" ] || missing+="$rel(not-exec) "
  done <<EOF
$refs
EOF
  assert_empty "$missing" "missing/non-exec scripts" || return
  pass
}

test_hooks_invokable_by_absolute_path() {
  # The recommended wiring uses an absolute path. A valid-but-non-Kerd dir must
  # still exit 0 silently (structure guards), proving absolute invocation works.
  TNAME="session-start: absolute-path invocation on non-Kerd dir is silent"
  local d; d=$(mktemp -d)
  OUT=$(CLAUDE_PROJECT_DIR="$d" bash "$HOOKS/session-start.sh" 2>/dev/null); RC=$?
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  pass
}

# --- missing-file branches ---------------------------------------------------

test_session_start_non_git_dir_silent() {
  TNAME="session-start: dir without .git exits silently"
  local d; d=$(mktemp -d)
  run_hook "$d" session-start.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  pass
}

test_session_start_no_kivna_silent() {
  TNAME="session-start: git repo without kivna/ exits silently"
  local d; d=$(mktemp -d)
  ( cd "$d" && git init -q ) >/dev/null 2>&1
  run_hook "$d" session-start.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  pass
}

test_session_start_no_todo_no_modes_silent() {
  TNAME="session-start: Kerd repo, no TODO/modes/remote -> silent"
  local d; d=$(make_kerd_repo)
  run_hook "$d" session-start.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  pass
}

test_stop_clean_tree_silent() {
  TNAME="stop: clean tree with no active mode -> silent"
  local d; d=$(make_kerd_repo)
  run_hook "$d" stop.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  pass
}

test_skill_complete_no_active_modes_silent() {
  TNAME="skill-complete: no .active-modes -> silent"
  local d; d=$(make_kerd_repo)
  run_hook "$d" skill-complete.sh '{"tool_input":{"skill":"kerd:conductor"},"tool_response":{"success":true}}'
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  pass
}

# --- behind-remote branch ----------------------------------------------------

test_session_start_behind_remote_reports() {
  # Offline 3-state setup: real remote at C, local tracking ref at B, local HEAD
  # at A. This is the only state where the hook's behind-detection fires: the
  # dry-run shows '->' (C is fetchable) AND HEAD..@{u} > 0 (HEAD behind B).
  TNAME="session-start: behind upstream -> reports + suggests switch in"
  local base remote up clone
  base=$(mktemp -d); remote="$base/remote.git"; up="$base/up"; clone="$base/clone"
  git init --bare -q "$remote"
  git clone -q "$remote" "$up" 2>/dev/null
  ( cd "$up" && git checkout -q -b main && echo A >f && git add f && git commit -qm A && git push -q -u origin main ) >/dev/null 2>&1
  git clone -q "$remote" "$clone" 2>/dev/null
  ( cd "$up" && echo B >f && git commit -qam B && git push -q ) >/dev/null 2>&1
  ( cd "$clone" && git fetch -q ) >/dev/null 2>&1          # tracking ref -> B, HEAD stays A
  ( cd "$up" && echo C >f && git commit -qam C && git push -q ) >/dev/null 2>&1
  mkdir "$clone/kivna"
  run_hook "$clone" session-start.sh
  rm -rf "$base"
  assert_exit 0 "$RC" || return
  assert_matches "$OUT" 'behind remote \([0-9]+ commits\)' "behind message" || return
  assert_contains "$OUT" "Run /switch in" || return
  pass
}

# --- SessionStart staleness report -------------------------------------------

test_session_start_last_session_date() {
  TNAME="session-start: newest session log -> '📋 Last session: <date>'"
  local d; d=$(make_kerd_repo)
  mkdir -p "$d/kivna/sessions"
  printf '# Session 2026-06-20\n' >"$d/kivna/sessions/2026-06-20.md"
  printf '# Session 2026-06-25\n' >"$d/kivna/sessions/2026-06-25.md"
  run_hook "$d" session-start.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_contains "$OUT" "Last session: 2026-06-25" || return
  # No remote, no mode -> no "switch in" suggestion appended.
  case "$OUT" in *"Run /switch in"*) fail "unexpected switch-in suggestion: $OUT"; return ;; esac
  pass
}

test_session_start_mode_interrupted() {
  TNAME="session-start: active mode -> 'mode interrupted' + suggestion"
  local d; d=$(make_kerd_repo)
  printf 'mode: greenfield (step 4 of 9)\n' >"$d/kivna/.active-modes"
  run_hook "$d" session-start.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  # First/only message is capitalized by the report builder -> "Mode interrupted".
  assert_contains "$OUT" "Mode interrupted: greenfield (step 4 of 9)" || return
  assert_contains "$OUT" "Run /switch in" || return
  pass
}

test_session_start_combined_report() {
  TNAME="session-start: date + mode compose into one report line"
  local d; d=$(make_kerd_repo)
  mkdir -p "$d/kivna/sessions"
  printf '# Session 2026-06-25\n' >"$d/kivna/sessions/2026-06-25.md"
  printf 'mode: writing (step 2 of 5)\n' >"$d/kivna/.active-modes"
  run_hook "$d" session-start.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_contains "$OUT" "📋 Last session: 2026-06-25" || return
  assert_contains "$OUT" "mode interrupted: writing (step 2 of 5)" || return
  pass
}

# --- stop hook reporting -----------------------------------------------------

test_stop_uncommitted_reports() {
  TNAME="stop: uncommitted change -> warns + suggests switch out"
  local d; d=$(make_kerd_repo)
  echo dirty >"$d/newfile.txt"
  run_hook "$d" stop.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_contains "$OUT" "uncommitted changes detected" || return
  assert_contains "$OUT" "Run /switch out" || return
  pass
}

test_stop_active_mode_and_conductor_report() {
  TNAME="stop: active mode + conductor lines both reported"
  local d; d=$(make_kerd_repo)
  printf 'mode: research (step 1 of 4)\nconductor: orient\n' >"$d/kivna/.active-modes"
  run_hook "$d" stop.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_contains "$OUT" "mode active: research (step 1 of 4)" || return
  assert_contains "$OUT" "conductor: orient" || return
  pass
}

# --- skill-complete progress -------------------------------------------------

# Shared .active-modes fixture: step 2 current, step 3 pending.
write_modes_fixture() {  # dir
  cat >"$1/kivna/.active-modes" <<'EOF'
mode: greenfield (step 2 of 9)
  instruction: focus on pricing
1: /kerd:switch in | load context [done]
2: /kerd:conductor orient | frame the work [current]
3: /kerd:brainstorm | explore options [pending]
EOF
}

test_skill_complete_matching_step_reports_progress() {
  TNAME="skill-complete: completed skill matches current step -> progress"
  local d; d=$(make_kerd_repo)
  write_modes_fixture "$d"
  run_hook "$d" skill-complete.sh \
    '{"tool_input":{"skill":"kerd:conductor","args":"orient"},"tool_response":{"success":true}}'
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_contains "$OUT" "Step complete: /kerd:conductor orient" || return
  assert_contains "$OUT" "Instruction: focus on pricing" || return
  # next_skill keeps its leading slash (unlike current_command, which strips it).
  assert_contains "$OUT" "Next: step 3 — /kerd:brainstorm (explore options)" || return
  pass
}

test_skill_complete_nonmatching_step_silent() {
  TNAME="skill-complete: skill != current step -> silent"
  local d; d=$(make_kerd_repo)
  write_modes_fixture "$d"
  run_hook "$d" skill-complete.sh \
    '{"tool_input":{"skill":"kerd:slainte"},"tool_response":{"success":true}}'
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  pass
}

test_skill_complete_unsuccessful_skill_silent() {
  TNAME="skill-complete: success=false -> silent"
  local d; d=$(make_kerd_repo)
  write_modes_fixture "$d"
  run_hook "$d" skill-complete.sh \
    '{"tool_input":{"skill":"kerd:conductor","args":"orient"},"tool_response":{"success":false}}'
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  pass
}

# --- lint gate ---------------------------------------------------------------

test_shellcheck_clean() {
  TNAME="shellcheck: all hook scripts clean"
  if ! command -v shellcheck >/dev/null 2>&1; then
    printf '  \033[33m-\033[0m %s (shellcheck not installed — skipped)\n' "$TNAME"
    return 0
  fi
  local out
  out=$(shellcheck "$HOOKS/session-start.sh" "$HOOKS/stop.sh" "$HOOKS/skill-complete.sh" "$HOOKS/pair.sh" 2>&1)
  if [ -n "$out" ]; then
    fail "shellcheck reported issues:"$'\n'"$out"
    return
  fi
  pass
}

# --- pair mode (UserPromptSubmit) --------------------------------------------

test_pair_unset_projectdir_is_silent() {
  TNAME="pair:unset CLAUDE_PROJECT_DIR exits silently"
  run_hook UNSET pair.sh
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  assert_empty "$ERR" stderr || return
  pass
}

test_pair_empty_projectdir_is_silent() {
  TNAME="pair:empty CLAUDE_PROJECT_DIR exits silently"
  run_hook "" pair.sh
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  assert_empty "$ERR" stderr || return
  pass
}

test_pair_no_flag_file_silent() {
  TNAME="pair:no kivna/.pair -> silent"
  local d; d=$(make_kerd_repo)
  run_hook "$d" pair.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  pass
}

test_pair_off_silent() {
  TNAME="pair:flag = off -> silent"
  local d; d=$(make_kerd_repo)
  echo "off" > "$d/kivna/.pair"
  run_hook "$d" pair.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_empty "$OUT" stdout || return
  pass
}

test_pair_on_injects_partner_mode() {
  TNAME="pair:flag = on -> injects partner-mode reminder"
  local d; d=$(make_kerd_repo)
  echo "on" > "$d/kivna/.pair"
  run_hook "$d" pair.sh
  rm -rf "$d"
  assert_exit 0 "$RC" || return
  assert_contains "$OUT" "Partner mode" || return
  assert_contains "$OUT" "ask ONE question" || return
  assert_contains "$OUT" "multiple choice only when it clarifies" || return
  pass
}

# --- runner ------------------------------------------------------------------

printf '\nKerd hooks test harness\n=======================\n'
for t in $(declare -F | awk '{print $3}' | grep '^test_' | sort); do
  "$t"
done

printf '\n-----------------------\n'
printf 'Passed: %d   Failed: %d\n' "$PASS" "$FAIL"
if [ "$FAIL" -gt 0 ]; then
  printf '\nFailures:\n%s\n' "$FAILURES"
  exit 1
fi
printf 'All green.\n'
exit 0
