"""SemVer Dependency Resolver Agent.
100% Python Standard Library.
"""
import re

class SemVerDependencyResolver:
    """Semantic Versioning 2.0.0 range matcher & dependency resolver."""

    @staticmethod
    def parse_version(v_str: str) -> tuple:
        v_clean = v_str.strip().lstrip("v")
        m = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+([0-9A-Za-z.-]+))?$', v_clean)
        if not m:
            raise ValueError(f"Invalid SemVer string: {v_str}")
        major, minor, patch, prerelease, build = m.groups()
        return (int(major), int(minor), int(patch), prerelease or "")

    @classmethod
    def satisfies(cls, version_str: str, constraint: str) -> bool:
        v = cls.parse_version(version_str)
        c = constraint.strip()

        if c in ("*", "latest"):
            return True

        if c.startswith("^"):
            base_v = cls.parse_version(c[1:])
            next_major = base_v[0] + 1
            return v >= base_v and v < (next_major, 0, 0, "")

        if c.startswith("~"):
            base_v = cls.parse_version(c[1:])
            next_minor = base_v[1] + 1
            return v >= base_v and v < (base_v[0], next_minor, 0, "")

        if c.startswith("==") or not any(c.startswith(op) for op in [">=", "<=", ">", "<"]):
            target = c.lstrip("=").strip()
            return v[:3] == cls.parse_version(target)[:3]

        if c.startswith(">="):
            return v >= cls.parse_version(c[2:].strip())
        if c.startswith("<="):
            return v <= cls.parse_version(c[2:].strip())
        if c.startswith(">"):
            return v > cls.parse_version(c[1:].strip())
        if c.startswith("<"):
            return v < cls.parse_version(c[1:].strip())

        return False

    @classmethod
    def resolve_best_version(cls, versions: list, constraint: str) -> str:
        valid_candidates = []
        for v in versions:
            try:
                if cls.satisfies(v, constraint):
                    valid_candidates.append(v)
            except Exception:
                continue

        if not valid_candidates:
            return None

        valid_candidates.sort(key=cls.parse_version, reverse=True)
        return valid_candidates[0]
