# Quick Start Guide

## Perfect for Obsidian Users! 📝

**Taking notes in Obsidian?** You're in the perfect place! Just format your study notes like this:

```markdown
Book 1, Page 6, Slide: "Introduction" #security #basics
Book 1, Page 10, Slide: "Networks" #networking #tcp-ip
```

Then run `indxr` to generate beautiful PDFs. See the [Obsidian Integration Guide](obsidian-templates/OBSIDIAN_GUIDE.md) for the complete workflow.

## Installation

### Option 1: Use with uvx (No Installation Required)

```bash
# Run from anywhere without installing
uvx --from git+https://github.com/jlgore/indxr indxr all
```

### Option 2: Install Locally

```bash
cd indxr
pip install -e .
```

## Basic Usage

### Generate All PDFs

```bash
# Using installed version
indxr all -i Cards/Index -o output

# Using Python module directly
python -m indxr.cli all -i Cards/Index -o output

# Using uvx
uvx --from git+https://github.com/jlgore/indxr indxr all -i Cards/Index -o output
```

### Generate Specific Types

```bash
# Just book PDFs
indxr books -i Cards/Index -o output

# Just master index
indxr master -i Cards/Index -o output

# Just compact index
indxr compact -i Cards/Index -o output
```

## Customization

### Add Custom Titles

```bash
indxr books --title-prefix "SANS SEC504"
indxr master --title "My Custom Index" --subtitle "Study Guide 2024"
indxr compact --title "Quick Reference"
```

### Using a Config File

Create `indxr.toml`:

```toml
index_dir = "Cards/Index"
output_dir = "output"
file_pattern = "Book * Index.md"
title_prefix = "SANS SEC504"
master_title = "SANS SEC504<br/>Master Index"
```

Then run:

```bash
indxr all -c indxr.toml
```

## Publishing to GitHub

```bash
# Initialize git repo in indxr directory
cd indxr
git init
git add .
git commit -m "Initial commit: indxr package"

# Create repo on GitHub at github.com/jlgore/indxr
# Then push:
git remote add origin https://github.com/jlgore/indxr.git
git branch -M main
git push -u origin main
```

## After Publishing

Anyone can then use it with uvx:

```bash
uvx --from git+https://github.com/jlgore/indxr indxr all
```

Or install it:

```bash
pip install git+https://github.com/jlgore/indxr
```

## Help

Get help on any command:

```bash
indxr --help
indxr books --help
indxr master --help
indxr compact --help
indxr all --help
```
