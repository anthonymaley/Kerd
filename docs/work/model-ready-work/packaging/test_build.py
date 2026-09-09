import json
from pathlib import Path
import re
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

from build import PACK, SKILLS, build, inputs


class PackageTests(unittest.TestCase):
    def test_relocated_copy_is_exact_and_self_contained(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "a different place" / "kerd"
            count, size = build(destination)
            selected = inputs(PACK)
            self.assertEqual(count, len(selected))
            self.assertEqual(size, sum(p.stat().st_size for p in selected.values()))
            self.assertEqual(sorted(p.name for p in (destination / "skills").iterdir()),
                             sorted(SKILLS))
            for relative, source in selected.items():
                self.assertEqual((destination / relative).read_bytes(), source.read_bytes())
            for path in destination.rglob("*.md"):
                for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                    url = urlsplit(link)
                    if url.scheme or not url.path:
                        continue
                    target = (path.parent / unquote(url.path)).resolve()
                    self.assertTrue(target.is_relative_to(destination.resolve()), (path, link))
                    self.assertTrue(target.exists(), (path, link))
            for host in ("codex", "claude"):
                manifest = json.loads((destination / f".{host}-plugin/plugin.json").read_text())
                self.assertEqual(manifest["name"], destination.name)
                self.assertNotIn("hooks", manifest)
                self.assertNotIn("mcpServers", manifest)
            self.assertFalse((destination / "hooks").exists())
            self.assertFalse((destination / "website").exists())
            self.assertFalse((destination / "trials").exists())

    def test_existing_destination_is_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "kerd"
            destination.mkdir()
            sentinel = destination / "keep.txt"
            sentinel.write_text("user material")
            with self.assertRaises(FileExistsError):
                build(destination)
            self.assertEqual(list(destination.iterdir()), [sentinel])
            self.assertEqual(sentinel.read_text(), "user material")

    def test_wrong_name_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "other"
            with self.assertRaises(ValueError):
                build(destination)
            self.assertFalse(destination.exists())

    def test_symlink_destination_is_not_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "kerd"
            destination.symlink_to(root / "absent", target_is_directory=True)
            with self.assertRaises(FileExistsError):
                build(destination)
            self.assertFalse((root / "absent").exists())

    def test_missing_sources_do_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "kerd"
            with self.assertRaises(ValueError):
                build(destination, pack=root / "missing")
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
