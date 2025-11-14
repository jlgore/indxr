# indxr

A flexible tool for generating indexed study materials from markdown files. Perfect for creating study guides, course indexes, and exam preparation materials.

## Features

- **Per-Book PDFs**: Generate individual content tables for each book
- **Master Index**: Comprehensive alphabetical index of all tags across all books
- **Compact Index**: Two-column quick reference with B#:P# notation
- **Configurable**: Custom titles, patterns, and file locations
- **Easy to Use**: Run with `uvx` - no installation required!
- **Obsidian-Friendly**: Perfect workflow for taking notes in Obsidian

## Perfect for Obsidian Users

**indxr** was designed to work seamlessly with [Obsidian](https://obsidian.md/) note-taking workflows. As you study, simply take notes in Obsidian using a simple format, and indxr generates beautiful PDF indexes automatically.

### Why Obsidian + indxr?

- **Natural Note-Taking**: Just type notes as you normally would in Obsidian
- **Use Obsidian Tags**: Your existing `#hashtags` become index entries
- **No Special Formatting**: The format is simple and human-readable
- **Linked Notes**: Keep your notes linked and organized in Obsidian
- **Generate PDFs Anytime**: Run indxr whenever you need study materials

### Simple Obsidian Workflow

1. **Create a folder** in your Obsidian vault (e.g., `SEC504/Index/`)
2. **Create one note per book** (e.g., `Book 1 Index.md`, `Book 2 Index.md`)
3. **Take notes as you study** using this simple format:

```markdown
Book 1, Page 6, Slide: "Introduction to Security" #security #basics
Book 1, Page 10, Slide: "Network Fundamentals" #networking #tcp-ip #OSI-model
Book 1, Page 15, Slide: "Common Vulnerabilities" #vulnerabilities #OWASP #web-security
```

4. **Generate your PDFs** whenever you want:

```bash
cd /path/to/your/obsidian/vault
uvx --from git+https://github.com/jlgore/indxr indxr all -i SEC504/Index -o SEC504/PDFs
```

5. **Done!** You now have professional PDF study guides

### Want the Full Obsidian Experience?

**See the complete [Obsidian Integration Guide](obsidian-templates/OBSIDIAN_GUIDE.md)** for:
- Templates you can import directly
- Dataview queries for dashboards
- Advanced search techniques
- Daily workflow examples
- Pro tips and shortcuts

The `obsidian-templates/` folder includes:
- Ready-to-use templates
- Example index files
- Complete setup guide

## Quick Start

### Using uvx (Recommended)

Run indxr without installation using `uvx`:

```bash
# Generate all PDFs
uvx --from git+https://github.com/jlgore/indxr indxr all

# Generate just book PDFs
uvx --from git+https://github.com/jlgore/indxr indxr books

# Generate master index
uvx --from git+https://github.com/jlgore/indxr indxr master

# Generate compact index
uvx --from git+https://github.com/jlgore/indxr indxr compact
```

### Using pip

```bash
# Install from GitHub
pip install git+https://github.com/jlgore/indxr

# Or install locally for development
cd indxr
pip install -e .

# Run commands
indxr all
indxr books
indxr master
indxr compact
```

## Usage

### Commands

**`indxr all`** - Generate all PDF types (books + master + compact)

```bash
indxr all -i Cards/Index -o output
```

**`indxr books`** - Generate per-book content PDFs

```bash
indxr books -i Cards/Index -o output --title-prefix "SANS SEC504"
```

**`indxr master`** - Generate master index with all tags

```bash
indxr master -i Cards/Index -o output --title "Master Index" --top-tags 20
```

**`indxr compact`** - Generate compact two-column index

```bash
indxr compact -i Cards/Index -o output --title "Quick Reference"
```

### Options

All commands support these common options:

- `-i, --index-dir PATH` - Directory containing index markdown files (default: `Cards/Index`)
- `-o, --output-dir PATH` - Output directory for PDFs (default: `output`)
- `-p, --pattern TEXT` - Custom regex pattern for parsing entries
- `--file-pattern TEXT` - Glob pattern for finding index files (default: `Book * Index.md`)
- `-c, --config PATH` - Path to config file (TOML format)

Additional options per command:

**books:**
- `--title-prefix TEXT` - Prefix for book titles (e.g., "SANS SEC504")

**master:**
- `--title TEXT` - Custom title for master index
- `--subtitle TEXT` - Custom subtitle
- `--top-tags INTEGER` - Number of top tags to display (default: 10)

**compact:**
- `--title TEXT` - Custom title for compact index

### Configuration File

Create an `indxr.toml` file for persistent settings:

```toml
# Input and output directories
index_dir = "Cards/Index"
output_dir = "output"

# File pattern for finding index files
file_pattern = "Book * Index.md"

# Customization
title_prefix = "SANS SEC504"
master_title = "SANS SEC504<br/>Master Index"
master_subtitle = "Comprehensive Topic Index Across All Books"
compact_title = "SANS SEC504<br/>Compact Index"
```

Use with `-c` flag:

```bash
indxr all -c indxr.toml
```

## Input Format

Index markdown files should follow this format:

```markdown
Book 1, Page 6, Slide: "Introduction to Security" #security #basics
Book 1, Page 10, Slide: "Network Fundamentals" #networking #tcp-ip
Book 1, Page 15, Slide: "Common Vulnerabilities" #vulnerabilities #OWASP
```

Format:
- **Book number** - Integer
- **Page number** - Integer or range (e.g., "10" or "10-11")
- **Slide title** - Quoted string
- **Tags** - Space-separated hashtags

### Custom Patterns

If your format differs, specify a custom regex pattern:

```bash
indxr all -p "Chapter\s+(\d+),\s+Section\s+(\d+),\s+Title:\s+\"([^\"]+)\"\s+(#[\w\-]+(?:\s+#[\w\-]+)*)"
```

## Examples

### SANS Course Materials

```bash
# Generate all PDFs for SANS SEC504
uvx --from git+https://github.com/jlgore/indxr indxr all \
  -i ~/SANS/SEC504/Cards/Index \
  -o ~/SANS/SEC504/output

# Generate just the compact index for quick reference
uvx --from git+https://github.com/jlgore/indxr indxr compact \
  -i ~/SANS/SEC504/Cards/Index \
  -o ~/SANS/SEC504/output \
  --title "SEC504 Quick Reference"
```

### College Course

```bash
# Using custom file pattern and title
indxr all \
  -i ~/Courses/CS101/notes \
  -o ~/Courses/CS101/study-guides \
  --file-pattern "Chapter*.md" \
  --title-prefix "CS101"
```

### With Config File

```bash
# Create indxr.toml with your settings
cat > indxr.toml <<EOF
index_dir = "notes"
output_dir = "pdfs"
file_pattern = "*.md"
title_prefix = "My Course"
EOF

# Run with config
uvx --from git+https://github.com/jlgore/indxr indxr all -c indxr.toml
```

## Development

### Setup

```bash
git clone https://github.com/jlgore/indxr
cd indxr
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black indxr/
ruff check indxr/
```

## Output Examples

### Per-Book PDFs
- `Book_1_Contents.pdf` - Table of contents for Book 1
- `Book_2_Contents.pdf` - Table of contents for Book 2
- etc.

### Master Index
- `Master_Index.pdf` - Alphabetical listing of all tags with:
  - Tag name and occurrence count
  - Book and page references for each occurrence
  - Full slide titles

### Compact Index
- `Compact_Index.pdf` - Two-column quick reference with:
  - Tag name
  - Compact B#:P# notation (e.g., B1:42 = Book 1, Page 42)

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a PR.

## Author

jlgore - https://github.com/jlgore
