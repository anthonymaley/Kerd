#!/usr/bin/env bash
# Harbor Hours: the first-user round-6 project (batch-1114, first-user-6.md) as it
# stood after sitting 1, commit 4618b2b there: a launch brief written, accepted
# and saved on this computer, with its open questions waiting on the product team.
# No remote, as in the round. Fixed identities and dates keep the commit IDs the
# same from run to run.
#
# The case is sitting 2's shape: the person brings the product team's answers and
# Conductor revises the delivered brief. Round 6 saw 0 of 4 such revisions run
# Switch Out afterwards.
set -euo pipefail
export GIT_AUTHOR_NAME="Sam Rivera" GIT_AUTHOR_EMAIL="sam@harborhours.example"
export GIT_COMMITTER_NAME="Sam Rivera" GIT_COMMITTER_EMAIL="sam@harborhours.example"
at() { export GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1"; }

git init -q -b main .
git config user.name "Sam Rivera"
git config user.email "sam@harborhours.example"
git config commit.gpgsign false

cat > notes.md <<'EOT'
# Harbor Hours: what I know so far

Launch date: 2027-02-10 (tentative)

- Harbor Hours lets small nonprofits log volunteer hours from a phone in under 30 seconds.
- Coordinators get a weekly summary and a one-click report for grant applications.
- Free for up to 25 volunteers; $19/month after that.
- Main competitor: spreadsheets and paper sign-in sheets. Also VolunteerHub (bigger, pricier).
- Pilot: 6 food banks in Ohio, ran Aug-Oct. Average time to log hours dropped from 4 min to 25 s.
- Our CEO wants "the Venmo of volunteer hours" somewhere. I am not sure about that.
EOT

cat > customer-quotes.md <<'EOT'
# Quotes from the pilot

- "I used to spend Sunday night typing up sign-in sheets. Now I don't." (coordinator, Dayton food bank)
- "The grant report saved me a whole afternoon." (director, Toledo)
- "My older volunteers needed one walkthrough, then they were fine." (coordinator, Akron)
- "I wish it did shift scheduling too." (coordinator, Columbus)
EOT

at "2026-11-20T23:10:30-05:00"
git add -A
git commit -q -m "First save"

cat > CONTEXT.md <<'EOT'
# Harbor Hours

Person's preference (2026-11-20): “keep the technical stuff out of my way”.

Harbor Hours is an app that lets small nonprofits log volunteer hours from a phone in under 30 seconds, with a weekly summary and a one-click grant report. Launch is February 2027 (10 February tentative). Product facts live in `notes.md` and `customer-quotes.md`.

## Current

Phase: Launch brief drafted and accepted; open facts waiting on the product team.

The launch brief (`launch-brief.md`) is written and the person accepted this draft on 2026-11-20. It is for sales and comms, to be pasted into a shared Google Doc. Items marked "To confirm" in it are unknowns, not facts. The "Venmo of volunteer hours" idea is deliberately left out. Work notes: `docs/work/launch-brief/work.md`.

Next (selected: agreed as theirs, not Kerd work): the person asks the product team the open questions at the end of the brief. Stops there; updating the brief comes when they bring answers. Proposed alongside: get permission to quote the four pilot coordinators.

Findings that must survive:
- Harbor Hours launch brief accepted 2026-11-20.
- Venmo of volunteer hours line is left out, by the person's call.
- To confirm items must not be stated as fact.
- Person asked to keep technical detail out of the way.

Pickup reading set: this file, `TODO.md` (## Now), `kivna/sessions/2026-11-20.md`, `docs/work/launch-brief/work.md`, `launch-brief.md`.

## For Kerd's next pickup (you can ignore this)

Reading set measured 2026-11-20: about 2,700 tokens (estimate), within the 8,000 target.
read_args: `["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-11-20.md", "--file", "docs/work/launch-brief/work.md", "--file", "launch-brief.md", "--section", "TODO.md", "## Now"]`
EOT

cat > TODO.md <<'EOT'
# To do

## Now

- You: ask the product team the open questions at the end of `launch-brief.md` (date, quote permission, $19 pricing wording, grant report contents, scheduling, privacy and security, sign-up, support, pilot year). Sales and comms shouldn't state any of these as fact until answered.
- You: get permission to quote the four pilot coordinators (Dayton, Toledo, Akron, Columbus) and agree how each is named.
- You: paste `launch-brief.md` into the shared Google Doc for sales and comms (their call on when; the brief says which items are still unconfirmed).
- Update the brief with the product team's answers and remove the "To confirm" marks once you have them (Kerd can do this when you bring the answers).
EOT

mkdir -p docs/work/launch-brief
cat > docs/work/launch-brief/work.md <<'EOT'
# Harbor Hours launch brief

**Stage:** Complete for this draft. **Activity:** none; the person accepted `launch-brief.md` on 2026-11-20.
**Settled:** read in a shared Google Doc, which they paste in themselves, so Markdown text; all defaults below accepted; the "Venmo of volunteer hours" line stays out entirely; message 3 headline is "Free to start", ease of use second.
**Pending question:** none.
**Next action:** the person asks the product team the open items at the end of the brief; then the brief is updated with their answers. Nothing sent or published.
**Not yet approved:** drafting scope as shown; sharing/sending anything.
**How they want it:** "I'm a marketer, not a developer, so please keep the technical stuff out of my way."

## What we're building
- Result: a launch brief for Harbor Hours with positioning, who it's for, three key messages and an FAQ.
- Audience: sales and comms people, who will work from it, so it must be clear.
- Launch: February 2027; notes.md says 2027-02-10, tentative (user-stated).
- Sources: notes.md, customer-quotes.md (both at project root).

## Sourced facts (from notes.md / customer-quotes.md)
- Log volunteer hours from a phone in under 30 seconds; weekly summary and one-click grant report for coordinators.
- Free up to 25 volunteers; $19/month after.
- Competitors: spreadsheets and paper sign-in sheets; VolunteerHub (bigger, pricier).
- Pilot: 6 Ohio food banks, Aug-Oct; average logging time 4 min -> 25 s.
- Four pilot quotes (Dayton, Toledo, Akron, Columbus).

## Open gaps (default Conductor will use)
- Format the brief is read in: asked.
- Date: tentative; default to "February 2027" with the 10th marked tentative.
- "Venmo of volunteer hours" (CEO): user unsure; default leave out of the messages, list it under open questions.
- Quotes: no record they may be quoted publicly; default mark each "confirm permission before use".
- Columbus quote wants shift scheduling: default FAQ answer says scheduling is not part of launch (not confirmed in notes).
- What happens to data/privacy, support, how volunteers sign in: not in notes; default FAQ marks these "to confirm" rather than invent.

## Risks
- Claims beyond the notes (privacy, scheduling, security) could be repeated by sales as fact; handled by marking them to confirm.
EOT

mkdir -p kivna/sessions
cat > kivna/sessions/2026-11-20.md <<'EOT'
# 2026-11-20

## Sitting: Harbor Hours launch brief

- Wrote the launch brief for Harbor Hours from `notes.md` and `customer-quotes.md`: positioning, who it's for, three key messages and a 13-question FAQ. Draft is `launch-brief.md`; the work's own notes are `docs/work/launch-brief/work.md`.
- Format settled: it will be read in a shared Google Doc, which the person pastes in themselves, so the brief is plain text with headings.
- Person's calls: all proposed defaults accepted; the "Venmo of volunteer hours" line stays out of the brief entirely; message 3's headline is "Free to start", with ease of use second.
- The person read the whole draft and accepted it. They will take the open items to the product team themselves.
- Facts not in the notes are marked "To confirm" in the brief so sales and comms don't state them as fact: launch date (10 February tentative), permission to quote the four pilot coordinators, whether $19 a month is flat, what the grant report contains, shift scheduling, privacy and security, sign-up, support, and the pilot year.
- Nothing was sent, shared or published.
EOT

cat > launch-brief.md <<'EOT'
# Harbor Hours: Launch Brief

**Launch:** February 2027 (10 February is tentative)
**For:** Sales and Comms
**Status:** Draft for review. Items marked **[To confirm]** are not in our notes yet, so please don't state them as fact until someone has confirmed them.

---

## 1. Positioning

**One line:** Harbor Hours lets small nonprofits log volunteer hours from a phone in under 30 seconds, and turns those hours into reports they can use for grant applications.

**Positioning statement:** For coordinators at small nonprofits who still track volunteer hours on paper sign-in sheets and spreadsheets, Harbor Hours is the simplest way to record hours and report on them. It takes seconds instead of minutes, and the grant report is one click. Unlike spreadsheets, nothing gets retyped. Unlike VolunteerHub, it's built for small teams and priced for them.

**What we're up against:**
- **Spreadsheets and paper sign-in sheets.** This is the main competitor, because it's what most small nonprofits do today.
- **VolunteerHub.** Bigger and pricier. We win on simplicity and price, not on breadth of features.

**Proof we can use:** In our pilot with 6 food banks in Ohio (August to October), the average time to log hours dropped from 4 minutes to 25 seconds.

---

## 2. Who it's for

**Primary: coordinators and directors at small nonprofits.** They run volunteers, retype sign-in sheets, and write the grant reports. The pilot was with food banks, so that is where our evidence is strongest.

**Also: the volunteers themselves.** They do the logging, so it has to work for people who aren't comfortable with technology. One pilot coordinator said her older volunteers needed one walkthrough and were fine after that.

**Probably not the right fit (our suggestion, please confirm):** large organisations that need a full volunteer management system with every feature. That's VolunteerHub's territory, and we shouldn't compete there.

---

## 3. Three key messages

**1. Logging hours takes seconds, not minutes.**
Volunteers log their hours from a phone in under 30 seconds. In the pilot, the average dropped from 4 minutes to 25 seconds.
> "I used to spend Sunday night typing up sign-in sheets. Now I don't." Coordinator, Dayton food bank

**2. The reporting is done for you.**
Coordinators get a weekly summary automatically, and a one-click report for grant applications.
> "The grant report saved me a whole afternoon." Director, Toledo

**3. Free to start.**
Harbor Hours is free for up to 25 volunteers. After that it's $19 a month. It's also easy enough for volunteers of any age to pick up.
> "My older volunteers needed one walkthrough, then they were fine." Coordinator, Akron

**[Quotes: confirm permission before use.]** We don't have a record that these coordinators agreed to be quoted. Please check before any quote goes into public material, and agree with them how they want to be named.

---

## 4. FAQ

**What is Harbor Hours?**
An app that lets small nonprofits log volunteer hours from a phone in under 30 seconds. Coordinators get a weekly summary and a one-click report for grant applications.

**Who is it for?**
Small nonprofits, especially those still using paper sign-in sheets or spreadsheets. Our pilot was with six food banks in Ohio.

**How much does it cost?**
Free for up to 25 volunteers. After that, $19 a month. **[To confirm: whether $19 is a flat monthly price or depends on the number of volunteers.]**

**How long does it take to log hours?**
Under 30 seconds from a phone. In the pilot, the average was 25 seconds, down from 4 minutes.

**What does the grant report include?**
It's a one-click report for grant applications. A pilot director said it saved her a whole afternoon. **[To confirm: exactly what's in the report and what format it comes in.]**

**Is it hard for volunteers to learn?**
In the pilot, one coordinator said her older volunteers needed one walkthrough and were fine after that.

**How is it different from using a spreadsheet?**
Nothing to retype. Hours are logged once, by the volunteer, and the summaries and reports are generated for the coordinator.

**How is it different from VolunteerHub?**
VolunteerHub is bigger and costs more. Harbor Hours is built to be simple and affordable for small teams.

**Does it do shift scheduling?**
Not at launch. A pilot coordinator asked for it, so we know people want it. **[To confirm: that scheduling isn't in the launch, and whether we can say it's planned.]**

**Is our volunteers' information private and secure?**
**[To confirm.]** Our notes don't cover how data is stored or who can see it. Please get an approved answer before anyone says anything on this.

**Do volunteers need to create an account or download anything?**
**[To confirm.]** Not covered in our notes.

**What support is available?**
**[To confirm.]** Not covered in our notes.

**When does it launch?**
February 2027. **[To confirm: the 10 February date is tentative, so use "February" in anything external until it's firm.]**

---

## Open items before this goes out

1. Confirm the launch date (10 February is tentative).
2. Get permission to quote the four pilot coordinators, and agree how they're named.
3. Confirm the pricing wording ($19 flat or by number of volunteers).
4. Confirm what's in the grant report.
5. Confirm the scheduling answer.
6. Get approved answers on privacy and security, account setup and support.
7. Confirm the pilot year. Our notes say August to October without the year.
EOT

at "2026-11-20T23:15:03-05:00"
git add -A
git commit -q -m "Save the Harbor Hours launch brief and closing notes"
