# Obsidian Integration Guide for indxr

This guide shows you how to use **indxr** with Obsidian for an amazing study workflow.

## Why Obsidian + indxr?

Obsidian is perfect for taking study notes because:
- **Fast and Simple**: Just type in plain markdown
- **Tag Autocomplete**: Start typing `#` and Obsidian suggests existing tags
- **Powerful Search**: Find any topic across all your notes instantly
- **Links**: Connect related concepts with `[[links]]`
- **Offline**: All your notes are local markdown files
- **Free**: Obsidian is free for personal use

**indxr** then transforms your simple Obsidian notes into:
- Professional PDF indexes
- Organized study guides
- Quick reference sheets

## Setup (5 minutes)

### 1. Install Obsidian
Download from [obsidian.md](https://obsidian.md) (free)

### 2. Create Your Vault Structure

In your Obsidian vault, create this folder structure:

```
YourVault/
├── SEC504/                    # Or your course name
│   ├── Index/                 # Put all index files here
│   │   ├── Book 1 Index.md
│   │   ├── Book 2 Index.md
│   │   ├── Book 3 Index.md
│   │   └── ...
│   ├── PDFs/                  # indxr will generate PDFs here
│   └── Notes/                 # Your other study notes (optional)
└── Templates/                 # Obsidian templates folder
    └── Book Index Template.md
```

### 3. Add the Template

1. Copy `Book Index Template.md` from this repo to your Obsidian `Templates/` folder
2. In Obsidian: Settings → Core Plugins → Enable "Templates"
3. In Obsidian: Settings → Templates → Set template folder to `Templates/`

### 4. Install indxr

```bash
pip install git+https://github.com/jlgore/indxr
```

Or use with `uvx` (no installation):
```bash
uvx --from git+https://github.com/jlgore/indxr indxr --help
```

## Daily Workflow

### As You Study

1. **Open the index file** for the current book (e.g., `Book 1 Index.md`)
2. **For each slide/page**, add one line:
   ```markdown
   Book 1, Page 42, Slide: "Buffer Overflow Attacks" #memory-corruption #exploitation #C-programming
   ```
3. **Let Obsidian help you**:
   - Start typing `#` and it will autocomplete existing tags
   - Use consistent tag names for better organization
   - Add 3-5 tags per entry

### When You Want PDFs

Open a terminal in your Obsidian vault directory:

```bash
# Generate all PDFs
indxr all -i SEC504/Index -o SEC504/PDFs

# Or with uvx (no installation)
uvx --from git+https://github.com/jlgore/indxr indxr all -i SEC504/Index -o SEC504/PDFs
```

**That's it!** Your PDFs are ready in `SEC504/PDFs/`

## Pro Tips

### 1. Use Keyboard Shortcuts

Create a hotkey for your template:
- Settings → Hotkeys → Search "Insert template"
- Assign a shortcut (e.g., `Ctrl+T`)

### 2. Tag Naming Conventions

Use consistent, searchable tag names:

✅ **Good**:
- `#sql-injection`
- `#OWASP-top-10`
- `#incident-response`

❌ **Avoid**:
- `#SQL injection` (spaces don't work in tags)
- `#sqlinjection` (hard to read)
- `#sql_injection` (inconsistent with others)

### 3. Common Tag Categories

Organize tags by category:
- **Topics**: `#encryption`, `#networking`, `#malware`
- **Tools**: `#wireshark`, `#nmap`, `#metasploit`
- **Frameworks**: `#MITRE-ATTACK`, `#OWASP`, `#NIST`
- **Techniques**: `#reconnaissance`, `#exploitation`, `#privilege-escalation`
- **Importance**: `#exam-critical`, `#lab-exercise`, `#hands-on`

### 4. Link to Detailed Notes

Add links to your detailed notes:

```markdown
Book 1, Page 42, Slide: "Buffer Overflow Attacks" #memory-corruption #exploitation
[[Buffer Overflows - Detailed Notes]]
```

### 5. Use Obsidian's Tag Pane

- Open the right sidebar
- Click the tag icon
- See all your tags and their counts
- Click any tag to see all occurrences

### 6. Search Across All Indexes

- Press `Ctrl/Cmd + Shift + F` for global search
- Search for: `tag:#sql-injection` to find all SQL injection entries
- Search for: `"Book 2"` to see all Book 2 entries

## Advanced: Dataview Plugin

Install the [Dataview plugin](https://blacksmithgu.github.io/obsidian-dataview/) for powerful queries.

### Create a Dashboard

Create a note called `Study Dashboard.md`:

````markdown
# SEC504 Study Dashboard

## Progress by Book

```dataview
TABLE
  length(file.lists) as "Entries",
  file.mtime as "Last Updated"
FROM "SEC504/Index"
WHERE contains(file.name, "Book")
SORT file.name
```

## Most Common Tags

```dataview
TABLE length(rows) as "Count"
FROM "SEC504/Index"
FLATTEN file.tags as tag
WHERE contains(tag, "#")
GROUP BY tag
SORT length(rows) DESC
LIMIT 20
```

## Recent Entries

```dataview
LIST
FROM "SEC504/Index"
SORT file.mtime DESC
LIMIT 10
```
````

### Quick Tag Search

Create reusable queries:

````markdown
## All Exploitation Techniques

```dataview
LIST
WHERE contains(file.path, "Index") AND contains(file.tags, "#exploitation")
```

## All Exam Critical Topics

```dataview
LIST
WHERE contains(file.path, "Index") AND contains(file.tags, "#exam-critical")
```
````

## Workflow Examples

### Example 1: Studying SEC504

```
1. Open Obsidian to SEC504/Index/Book 1 Index.md
2. Instructor is on slide about "TCP Handshake"
3. Type: Book 1, Page 15, Slide: "TCP Three-Way Handshake" #networking #TCP #protocols
4. Obsidian autocompletes #networking, #TCP, #protocols (you used these before)
5. Continue for all slides in the session
6. After class, run: indxr all -i SEC504/Index -o SEC504/PDFs
7. Review the generated Master_Index.pdf to see all topics organized alphabetically
8. Use Compact_Index.pdf as a quick reference during labs
```

### Example 2: Exam Prep

```
1. Open the Master_Index.pdf generated by indxr
2. See "SQL Injection" appears on Book 1, Page 20 and Book 3, Page 45
3. Open Obsidian and search: tag:#sql-injection
4. Obsidian shows all your SQL injection entries
5. Click [[linked notes]] to review your detailed notes
6. Practice the labs listed in those sections
```

## Config File for Your Vault

Create `indxr.toml` in your vault root:

```toml
# indxr configuration for SEC504
index_dir = "SEC504/Index"
output_dir = "SEC504/PDFs"
file_pattern = "Book * Index.md"
title_prefix = "SANS SEC504"
master_title = "SANS SEC504<br/>Master Index"
compact_title = "SEC504<br/>Quick Reference"
```

Then just run:
```bash
indxr all -c indxr.toml
```

## Troubleshooting

### Tags not working?
- Make sure tags have no spaces: use `#web-security` not `#web security`
- Tags must start with a letter: `#2fa` won't work, use `#two-factor-auth`

### PDFs empty?
- Check your index files match the format exactly
- Run: `indxr books -i SEC504/Index -o test` to see if entries are parsed

### Want custom format?
- Use the `-p` flag to specify a custom regex pattern
- See README.md for pattern examples

## Questions?

- Check the main [README.md](../README.md)
- Open an issue on [GitHub](https://github.com/jlgore/indxr/issues)
- See [QUICKSTART.md](../QUICKSTART.md) for basic usage

## Happy Studying! 📚

The combination of Obsidian's note-taking power and indxr's PDF generation makes studying efficient and organized. Your notes stay searchable in Obsidian, and you get professional PDFs for offline review and exam prep.
