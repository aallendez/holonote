import os

# Project root (change if needed)
PROJECT_ROOT = "."

# Output file
OUTPUT_FILE = "codebase.md"

# Extensions to include
INCLUDE_EXTS = (
    ".py",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".json",
    ".txt",
    ".yml",
    ".yaml",
    ".yml.lock",
    ".yml.lock.yaml",
    "Dockerfile",
    "docker-compose.yaml",
    "makefile",
    ".sql",
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("# Project Codebase\n\n")
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip virtual envs or hidden folders
        if any(
            skip in root
            for skip in [
                ".git",
                "__pycache__",
                ".venv",
                "node_modules",
                "package-lock.json",
                "yarn.lock",
                "pnpm-lock.yaml",
                "coverage",
                "dist",
                "build",
                "out",
                "instance",
                ".pytest_cache",
                ".mypy_cache",
                ".cache",
                ".tox",
                ".env",
                ".env.local",
                ".env.development.local",
                ".env.test.local",
                ".env.production.local",
                ".puml",
            ]
        ):
            continue
        # skip package-lock.json, yarn.lock, pnpm-lock.yaml
        if any(
            file == "package-lock.json"
            or file == "yarn.lock"
            or file == "pnpm-lock.yaml"
            for file in files
        ):
            continue
        # Write folder name
        rel_path = os.path.relpath(root, PROJECT_ROOT)
        if rel_path == ".":
            rel_path = "Root"
        out.write(f"\n\n## 📂 {rel_path}\n\n")

        for file in sorted(files):
            if file.endswith(INCLUDE_EXTS):
                filepath = os.path.join(root, file)
                out.write(f"\n### 📄 {file}\n\n")
                out.write("```" + filepath.split(".")[-1] + "\n")  # syntax highlight
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        out.write(f.read())
                except Exception as e:
                    out.write(f"⚠️ Could not read file: {e}")
                out.write("\n```\n")

print(f"✅ Codebase exported to {OUTPUT_FILE}. Now run:")
print("   pandoc codebase.md -o codebase.pdf   # convert to PDF")
