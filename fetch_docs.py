from dataclasses import dataclass
from subprocess import Popen
import sys
import tempfile
from pathlib import Path
import shutil


@dataclass
class DocumentationSource:
    repo_address: str
    repo_docs_path: Path
    local_docs_path: Path


def report(message: str):
    print(f"🔨 {message}", file=sys.stderr)

def clone_git_repo(address: str, destination: Path):
    report(f"Cloning from {address} into {destination}")
    Popen([
        "git",
        "clone",
        address,
        destination,
    ]).communicate()

def fetch_documentation_from_dir(documentation_path: Path, target_path: Path):
    report(f"Cloning docs from {documentation_path} to {target_path}")
    shutil.copytree(documentation_path, target_path, dirs_exist_ok=True)

def main():
    SOURCES = [
        DocumentationSource(
            "git@github.com:Mazurel/Modbus.git",
            Path("docs/html/"),
            Path("docs/modbus/")
        )
    ]

    for source in SOURCES:
        report(f"Loading docs from: {source}")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            clone_git_repo(source.repo_address, tmpdir_path)
            fetch_documentation_from_dir(tmpdir_path / source.repo_docs_path, source.local_docs_path)

if __name__ == "__main__":
    main()
