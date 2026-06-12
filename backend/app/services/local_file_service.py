from pathlib import Path

SEARCH_ROOTS = [
    Path.home() / "Documents",
    Path.home() / "Downloads",
    Path.home() / "Desktop",
]

# Common noisy/system folders to skip
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".cache",
    "AppData", "$RECYCLE.BIN", "System Volume Information",
}


def search_files(query: str) -> list[str]:
    matches = []
    query_lower = query.lower().strip()

    if not query_lower:
        return []

    for root in SEARCH_ROOTS:
        if not root.exists():
            continue

        try:
            for file in root.rglob("*"):
                # Skip directories in the skip list
                if any(part in SKIP_DIRS for part in file.parts):
                    continue

                if not file.is_file():
                    continue

                if query_lower in file.name.lower():
                    matches.append(str(file))

        except (PermissionError, OSError):
            continue

    return matches[:20]
