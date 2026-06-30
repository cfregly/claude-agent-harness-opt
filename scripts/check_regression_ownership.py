#!/usr/bin/env python3
"""Validate source files have explicit regression-test ownership."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = "claude_agent_harness_opt"
SCRIPTS_DIR = "scripts"
TESTS_DIR = "tests"

PACKAGE_OWNER_OVERRIDES = {
    "__init__.py": ("tests/test_check_package_surface_script.py",),
    "__main__.py": ("tests/test_check_package_surface_script.py", "tests/test_cli.py"),
}

SCRIPT_OWNER_OVERRIDES = {
    "build_gstack_skill_target.py": ("tests/test_build_gstack_skill_target_script.py",),
    "deslop_check.py": ("tests/test_deslop_check_script.py",),
    "live_sdk_smoke.py": ("tests/test_live_sdk_smoke_script.py",),
    "optimize_mcp.py": ("tests/test_optimize_mcp_script.py",),
    "probe_service_keys.py": ("tests/test_probe_service_keys_script.py",),
    "sdk_surface_inventory.py": ("tests/test_sdk_surface_inventory_script.py",),
}


def main() -> int:
    failures = check_regression_ownership()
    if failures:
        print("\n".join(sorted(failures)))
        return 1
    print("regression ownership check passed")
    return 0


def check_regression_ownership(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    failures.extend(_check_package_modules(root))
    failures.extend(_check_scripts(root))
    return failures


def _check_package_modules(root: Path) -> list[str]:
    package_root = root / PACKAGE_DIR
    if not package_root.is_dir():
        return [f"{PACKAGE_DIR}: missing"]

    failures: list[str] = []
    for path in sorted(package_root.glob("*.py")):
        rel = path.relative_to(root).as_posix()
        owners = PACKAGE_OWNER_OVERRIDES.get(path.name, (f"tests/test_{path.stem}.py",))
        failures.extend(_check_owner_paths(root, rel, owners))
    return failures


def _check_scripts(root: Path) -> list[str]:
    scripts_root = root / SCRIPTS_DIR
    if not scripts_root.is_dir():
        return [f"{SCRIPTS_DIR}: missing"]

    failures: list[str] = []
    for path in sorted(scripts_root.glob("*.py")):
        rel = path.relative_to(root).as_posix()
        owners = _script_owners(path.name)
        if owners is None:
            failures.append(f"{rel}: missing regression owner mapping")
            continue
        failures.extend(_check_owner_paths(root, rel, owners))
    return failures


def _script_owners(filename: str) -> tuple[str, ...] | None:
    if filename in SCRIPT_OWNER_OVERRIDES:
        return SCRIPT_OWNER_OVERRIDES[filename]
    if filename.startswith("check_"):
        stem = filename.removesuffix(".py")
        return (f"tests/test_{stem}_script.py",)
    return None


def _check_owner_paths(root: Path, source: str, owners: tuple[str, ...]) -> list[str]:
    failures: list[str] = []
    for owner in owners:
        path = root / owner
        if not path.is_file():
            failures.append(f"{source}: missing regression owner {owner}")
            continue
        if path.stat().st_size == 0:
            failures.append(f"{source}: regression owner is empty: {owner}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
