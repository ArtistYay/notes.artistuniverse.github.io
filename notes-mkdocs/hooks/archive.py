"""
archive.py - MkDocs hook that automatically moves pages last edited more than
ARCHIVE_THRESHOLD_DAYS ago into an "Archive" nav section at build time.

Pages are still fully searchable and appear on the Tags page.
The last-modified date is taken from git log (falls back to file mtime).
"""

import os
import subprocess
from datetime import datetime, timedelta

# Pages not edited within this many days get archived
ARCHIVE_THRESHOLD_DAYS = 365

# Nav entries to never archive (e.g. index pages, tags page)
NEVER_ARCHIVE = {"index.md", "tags.md"}


def _git_last_modified(filepath: str) -> datetime | None:
    """Return the date of the last git commit that touched this file."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", filepath],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=os.path.dirname(filepath),
        )
        ts = result.stdout.strip()
        if ts:
            return datetime.fromtimestamp(int(ts))
    except Exception:
        pass
    return None


def _file_last_modified(filepath: str) -> datetime | None:
    """Fallback: return the OS file modification time."""
    try:
        return datetime.fromtimestamp(os.path.getmtime(filepath))
    except Exception:
        return None


def _is_stale(rel_path: str, docs_dir: str) -> bool:
    """Return True if the file hasn't been touched in ARCHIVE_THRESHOLD_DAYS."""
    if rel_path in NEVER_ARCHIVE:
        return False
    full_path = os.path.join(docs_dir, rel_path)
    last_modified = _git_last_modified(full_path) or _file_last_modified(full_path)
    if last_modified is None:
        return False
    cutoff = datetime.now() - timedelta(days=ARCHIVE_THRESHOLD_DAYS)
    return last_modified < cutoff


def _collect_pages(nav_item) -> list[tuple[str, str]]:
    """
    Recursively walk a nav structure and return a flat list of
    (rel_path, title) for every leaf page entry.
    """
    pages = []
    if isinstance(nav_item, dict):
        for title, value in nav_item.items():
            if isinstance(value, str):
                pages.append((value, title))
            elif isinstance(value, list):
                for child in value:
                    pages.extend(_collect_pages(child))
    elif isinstance(nav_item, list):
        for child in nav_item:
            pages.extend(_collect_pages(child))
    return pages


def _remove_page(nav, rel_path: str) -> tuple[list, str | None]:
    """
    Remove a leaf page from the nav tree.
    Returns (updated_nav, title_of_removed_page | None).
    Empty section lists are pruned automatically.
    """
    if not isinstance(nav, list):
        return nav, None

    new_nav = []
    found_title = None

    for item in nav:
        if not isinstance(item, dict):
            new_nav.append(item)
            continue

        new_item = {}
        for key, value in item.items():
            if isinstance(value, str):
                if value == rel_path:
                    found_title = key  # skip — this is the page we're removing
                else:
                    new_item[key] = value
            elif isinstance(value, list):
                updated_list, ft = _remove_page(value, rel_path)
                if ft:
                    found_title = ft
                if updated_list:          # only keep section if it still has children
                    new_item[key] = updated_list
            else:
                new_item[key] = value

        if new_item:
            new_nav.append(new_item)

    return new_nav, found_title


def on_config(config):
    nav = config.get("nav")
    if not nav:
        return config

    docs_dir = config["docs_dir"]

    # Find every page in the nav
    all_pages = _collect_pages(nav)

    archive_entries: list[dict] = []
    current_nav = list(nav)

    for rel_path, title in all_pages:
        if _is_stale(rel_path, docs_dir):
            current_nav, removed_title = _remove_page(current_nav, rel_path)
            archive_entries.append({removed_title or title: rel_path})

    if archive_entries:
        current_nav.append({"Archive": archive_entries})

    config["nav"] = current_nav
    return config
