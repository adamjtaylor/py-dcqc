import hashlib
from pathlib import Path

from dcqc.target import SingleTarget
from dcqc.tests.base_test import InternalBaseTest, TestStatus, TestTier


class Md5ChecksumTest(InternalBaseTest):
    """Tests if a file has the expected MD5 checksum."""

    tier = TestTier.FILE_INTEGRITY
    target: SingleTarget

    def compute_status(self) -> TestStatus:
        path = self.target.file.stage()
        expected_md5 = self.target.file.get_metadata("md5_checksum")
        actual_md5 = self._compute_md5_checksum(path)
        if expected_md5 == actual_md5:
            status = TestStatus.PASS
        else:
            status = TestStatus.FAIL
            self.status_reason = "Computed MD5 checksum does not match provided value"
        return status

    def _compute_md5_checksum(self, path: Path) -> str:
        hash_md5 = hashlib.md5()
        with path.open("rb") as infile:
            for chunk in iter(lambda: infile.read(4096), b""):
                hash_md5.update(chunk)
        actual_md5 = hash_md5.hexdigest()
        return actual_md5
