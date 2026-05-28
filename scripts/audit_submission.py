#!/usr/bin/env python3
"""Audit a Kaggle submission CSV for the 3LC Multi Vehicle Detection Challenge.

This script is read-only: it validates a candidate submission against the
authoritative sample_submission.csv and optionally against local test images.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EXPECTED_COLUMNS = ["id", "image_id", "prediction_string"]
CLASS_NAMES = {
    0: "truck",
    1: "car",
    2: "van",
    3: "bus",
}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
INT_RE = re.compile(r"^(0|[1-9][0-9]*)$")


@dataclass
class Finding:
    level: str
    message: str
    row_number: int | None = None
    image_id: str | None = None

    def format(self) -> str:
        prefix = self.level.upper()
        location = []
        if self.row_number is not None:
            location.append(f"row={self.row_number}")
        if self.image_id is not None:
            location.append(f"image_id={self.image_id}")
        if location:
            return f"{prefix}: {' '.join(location)}: {self.message}"
        return f"{prefix}: {self.message}"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")
        rows = [dict(row) for row in reader]
        return list(reader.fieldnames), rows


def duplicate_values(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for value in values:
        if value in seen:
            dupes.add(value)
        seen.add(value)
    return sorted(dupes)


def parse_float(token: str) -> float:
    value = float(token)
    if not math.isfinite(value):
        raise ValueError("not finite")
    return value


def validate_prediction_string(
    raw_value: str | None,
    row_number: int,
    image_id: str,
    strict_bbox_inside: bool,
) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    box_count = 0

    if raw_value is None:
        return [
            Finding("error", "prediction_string is missing", row_number, image_id)
        ], box_count

    value = raw_value.strip()
    if "\n" in raw_value or "\r" in raw_value:
        findings.append(
            Finding("error", "prediction_string contains a line break", row_number, image_id)
        )

    if value == "no box":
        if raw_value != "no box":
            findings.append(
                Finding(
                    "warning",
                    "no-detection value should be exactly 'no box' without surrounding whitespace",
                    row_number,
                    image_id,
                )
            )
        return findings, box_count

    if value.lower() == "no box":
        findings.append(
            Finding("error", "no-detection value must be exactly lowercase 'no box'", row_number, image_id)
        )
        return findings, box_count

    if not value:
        findings.append(
            Finding("error", "prediction_string is empty; use 'no box' for no detections", row_number, image_id)
        )
        return findings, box_count

    tokens = value.split()
    if len(tokens) % 6 != 0:
        findings.append(
            Finding(
                "error",
                f"prediction_string has {len(tokens)} tokens, not a multiple of 6",
                row_number,
                image_id,
            )
        )
        return findings, box_count

    for offset in range(0, len(tokens), 6):
        box_index = offset // 6
        class_token, conf_token, x_token, y_token, w_token, h_token = tokens[offset : offset + 6]

        if not INT_RE.match(class_token):
            findings.append(
                Finding(
                    "error",
                    f"box {box_index}: class_id must be an integer token in 0..3, got {class_token!r}",
                    row_number,
                    image_id,
                )
            )
            continue

        class_id = int(class_token)
        if class_id not in CLASS_NAMES:
            findings.append(
                Finding(
                    "error",
                    f"box {box_index}: class_id {class_id} is outside 0..3",
                    row_number,
                    image_id,
                )
            )

        numeric_tokens = {
            "confidence": conf_token,
            "x_center": x_token,
            "y_center": y_token,
            "width": w_token,
            "height": h_token,
        }
        parsed: dict[str, float] = {}
        for name, token in numeric_tokens.items():
            try:
                number = parse_float(token)
            except ValueError:
                findings.append(
                    Finding(
                        "error",
                        f"box {box_index}: {name} must be a finite float in [0, 1], got {token!r}",
                        row_number,
                        image_id,
                    )
                )
                continue
            parsed[name] = number
            if number < 0.0 or number > 1.0:
                findings.append(
                    Finding(
                        "error",
                        f"box {box_index}: {name}={number:g} is outside [0, 1]",
                        row_number,
                        image_id,
                    )
                )

        if {"x_center", "y_center", "width", "height"}.issubset(parsed):
            width = parsed["width"]
            height = parsed["height"]
            x_center = parsed["x_center"]
            y_center = parsed["y_center"]

            if width <= 0.0 or height <= 0.0:
                findings.append(
                    Finding(
                        "error",
                        f"box {box_index}: width and height must be positive, got width={width:g}, height={height:g}",
                        row_number,
                        image_id,
                    )
                )

            x_min = x_center - width / 2.0
            x_max = x_center + width / 2.0
            y_min = y_center - height / 2.0
            y_max = y_center + height / 2.0
            outside = x_min < 0.0 or y_min < 0.0 or x_max > 1.0 or y_max > 1.0
            if outside:
                level = "error" if strict_bbox_inside else "warning"
                findings.append(
                    Finding(
                        level,
                        (
                            f"box {box_index}: bbox extends outside normalized image bounds "
                            f"(x_min={x_min:g}, y_min={y_min:g}, x_max={x_max:g}, y_max={y_max:g})"
                        ),
                        row_number,
                        image_id,
                    )
                )

        box_count += 1

    return findings, box_count


def collect_test_image_stems(test_images_dir: Path) -> set[str]:
    if not test_images_dir.exists():
        raise FileNotFoundError(f"test images directory does not exist: {test_images_dir}")
    return {
        path.stem
        for path in test_images_dir.iterdir()
        if path.is_file()
        and not path.name.startswith("._")
        and path.suffix.lower() in IMAGE_EXTENSIONS
    }


def audit(args: argparse.Namespace) -> tuple[list[Finding], dict[str, int]]:
    sample_header, sample_rows = read_csv(args.sample)
    submission_header, submission_rows = read_csv(args.submission)

    findings: list[Finding] = []
    stats = {
        "sample_rows": len(sample_rows),
        "submission_rows": len(submission_rows),
        "images_with_boxes": 0,
        "images_no_box": 0,
        "total_boxes": 0,
    }

    if sample_header != EXPECTED_COLUMNS:
        findings.append(
            Finding(
                "error",
                f"sample header is {sample_header!r}, expected {EXPECTED_COLUMNS!r}; verify the sample file",
            )
        )

    if submission_header != EXPECTED_COLUMNS:
        findings.append(
            Finding(
                "error",
                f"submission header is {submission_header!r}, expected exact columns/order {EXPECTED_COLUMNS!r}",
            )
        )

    if len(submission_rows) != len(sample_rows):
        findings.append(
            Finding(
                "error",
                f"row count mismatch: submission has {len(submission_rows)}, sample has {len(sample_rows)}",
            )
        )

    sample_ids = [row.get("id", "") for row in sample_rows]
    sample_image_ids = [row.get("image_id", "") for row in sample_rows]
    submission_ids = [row.get("id", "") for row in submission_rows]
    submission_image_ids = [row.get("image_id", "") for row in submission_rows]

    for label, values in (
        ("sample id", sample_ids),
        ("sample image_id", sample_image_ids),
        ("submission id", submission_ids),
        ("submission image_id", submission_image_ids),
    ):
        dupes = duplicate_values(values)
        if dupes:
            findings.append(
                Finding("error", f"duplicate {label} values found: {dupes[:10]!r}")
            )

    if set(submission_image_ids) != set(sample_image_ids):
        missing = sorted(set(sample_image_ids) - set(submission_image_ids))
        extra = sorted(set(submission_image_ids) - set(sample_image_ids))
        if missing:
            findings.append(
                Finding("error", f"missing image_id values from sample: {missing[:10]!r}")
            )
        if extra:
            findings.append(
                Finding("error", f"extra image_id values not in sample: {extra[:10]!r}")
            )

    compare_count = min(len(sample_rows), len(submission_rows))
    for idx in range(compare_count):
        row_number = idx + 2  # CSV row number including header.
        sample_row = sample_rows[idx]
        submission_row = submission_rows[idx]
        sample_id = sample_row.get("id", "")
        sample_image_id = sample_row.get("image_id", "")
        submission_id = submission_row.get("id", "")
        submission_image_id = submission_row.get("image_id", "")

        if submission_id != sample_id:
            findings.append(
                Finding(
                    "error",
                    f"id/order mismatch: expected id {sample_id!r}, got {submission_id!r}",
                    row_number,
                    submission_image_id or None,
                )
            )
        if submission_image_id != sample_image_id:
            findings.append(
                Finding(
                    "error",
                    f"image_id/order mismatch: expected {sample_image_id!r}, got {submission_image_id!r}",
                    row_number,
                    submission_image_id or None,
                )
            )

        row_findings, box_count = validate_prediction_string(
            submission_row.get("prediction_string"),
            row_number,
            submission_image_id,
            args.strict_bbox_inside,
        )
        findings.extend(row_findings)
        stats["total_boxes"] += box_count
        if box_count:
            stats["images_with_boxes"] += 1
        else:
            stats["images_no_box"] += 1

    if args.test_images_dir is not None:
        test_stems = collect_test_image_stems(args.test_images_dir)
        sample_stems = set(sample_image_ids)
        if test_stems != sample_stems:
            missing_images = sorted(sample_stems - test_stems)
            extra_images = sorted(test_stems - sample_stems)
            if missing_images:
                findings.append(
                    Finding("error", f"sample image_id values missing from test images: {missing_images[:10]!r}")
                )
            if extra_images:
                findings.append(
                    Finding("error", f"test images not represented in sample_submission.csv: {extra_images[:10]!r}")
                )

    if stats["submission_rows"] and stats["images_with_boxes"] == 0:
        findings.append(
            Finding("warning", "all rows are 'no box'; this is valid format but likely not a competitive submission")
        )

    return findings, stats


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a 3LC vehicle detection Kaggle submission CSV before upload."
    )
    parser.add_argument(
        "submission",
        type=Path,
        help="Path to the candidate submission CSV.",
    )
    parser.add_argument(
        "--sample",
        type=Path,
        default=Path("competition_starter/sample_submission.csv"),
        help="Path to authoritative sample_submission.csv.",
    )
    parser.add_argument(
        "--test-images-dir",
        type=Path,
        default=None,
        help="Optional path to competition_starter/data/test/images for image_id stem cross-checking.",
    )
    parser.add_argument(
        "--strict-bbox-inside",
        action="store_true",
        help="Treat boxes extending outside normalized image bounds as errors instead of warnings.",
    )
    parser.add_argument(
        "--max-findings",
        type=int,
        default=100,
        help="Maximum number of findings to print before truncating.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.submission.exists():
        print(f"ERROR: submission file does not exist: {args.submission}", file=sys.stderr)
        return 2
    if not args.sample.exists():
        print(f"ERROR: sample file does not exist: {args.sample}", file=sys.stderr)
        print(
            "Sync/download competition_starter/sample_submission.csv, or pass --sample /path/to/sample_submission.csv.",
            file=sys.stderr,
        )
        return 2

    try:
        findings, stats = audit(args)
    except Exception as exc:
        print(f"ERROR: audit failed: {exc}", file=sys.stderr)
        return 2

    errors = [finding for finding in findings if finding.level == "error"]
    warnings = [finding for finding in findings if finding.level == "warning"]

    print("Submission audit summary")
    print(f"- sample rows: {stats['sample_rows']}")
    print(f"- submission rows: {stats['submission_rows']}")
    print(f"- images with boxes: {stats['images_with_boxes']}")
    print(f"- images with no box: {stats['images_no_box']}")
    print(f"- total parsed boxes: {stats['total_boxes']}")
    print(f"- errors: {len(errors)}")
    print(f"- warnings: {len(warnings)}")

    if findings:
        print()
        print("Findings")
        for finding in findings[: args.max_findings]:
            print(f"- {finding.format()}")
        remaining = len(findings) - args.max_findings
        if remaining > 0:
            print(f"- INFO: {remaining} additional findings omitted; increase --max-findings to show more.")

    if errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
