# Kerd model catalogue

This branch holds the model profiles Kerd's Conductor reads (`guidance/`) and the retry list (`retry.md`).
A scheduled job updates it weekly by pull request, Codex reviews each clause against its cited page, and the owner merges.
The plugin reads it through `skills/conductor/scripts/catalogue.py` on `main`, falling back to its shipped profiles.
