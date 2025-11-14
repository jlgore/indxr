# Obsidian Templates for indxr

This folder contains everything you need to use **indxr** with Obsidian.

## Files

- **`OBSIDIAN_GUIDE.md`** - Complete integration guide with setup, workflow, and pro tips
- **`Book Index Template.md`** - Ready-to-use Obsidian template for creating index files
- **`Book Index Example.md`** - Example of a filled-out index file with tips

## Quick Setup

### 1. Copy Template to Obsidian

Copy `Book Index Template.md` to your Obsidian vault's `Templates/` folder.

### 2. Create Your Index Structure

In your Obsidian vault, create:

```
YourVault/
├── SEC504/              # Your course folder
│   ├── Index/           # Put index files here
│   │   ├── Book 1 Index.md
│   │   ├── Book 2 Index.md
│   │   └── ...
│   └── PDFs/           # indxr outputs here
└── Templates/
    └── Book Index Template.md
```

### 3. Use the Template

1. In Obsidian, create a new note in `SEC504/Index/`
2. Name it `Book 1 Index.md`
3. Insert the template (Ctrl/Cmd + T or use Templates button)
4. Start taking notes!

### 4. Generate PDFs

```bash
cd /path/to/your/obsidian/vault
indxr all -i SEC504/Index -o SEC504/PDFs
```

## Example Workflow

### As You Study:

```markdown
Book 1, Page 15, Slide: "TCP Handshake" #networking #tcp #protocols
Book 1, Page 20, Slide: "SQL Injection" #web-security #sql-injection #OWASP
Book 1, Page 25, Slide: "XSS Attacks" #web-security #xss #javascript
```

### Generate PDFs:

```bash
indxr all -i SEC504/Index -o SEC504/PDFs
```

### Result:

You get three PDFs:
1. **Per-book contents** (Book_1_Contents.pdf, etc.)
2. **Master Index** - All tags alphabetically
3. **Compact Index** - Quick B#:P# reference

## Learn More

Read **`OBSIDIAN_GUIDE.md`** for:
- Detailed setup instructions
- Obsidian power features
- Dataview queries
- Tag organization tips
- Troubleshooting

## Questions?

- See the main [README](../README.md)
- Check the [OBSIDIAN_GUIDE.md](OBSIDIAN_GUIDE.md)
- Open an issue on GitHub

Happy studying! 📚
