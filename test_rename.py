"""Smoke tests for rename.py (run: python -m pytest test_rename.py -q
or simply: python test_rename.py)."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rename import build_new_name, main, plan  # noqa: E402


class Args:
    def __init__(self, **kw):
        self.replace = None
        self.lower = False
        self.upper = False
        self.prefix = None
        self.suffix = None
        self.number = False
        self.start = 1
        self.pad = 3
        self.separator = "_"
        self.ext = None
        self.dry_run = False
        self.__dict__.update(kw)


def test_replace_and_prefix():
    args = Args(replace=("IMG_", "trip_"), prefix="2026-")
    assert build_new_name(Path("IMG_01.jpg"), args, 1) == "2026-trip_01.jpg"


def test_numbering_and_extension():
    args = Args(number=True, start=5, pad=2, ext="txt")
    assert build_new_name(Path("notes.md"), args, 5) == "notes_05.txt"


def test_case_and_suffix():
    args = Args(lower=True, suffix="-final")
    assert build_new_name(Path("Report.TXT"), args, 1) == "report-final.TXT"


def test_end_to_end_dry_run_then_real():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "a.txt").write_text("a")
        (d / "b.txt").write_text("b")
        assert main([tmp, "*.txt", "--prefix", "x-", "--dry-run"]) == 0
        assert (d / "a.txt").exists()  # dry run changes nothing
        assert main([tmp, "*.txt", "--prefix", "x-"]) == 0
        assert (d / "x-a.txt").exists() and (d / "x-b.txt").exists()
        assert not (d / "a.txt").exists()


def test_collision_is_skipped():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "a.txt").write_text("a")
        (d / "x-a.txt").write_text("keep me")
        assert main([tmp, "a.txt", "--prefix", "x-"]) == 0
        assert (d / "a.txt").exists()  # not overwritten
        assert (d / "x-a.txt").read_text() == "keep me"


def test_plan_is_sorted():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        for name in ("c.txt", "a.txt", "b.txt"):
            (d / name).write_text("x")
        args = Args(number=True)
        names = [t.name for _, t in plan(d, "*.txt", args)]
        assert names == ["a_001.txt", "b_002.txt", "c_003.txt"]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"{len(tests)} tests passed")
