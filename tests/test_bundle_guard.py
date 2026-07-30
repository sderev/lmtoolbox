from __future__ import annotations

import builtins
import importlib.util
import subprocess
import sys
from pathlib import Path


def load_bundle_guard_module(module_name: str = "bundle_guard"):
    module_path = Path(__file__).resolve().parents[1] / ".ci" / "bundle_guard.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


bundle_guard = load_bundle_guard_module()


def test_bundle_metadata_changed_uses_base_ref_diff(tmp_path):
    calls = []

    def fake_run_git(_repo_root, *args):
        calls.append(args)
        if args[:3] == ("rev-parse", "--verify", "--quiet"):
            return subprocess.CompletedProcess(args, 0, "", "")
        if args[0] == "diff":
            return subprocess.CompletedProcess(args, 0, "pyproject.toml\n", "")
        return subprocess.CompletedProcess(args, 0, "", "")

    changed = bundle_guard.bundle_metadata_changed(
        tmp_path,
        "origin/main",
        git_runner=fake_run_git,
    )

    assert changed is True
    assert calls[1] == (
        "diff",
        "--name-only",
        "origin/main...HEAD",
        "--",
        "pyproject.toml",
        "uv.lock",
    )


def test_bundle_metadata_changed_runs_conservatively_without_base_ref(tmp_path):
    calls = []

    def fake_run_git(_repo_root, *args):
        calls.append(args)
        if args[:3] == ("rev-parse", "--verify", "--quiet"):
            return subprocess.CompletedProcess(args, 1, "", "")
        return subprocess.CompletedProcess(args, 0, "", "")

    changed = bundle_guard.bundle_metadata_changed(
        tmp_path,
        "origin/main",
        git_runner=fake_run_git,
    )

    assert changed is True
    assert calls == [("rev-parse", "--verify", "--quiet", "origin/main")]


def test_bundle_metadata_changed_includes_dirty_worktree_with_base_ref(tmp_path):
    def fake_run_git(_repo_root, *args):
        if args[:3] == ("rev-parse", "--verify", "--quiet"):
            return subprocess.CompletedProcess(args, 0, "", "")
        if args[0] == "diff":
            return subprocess.CompletedProcess(args, 0, "", "")
        return subprocess.CompletedProcess(args, 0, " M pyproject.toml\n", "")

    changed = bundle_guard.bundle_metadata_changed(
        tmp_path,
        "origin/main",
        git_runner=fake_run_git,
    )

    assert changed is True


def test_bundle_metadata_changed_includes_staged_index_with_base_ref(tmp_path):
    def fake_run_git(_repo_root, *args):
        if args[:3] == ("rev-parse", "--verify", "--quiet"):
            return subprocess.CompletedProcess(args, 0, "", "")
        if args[0] == "diff":
            return subprocess.CompletedProcess(args, 0, "", "")
        return subprocess.CompletedProcess(args, 0, "M  pyproject.toml\n", "")

    changed = bundle_guard.bundle_metadata_changed(
        tmp_path,
        "origin/main",
        git_runner=fake_run_git,
    )

    assert changed is True


def test_bundle_metadata_changed_returns_false_without_committed_or_dirty_changes(tmp_path):
    def fake_run_git(_repo_root, *args):
        if args[:3] == ("rev-parse", "--verify", "--quiet"):
            return subprocess.CompletedProcess(args, 0, "", "")
        return subprocess.CompletedProcess(args, 0, "", "")

    changed = bundle_guard.bundle_metadata_changed(
        tmp_path,
        "origin/main",
        git_runner=fake_run_git,
    )

    assert changed is False


def test_find_resolution_errors_reports_stale_bundle_versions():
    errors = bundle_guard.find_resolution_errors(
        {
            "lmterminal": "0.0.44",
            "shellgenius": "0.1.9",
            "vocabmaster": "0.1.11",
        }
    )

    assert errors == [
        "shellgenius resolved to 0.1.9, below the declared minimum 0.2.0",
    ]


