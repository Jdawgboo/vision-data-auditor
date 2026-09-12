import tempfile
import unittest
from pathlib import Path

from vision_data_auditor import audit


class VisionAuditTests(unittest.TestCase):
    def test_detects_duplicate_content_and_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.bin").write_bytes(b"same")
            (root / "b.bin").write_bytes(b"same")
            report = audit([{"path": "a.bin", "label": "cat"}, {"path": "b.bin", "label": "dog"}, {"path": "missing.bin", "label": "cat"}], root)
        self.assertEqual(report.missing_files, ("missing.bin",))
        self.assertEqual(len(report.duplicate_groups), 1)
        self.assertEqual(report.class_counts, {"cat": 2, "dog": 1})


if __name__ == "__main__":
    unittest.main()
