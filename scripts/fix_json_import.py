import sys
from pathlib import Path

file_path = Path(sys.argv[1])
content = file_path.read_text()

# Add import if not present
if "from app.utils.serializers import JSONSerializable" not in content:
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("import sqlalchemy") or line.startswith(
            "from sqlalchemy"
        ):
            lines.insert(
                i + 1, "from app.utils.serializers import JSONSerializable"
            )
            break
    content = "\n".join(lines)

# Replace fully-qualified references with direct usage
content = content.replace(
    "app.utils.serializers.JSONSerializable", "JSONSerializable"
)

file_path.write_text(content)
print(f"[fix] ✅ JSONSerializable import and usage fixed in {file_path}")