def test_bundle_guard_imports_without_packaging_or_setuptools(monkeypatch):
    original_import = builtins.__import__

    for module_name in list(sys.modules):
        if module_name == "packaging" or module_name.startswith("packaging."):
            monkeypatch.delitem(sys.modules, module_name, raising=False)
        if module_name == "setuptools" or module_name.startswith("setuptools."):
            monkeypatch.delitem(sys.modules, module_name, raising=False)

    def failing_import(name, globals=None, locals=None, fromlist=(), level=0):  # noqa: A002
        if name == "packaging" or name.startswith("packaging."):
            raise ModuleNotFoundError(f"No module named {name!r}")
        if name == "setuptools" or name.startswith("setuptools."):
            raise ModuleNotFoundError(f"No module named {name!r}")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", failing_import)
    module = load_bundle_guard_module("bundle_guard_without_packaging")

    errors = module.find_resolution_errors(
        {
            "lmterminal": "0.0.44",
            "shellgenius": "0.2.0",
            "vocabmaster": "0.1.11",
        }
    )

    assert errors == []


def test_find_resolution_errors_accepts_declared_bundle_minimums():
    errors = bundle_guard.find_resolution_errors(
        {
            "lmterminal": "0.0.44",
            "shellgenius": "0.2.0",
            "vocabmaster": "0.1.11",
        }
    )

    assert errors == []


def test_find_resolution_errors_accepts_normalized_equivalent_versions():
    errors = bundle_guard.find_resolution_errors(
        {
            "lmterminal": "0.0.44.0",
            "shellgenius": "0.2",
            "vocabmaster": "0.1.11",
        }
    )

    assert errors == []


def test_find_resolution_errors_rejects_prerelease_below_minimum():
    errors = bundle_guard.find_resolution_errors(
        {
            "lmterminal": "0.0.44",
            "shellgenius": "0.2.0rc1",
            "vocabmaster": "0.1.11",
        }
    )

    assert errors == [
        "shellgenius resolved to 0.2.0rc1, below the declared minimum 0.2.0",
    ]


def test_find_resolution_errors_accepts_postrelease_above_minimum():
    errors = bundle_guard.find_resolution_errors(
        {
            "lmterminal": "0.0.44.post1",
            "shellgenius": "0.2.0.post1",
            "vocabmaster": "0.1.11",
        }
    )

    assert errors == []


def test_find_resolution_errors_does_not_apply_a_declared_minimum_to_vocabmaster():
    errors = bundle_guard.find_resolution_errors(
        {
            "lmterminal": "0.0.44",
            "shellgenius": "0.2.0",
            "vocabmaster": "0.0.1",
        }
    )

    assert errors == []


def test_main_skips_when_dependency_metadata_is_unchanged(monkeypatch, capsys):
    monkeypatch.setattr(bundle_guard, "bundle_metadata_changed", lambda *_args, **_kwargs: False)

    exit_code = bundle_guard.main(["--base-ref", "origin/main"])

    assert exit_code == 0
    assert (
        capsys.readouterr().out
        == "Skipping bundle guard; `pyproject.toml` and `uv.lock` match origin/main.\n"
    )


def test_main_reports_resolution_errors(monkeypatch, capsys):
    monkeypatch.setattr(bundle_guard, "bundle_metadata_changed", lambda *_args, **_kwargs: True)
    monkeypatch.setattr(bundle_guard, "check_lock_current", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        bundle_guard,
        "load_locked_versions",
        lambda _path: {
            "lmterminal": "0.0.44",
            "shellgenius": "0.1.9",
            "vocabmaster": "0.3.0",
        },
    )

    exit_code = bundle_guard.main(["--force"])

    assert exit_code == 1
    assert capsys.readouterr().err == (
        "Bundle guard failed:\n  - shellgenius resolved to 0.1.9, below the declared minimum 0.2.0\n"
    )


def test_gate_runs_bundle_guard_with_uv_managed_python():
    gate_path = Path(__file__).resolve().parents[1] / ".ci" / "gate"
    gate_script = gate_path.read_text()

    assert (
        "uv run --python 3.11 --managed-python --no-project .ci/bundle_guard.py "
        '"${bundle_guard_args[@]}"' in gate_script
    )
    assert 'python3.11 .ci/bundle_guard.py "${bundle_guard_args[@]}"' not in gate_script
