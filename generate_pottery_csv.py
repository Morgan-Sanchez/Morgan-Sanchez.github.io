from pathlib import Path
import csv
from collections import defaultdict

# Path to your pottery images folder (relative to repo root)
images_dir = Path("images/pottery")

# Output CSV (also inside the repo so GitHub Pages can serve it)
output_csv = images_dir / "pottery_.csv"

# Allowed image extensions
allowed_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".JPG", ".JPEG", ".PNG"}

# Group images by "base name" (caption), ignoring trailing " 1"/" 2"
# For each base we keep a primary and optional hover image.
groups = defaultdict(lambda: {"primary": None, "hover": None})

for path in sorted(images_dir.iterdir()):
    if path.suffix not in allowed_exts:
        continue

    stem = path.stem  # e.g. "Floral Bowls 1" or "Floral Bowls"

    suffix_num = None
    base_name = stem

    # Look for " ... 1" or " ... 2" at the end of the stem
    if stem.endswith(" 1") or stem.endswith(" 2"):
        suffix_num = stem[-1]          # "1" or "2"
        base_name = stem[:-2]          # drop " 1"/" 2"

    group = groups[base_name]

    if suffix_num == "2":
        # Hover image
        group["hover"] = path.name
    else:
        # Either " 1" or no number at all → treat as primary
        # If there's already a primary, don't overwrite it
        if group["primary"] is None:
            group["primary"] = path.name
        else:
            # If we somehow have two un-numbered images with same base,
            # put the second one in hover if it's still empty.
            if group["hover"] is None:
                group["hover"] = path.name

# Build rows: filename, hover, caption
rows = []
for base_name in sorted(groups.keys()):
    primary = groups[base_name]["primary"]
    hover   = groups[base_name]["hover"] or ""
    if primary is None:
        # Shouldn't happen, but be safe
        continue

    caption = base_name  # you already have proper spaces & capitalization
    rows.append((primary, hover, caption))

# Write CSV: filename,hover,caption
with output_csv.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "hover", "caption"])  # header
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {output_csv}")
