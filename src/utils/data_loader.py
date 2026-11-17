"""Load and validate the DigitalWell resource catalogue."""

from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

REQUIRED_COLUMNS = [
    "id", "name", "category", "description", "problem", "platforms", "cost",
    "privacy", "accessibility", "limitations", "official_url", "source_reference",
    "verified_on", "advantages",
]
NOT_STATED = "Not stated in reviewed source"


def is_valid_http_url(value: object) -> bool:
    """Return whether a value is an absolute HTTP(S) URL with a host."""
    if not isinstance(value, str):
        return False
    try:
        parsed = urlparse(value.strip())
        return parsed.scheme.lower() in {"http", "https"} and bool(parsed.netloc) and "." in parsed.hostname
    except (ValueError, TypeError):
        return False


def load_resources(path: str | Path) -> pd.DataFrame:
    """Load every CSV row; annotate invalid data instead of silently dropping it.

    Missing optional text is made explicit. Missing schema columns raise a
    ValueError so the dataset problem is visible to the caller.
    """
    path = Path(path)
    try:
        frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError:
        frame = pd.DataFrame(columns=REQUIRED_COLUMNS)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"Resource CSV is missing required columns: {', '.join(missing_columns)}")
    frame = frame[REQUIRED_COLUMNS].copy()
    for column in REQUIRED_COLUMNS:
        frame[column] = frame[column].astype("string").str.strip()
    for column in REQUIRED_COLUMNS:
        if column not in {"id", "name", "official_url", "source_reference"}:
            frame[column] = frame[column].replace("", NOT_STATED)
    frame["url_valid"] = frame["official_url"].map(is_valid_http_url)
    frame["duplicate_id"] = frame["id"].duplicated(keep=False) & frame["id"].ne("")
    errors = []
    for _, row in frame.iterrows():
        row_errors = []
        if not row["id"]: row_errors.append("missing id")
        if not row["name"]: row_errors.append("missing name")
        if not row["official_url"]: row_errors.append("missing official URL")
        elif not row["url_valid"]: row_errors.append("malformed official URL")
        if not row["source_reference"]: row_errors.append("missing source reference")
        if row["duplicate_id"]: row_errors.append("duplicate resource id")
        errors.append("; ".join(row_errors))
    frame["validation_errors"] = errors
    return frame


def filter_resources(frame: pd.DataFrame, query: str = "", category: str = "All", platform: str = "All") -> pd.DataFrame:
    """Filter resources by name/description/problem, category and platform."""
    result = frame.copy()
    if query.strip():
        searchable = result[["name", "description", "problem"]].fillna("").astype(str)
        mask = searchable.apply(lambda column: column.str.contains(query.strip(), case=False, regex=False)).any(axis=1)
        result = result[mask]
    if category != "All":
        result = result[result["category"] == category]
    if platform != "All":
        result = result[result["platforms"].astype(str).str.contains(platform, case=False, regex=False)]
    return result
