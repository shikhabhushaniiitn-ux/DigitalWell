from pathlib import Path

import pandas as pd
import pytest

from src.utils.data_loader import REQUIRED_COLUMNS, filter_resources, is_valid_http_url, load_resources


def write_csv(path: Path, rows: list[dict]) -> Path:
    pd.DataFrame(rows, columns=REQUIRED_COLUMNS).to_csv(path, index=False)
    return path


def sample(**overrides):
    row = {column: "Example text" for column in REQUIRED_COLUMNS}
    row.update(id="one", name="Focus App", category="Focus", platforms="Android, Web",
               official_url="https://example.org", source_reference="https://example.org/source", verified_on="2026-11-11")
    row.update(overrides)
    return row


def test_loads_csv_and_required_fields(tmp_path):
    frame = load_resources(write_csv(tmp_path / "resources.csv", [sample()]))
    assert len(frame) == 1
    assert all(column in frame.columns for column in REQUIRED_COLUMNS)
    assert frame.loc[0, "url_valid"]
    assert frame.loc[0, "validation_errors"] == ""


def test_missing_values_are_explicit(tmp_path):
    row = sample(description="", privacy="")
    frame = load_resources(write_csv(tmp_path / "resources.csv", [row]))
    assert frame.loc[0, "description"] == "Not stated in reviewed source"
    assert frame.loc[0, "privacy"] == "Not stated in reviewed source"


def test_duplicate_ids_are_flagged_and_preserved(tmp_path):
    frame = load_resources(write_csv(tmp_path / "resources.csv", [sample(), sample(name="Second")]))
    assert len(frame) == 2
    assert frame["duplicate_id"].all()
    assert frame["validation_errors"].str.contains("duplicate resource id").all()


def test_filtering_by_query_category_and_platform(tmp_path):
    rows = [sample(), sample(id="two", name="Privacy Guide", category="Privacy", platforms="Web")]
    frame = load_resources(write_csv(tmp_path / "resources.csv", rows))
    assert len(filter_resources(frame, query="focus")) == 1
    assert len(filter_resources(frame, category="Privacy")) == 1
    assert len(filter_resources(frame, platform="Android")) == 1


def test_empty_dataset_is_safe(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    frame = load_resources(path)
    assert frame.empty
    assert len(filter_resources(frame)) == 0


@pytest.mark.parametrize("url,expected", [
    ("https://example.org/page", True), ("http://localhost", False),
    ("javascript:alert(1)", False), ("not a url", False), ("", False),
])
def test_url_validation(url, expected):
    assert is_valid_http_url(url) is expected


def test_malformed_resource_url_is_preserved_and_flagged(tmp_path):
    frame = load_resources(write_csv(tmp_path / "bad.csv", [sample(official_url="javascript:alert(1)")]))
    assert len(frame) == 1
    assert not frame.loc[0, "url_valid"]
    assert "malformed official URL" in frame.loc[0, "validation_errors"]


def test_missing_required_schema_column_raises(tmp_path):
    path = tmp_path / "bad-schema.csv"
    path.write_text("id,name\none,Example\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required columns"):
        load_resources(path)
