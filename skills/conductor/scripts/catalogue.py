#!/usr/bin/env python3
"""Find the model profile Conductor should read: shared catalogue first, shipped copy as the floor.

    catalogue.py profile <provider>/<model>     e.g. anthropic/opus-5-5, openai/shared, model-choice

The shared catalogue is the `catalogue` branch of the public repository anthonymaley/Kerd,
laid out like the shipped skills/conductor/references/guidance/ (guidance/<provider>/<model>.md).
Order of use:
  1. a cached copy no older than 7 days            -> source "cache"
  2. a fresh fetch (HTTP 200, UTF-8, non-empty, under 200 KB, in the shape below),
     written to the cache atomically                -> source "catalogue"
  3. on any fetch failure, an older cached copy     -> source "stale-cache", with a reason
  4. else the profile shipped with Kerd             -> source "shipped", with a reason
  5. else exit 1 naming the gap.
Prints one JSON object: {"path": <absolute file to read>, "source": ..., "reason": null | sentence}.

Environment:
  KERD_CATALOGUE_CACHE    cache directory (default ~/.cache/kerd/catalogue)
  KERD_CATALOGUE_URL      catalogue base URL; "guidance/<name>.md" is appended
                          (default https://raw.githubusercontent.com/anthonymaley/Kerd/catalogue)
  KERD_CATALOGUE_OFFLINE  "1" uses the shipped profile and touches neither network nor cache

A name is one or two segments of letters, digits, "." and "-", not starting with "."
(lowercase for profiles; "README" is the one capitalised file the guidance holds). An
optional trailing ".md" is ignored. Anything else exits 2 before any file or URL is touched.

Shape, decided by the name: a <provider>/<model> profile must open with YAML frontmatter
(a "---" line, a closing "---" line, and `provider:` and `applicable_models:` keys inside);
a one-segment document such as README or model-choice must open with a "#" heading.
The same check applies to a cached copy before it is used.
Standard library only.
"""

import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_URL = "https://raw.githubusercontent.com/anthonymaley/Kerd/catalogue"
FRESH_SECONDS = 7 * 24 * 60 * 60
TIMEOUT_SECONDS = 5
SIZE_LIMIT = 200 * 1024  # bytes; a body must be strictly under this
SHIPPED_ROOT = Path(__file__).resolve().parents[1] / "references" / "guidance"
SEGMENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9.-]*")
FRONTMATTER_KEYS = ("provider", "applicable_models")


class Refused(Exception):
    """The name is not one this script will turn into a path or URL (exit 2)."""


class Gap(Exception):
    """No catalogue, cache or shipped copy exists for the name (exit 1)."""


def parse_name(raw):
    name = raw[:-3] if raw.endswith(".md") else raw
    parts = name.split("/")
    if not 1 <= len(parts) <= 2 or not all(SEGMENT.fullmatch(p) and ".." not in p for p in parts):
        raise Refused(
            f"refused: {raw!r} is not a profile name; use <provider>/<model> such as "
            "anthropic/opus-5-5, with letters, digits, '.' and '-' only")
    return "/".join(parts)


def frontmatter_gap(lines):
    """Return None when lines open with profile frontmatter, else what is wrong with it."""
    if not lines or lines[0].strip() != "---":
        return "the profile did not open with YAML frontmatter"
    closing = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if closing is None:
        return "the profile's frontmatter was never closed"
    block = lines[1:closing]
    for key in FRONTMATTER_KEYS:
        if not any(re.fullmatch(rf"\s*{key}:(\s.*)?", line) for line in block):
            return f"the profile's frontmatter had no {key}"
    return None


def valid_body(data, name):
    """Return (text, None) when the bytes have the shape the name calls for, else (None, reason)."""
    if not data:
        return None, "the body was empty"
    if len(data) >= SIZE_LIMIT:
        return None, "the body was 200 KB or larger"
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None, "the body was not UTF-8"
    lines = text.lstrip("\ufeff").splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if "/" in name:
        gap = frontmatter_gap(lines)
        if gap:
            return None, gap
    elif not lines or not lines[0].lstrip().startswith("#"):
        return None, "the document did not start with a Markdown heading"
    return text, None


def fetch(url, name):
    """Return (bytes, None) on an accepted response, else (None, reason)."""
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            status = getattr(response, "status", None) or response.getcode()
            if status != 200:
                return None, f"the catalogue answered HTTP {status}"
            data = response.read(SIZE_LIMIT)
    except urllib.error.HTTPError as error:
        error.close()
        return None, f"the catalogue answered HTTP {error.code}"
    except urllib.error.URLError as error:
        return None, f"the catalogue could not be reached ({error.reason})"
    except Exception as error:  # timeouts, resets, malformed responses
        return None, f"the catalogue could not be read ({type(error).__name__})"
    text, reason = valid_body(data, name)
    if text is None:
        return None, reason
    return data, None


def write_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=".catalogue-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.replace(temp, path)
    except BaseException:
        try:
            os.unlink(temp)
        except FileNotFoundError:
            pass
        raise


def cached(path, name):
    """Return the cache file's age in seconds when it holds a valid profile, else None."""
    try:
        if not path.is_file() or path.is_symlink():
            return None
        data = path.read_bytes()
        age = time.time() - path.stat().st_mtime
    except OSError:
        return None
    text, _ = valid_body(data, name)
    return None if text is None else max(age, 0)


def shipped(name, why):
    """Use the shipped profile; `why` is a lowercase clause saying why the catalogue was not used."""
    path = SHIPPED_ROOT / f"{name}.md"
    if path.is_file():
        return {"path": str(path), "source": "shipped",
                "reason": f"{why[0].upper() + why[1:]}, so this is the profile shipped with Kerd."}
    raise Gap(f"no profile for {name}: {why}, and Kerd ships none at {path}")


def resolve(raw, environ=None):
    environ = os.environ if environ is None else environ
    name = parse_name(raw)
    if environ.get("KERD_CATALOGUE_OFFLINE") == "1":
        return shipped(name, "KERD_CATALOGUE_OFFLINE=1 is set")

    cache_root = Path(environ.get("KERD_CATALOGUE_CACHE")
                      or Path.home() / ".cache" / "kerd" / "catalogue")
    cache_file = cache_root / "guidance" / f"{name}.md"
    age = cached(cache_file, name)
    if age is not None and age <= FRESH_SECONDS:
        return {"path": str(cache_file.resolve()), "source": "cache", "reason": None}

    base = (environ.get("KERD_CATALOGUE_URL") or DEFAULT_URL).rstrip("/")
    url = f"{base}/guidance/{urllib.parse.quote(name)}.md"
    data, failure = fetch(url, name)
    if data is not None:
        try:
            write_atomic(cache_file, data)
            return {"path": str(cache_file.resolve()), "source": "catalogue", "reason": None}
        except OSError as error:
            failure = f"the fetched copy could not be cached ({error.strerror or error})"

    if age is not None:
        days = int(age // 86400)
        return {"path": str(cache_file.resolve()), "source": "stale-cache",
                "reason": f"{failure[0].upper() + failure[1:]}, so this is a cached copy "
                          f"{days} days old."}
    return shipped(name, failure)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2 or argv[0] != "profile":
        print("usage: catalogue.py profile <provider>/<model>", file=sys.stderr)
        return 2
    try:
        result = resolve(argv[1])
    except Refused as error:
        print(str(error), file=sys.stderr)
        return 2
    except Gap as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
