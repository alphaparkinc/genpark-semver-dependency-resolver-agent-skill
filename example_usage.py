"""Example usage for SemVer Dependency Resolver Agent."""
from client import SemVerDependencyResolver

available_versions = ["1.0.0", "1.1.2", "1.2.0", "1.2.9", "1.3.0", "2.0.0"]
best_match = SemVerDependencyResolver.resolve_best_version(available_versions, "^1.2.0")
print(f"Best matching version for '^1.2.0': {best_match}")
