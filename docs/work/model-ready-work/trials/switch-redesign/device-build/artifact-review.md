# Laptop result — independent assessment

## Outcome

The returned work and focused correction pass the bounded M1–M4 review. This is
an assessment of the artifact, not producer acceptance of the entire Switch
redesign or permission to install it. The laptop's submitted version had one real
formatting gap; it was corrected on Studio and independently rechecked.

| Evidence | Observed result |
| --- | --- |
| Submitted patch at exact handoff `6393778c4993405ffec17616ab3950821e9d7795` | Applies to only the three assigned deliverables; 31 tests pass |
| Original handoff tests against corrected implementation | 19 pass; old validation/text/JSON function ASTs unchanged |
| Corrected retained artifact | 33 tests pass |
| Submitted synthetic GitHub GFM rendering | Two tables, nine rows, three unintended anchors inside cells |
| Corrected rendering of the same fixture | Two tables, nine rows, no active elements inside cells |
| Independent reviewer recheck | Repeated 33 current + 19 baseline tests; inspected HTML and regenerated matching Markdown; no remaining M1–M4 blocker |

## Finding and correction

Bare URLs and email addresses became clickable links in table cells. The laptop's
tests covered explicit Markdown punctuation, not automatic linking. The controller
reproduced the problem with synthetic example.com labels using GitHub's anonymous
Markdown API, without repository context, authentication or project/user content.
This external render was controller review evidence, not a network operation by
the bounded laptop worker or a dependency of the shipped test suite.

The correction escapes colons/periods as character references and displays email
`@` as `\u0040`. An encoded `&#64;` alone still allowed GitHub to link an email;
the visible escape avoids that behaviour. Literal backslash-u text remains distinct.
Two regression tests cover automatic-link candidates and this distinction.
The extra escaping affects Markdown only. Usage describes the representation and
the limits; the retained fixture does not establish safety for every renderer or
repository-specific link transformation.

M1 is supported by the original tests and unchanged function bodies, not the
overbroad claim that one byte-identical example proves all behaviour. M2 is
supported after correction. M3's inspected private-field and invalid-input cases
pass. M4 now includes retained renderer evidence and honest compatibility limits.
Minimum Python 3.10 execution remains untested.

## Files and reproduction

- [Original submitted patch](submitted.patch), SHA-256
  `a42a4154a1db4279259de5c7b351f774a9f3c9713ea49e22e1e714a53f4a40b8`.
  This matches the user-owned root patch, which remains untouched.
- [Reviewed artifact and usage](reviewed-artifact/USAGE.md), with the original
  unchanged example alongside its three deliverables.
- [Submitted render](submitted-render.json) and [corrected render](corrected-render.json)
  contain the synthetic input, Markdown, returned HTML and response date.
- [Render probe](review_probe.py) reproduces those checks; `--github` explicitly
  sends the synthetic fixture to the [GitHub Markdown API](https://docs.github.com/en/rest/markdown/markdown).
- [Baseline verifier](verify_baseline.py) reads the exact handoff's original 19
  tests from a clone and runs them against the supplied artifact without changing
  checkout files. It also compares pre-existing function ASTs.

From this folder:

```sh
(cd reviewed-artifact && python3 -m unittest -q)
python3 verify_baseline.py /path/to/clone-containing-handoff reviewed-artifact
```

Optional live external render, which refreshes the retained corrected observation:

```sh
python3 review_probe.py reviewed-artifact --label corrected --github
```

The independent reviewer ran read-only, without network or dependencies; its
assessment checked the retained actual HTML rather than claiming a second live
renderer call. Both laptop-reported alternative-renderer runs remain reported
evidence, not retained reproducible fixtures. They were not rerun after correction.

## Handoff conclusion

Studio's source save/release evidence, the supplied laptop transcript and the
returned working artifact support the bounded continuity trial. The user opened
the fresh laptop session and carried its result back. No automatic remote startup,
native conversation transfer or measured pickup token reduction is claimed.

No commit/push, source-branch advancement, live project edit or installation was
performed during this review. The laptop still holds its submitted version; the
reviewed correction is retained locally in this pack.
