#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from itertools import zip_longest
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised by the 3.10 test matrix.
    tomllib = None
    TOMLDecodeError = ValueError
else:
    TOMLDecodeError = tomllib.TOMLDecodeError

BUNDLE_MINIMUM_VERSIONS = {
    "lmterminal": "0.0.44",
    "shellgenius": "0.2.0",
}
BUNDLE_METADATA_FILES = ("pyproject.toml", "uv.lock")

_VERSION_PATTERN = re.compile(
    r"^(?P<release>\d+(?:\.\d+)*)"
    r"(?:(?P<pre_label>a|b|rc)(?P<pre_number>\d+)?)?"
    r"(?:\.?post(?P<post_number>\d+))?$"
)
_PRE_RELEASE_ORDER = {"a": 0, "b": 1, "rc": 2}


def run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )


def base_ref_exists(
    repo_root: Path,
    base_ref: str,
    git_runner=run_git,
) -> bool:
    result = git_runner(repo_root, "rev-parse", "--verify", "--quiet", base_ref)
    return result.returncode == 0


def metadata_files_dirty(repo_root: Path, git_runner=run_git) -> bool:
    status = git_runner(repo_root, "status", "--short", "--", *BUNDLE_METADATA_FILES)
    if status.returncode != 0:
        raise RuntimeError(status.stderr.strip() or status.stdout.strip() or "git status failed")
    return bool(status.stdout.strip())


def bundle_metadata_changed(repo_root: Path, base_ref: str, git_runner=run_git) -> bool:
    committed_changes = False
    if base_ref_exists(repo_root, base_ref, git_runner=git_runner):
        diff = git_runner(
            repo_root,
            "diff",
            "--name-only",
            f"{base_ref}...HEAD",
            "--",
            *BUNDLE_METADATA_FILES,
        )
        if diff.returncode != 0:
            raise RuntimeError(diff.stderr.strip() or diff.stdout.strip() or "git diff failed")
        committed_changes = bool(diff.stdout.strip())
    else:
        # Without the comparison ref we cannot reliably detect committed branch changes.
        # Fail closed so dependency checks are never skipped silently.
        committed_changes = True

    return committed_changes or metadata_files_dirty(repo_root, git_runner=git_runner)


def load_locked_versions(lock_path: Path) -> dict[str, str]:
    if tomllib is None:
        raise RuntimeError("Python 3.11+ is required to parse `uv.lock`")
    with lock_path.open("rb") as handle:
        lock_data = tomllib.load(handle)
    return {package["name"]: package["version"] for package in lock_data["package"]}


def _parse_version(version: str) -> tuple[tuple[int, ...], tuple[int, int] | None, int | None]:
    match = _VERSION_PATTERN.fullmatch(version.strip())
    if match is None:
        raise ValueError(f"Unsupported version format: {version!r}")

    release = [int(part) for part in match.group("release").split(".")]
    while len(release) > 1 and release[-1] == 0:
        release.pop()

    pre_label = match.group("pre_label")
    pre_number = match.group("pre_number")
    pre = (
        None
        if pre_label is None
        else (_PRE_RELEASE_ORDER[pre_label], int(pre_number) if pre_number is not None else 0)
    )

    post_number = match.group("post_number")
    post = int(post_number) if post_number is not None else None
    return tuple(release), pre, post


def _compare_versions(left: str, right: str) -> int:
    left_release, left_pre, left_post = _parse_version(left)
    right_release, right_pre, right_post = _parse_version(right)

    for left_part, right_part in zip_longest(left_release, right_release, fillvalue=0):
        if left_part < right_part:
            return -1
        if left_part > right_part:
            return 1

    if left_pre is None and right_pre is not None:
        return 1
    if left_pre is not None and right_pre is None:
        return -1
    if left_pre is not None and right_pre is not None:
        if left_pre < right_pre:
            return -1
        if left_pre > right_pre:
            return 1

    left_post_value = -1 if left_post is None else left_post
    right_post_value = -1 if right_post is None else right_post
    if left_post_value < right_post_value:
        return -1
    if left_post_value > right_post_value:
        return 1
    return 0


def find_resolution_errors(locked_versions: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for package_name, minimum_version in BUNDLE_MINIMUM_VERSIONS.items():
        resolved_version = locked_versions.get(package_name)
        if resolved_version is None:
            errors.append(f"{package_name} is missing from uv.lock")
            continue
        if _compare_versions(resolved_version, minimum_version) < 0:
            errors.append(
                f"{package_name} resolved to {resolved_version}, below the declared minimum {minimum_version}"
            )
    return errors


def check_lock_current(repo_root: Path) -> None:
    result = subprocess.run(
        ["uv", "lock", "--check"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return

    detail = result.stderr.strip() or result.stdout.strip() or "`uv lock --check` failed"
    raise RuntimeError(f"`uv.lock` is out of date with `pyproject.toml`: {detail}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail fast when bundled CLI resolution drifts below declared minimum versions."
    )
    parser.add_argument(
        "--base-ref",
        default="origin/main",
        help="Git ref used to decide whether dependency metadata changed.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Run the guard even when dependency metadata is unchanged.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path(__file__).resolve().parents[1]

    try:
        should_run = args.force or bundle_metadata_changed(repo_root, args.base_ref)
        if not should_run:
            print(f"Skipping bundle guard; `pyproject.toml` and `uv.lock` match {args.base_ref}.")
            return 0

        check_lock_current(repo_root)
        errors = find_resolution_errors(load_locked_versions(repo_root / "uv.lock"))
    except (OSError, KeyError, RuntimeError, ValueError, TOMLDecodeError) as error:
        print(f"Bundle guard failed: {error}", file=sys.stderr)
        return 1

    if errors:
        print("Bundle guard failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("Bundle guard passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
