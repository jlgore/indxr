"""
Command-line interface for indxr
"""

import click
import sys
from pathlib import Path
from typing import Optional

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from .parser import IndexParser
from .generators import BookPDFGenerator, MasterIndexGenerator, CompactIndexGenerator


@click.group()
@click.version_option()
def main():
    """indxr - Generate indexed study materials from markdown files"""
    pass


@main.command()
@click.option(
    '-i', '--index-dir',
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default='Cards/Index',
    help='Directory containing index markdown files'
)
@click.option(
    '-o', '--output-dir',
    type=click.Path(path_type=Path),
    default='output',
    help='Output directory for generated PDFs'
)
@click.option(
    '-p', '--pattern',
    type=str,
    help='Custom regex pattern for parsing entries'
)
@click.option(
    '--file-pattern',
    type=str,
    default='Book * Index.md',
    help='Glob pattern for finding index files'
)
@click.option(
    '--title-prefix',
    type=str,
    help='Title prefix for book PDFs (e.g., "SANS SEC504")'
)
@click.option(
    '-c', '--config',
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help='Path to config file (TOML format)'
)
def books(
    index_dir: Path,
    output_dir: Path,
    pattern: Optional[str],
    file_pattern: str,
    title_prefix: Optional[str],
    config: Optional[Path]
):
    """Generate per-book content PDFs"""

    # Load config if provided
    if config:
        with open(config, 'rb') as f:
            config_data = tomllib.load(f)
        index_dir = Path(config_data.get('index_dir', index_dir))
        output_dir = Path(config_data.get('output_dir', output_dir))
        pattern = config_data.get('pattern', pattern)
        file_pattern = config_data.get('file_pattern', file_pattern)
        title_prefix = config_data.get('title_prefix', title_prefix)

    if not index_dir.exists():
        click.echo(f"Error: Index directory '{index_dir}' does not exist.", err=True)
        sys.exit(1)

    # Find index files
    index_files = sorted(index_dir.glob(file_pattern))

    if not index_files:
        click.echo(f"No index files found in {index_dir} matching '{file_pattern}'", err=True)
        sys.exit(1)

    click.echo(f"Found {len(index_files)} index file(s)\n")

    # Parse all index files
    all_entries = IndexParser.parse_multiple([str(f) for f in index_files], pattern)

    if not all_entries:
        click.echo("No entries parsed from index files", err=True)
        sys.exit(1)

    # Generate PDF for each book
    output_dir.mkdir(parents=True, exist_ok=True)

    for book_num, entries in sorted(all_entries.items()):
        click.echo(f"Generating PDF for Book {book_num}...")
        generator = BookPDFGenerator(
            book_num,
            entries,
            str(output_dir),
            title_prefix=title_prefix
        )
        output_file = generator.generate()
        click.echo(f"  [OK] Created: {output_file} ({len(entries)} slides)\n")

    click.echo(f"All book PDFs generated in '{output_dir}' directory")


@main.command()
@click.option(
    '-i', '--index-dir',
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default='Cards/Index',
    help='Directory containing index markdown files'
)
@click.option(
    '-o', '--output-dir',
    type=click.Path(path_type=Path),
    default='output',
    help='Output directory for generated PDF'
)
@click.option(
    '-p', '--pattern',
    type=str,
    help='Custom regex pattern for parsing entries'
)
@click.option(
    '--file-pattern',
    type=str,
    default='Book * Index.md',
    help='Glob pattern for finding index files'
)
@click.option(
    '--title',
    type=str,
    help='Custom title for master index'
)
@click.option(
    '--subtitle',
    type=str,
    help='Custom subtitle for master index'
)
@click.option(
    '--top-tags',
    type=int,
    default=10,
    help='Number of top tags to display'
)
@click.option(
    '-c', '--config',
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help='Path to config file (TOML format)'
)
def master(
    index_dir: Path,
    output_dir: Path,
    pattern: Optional[str],
    file_pattern: str,
    title: Optional[str],
    subtitle: Optional[str],
    top_tags: int,
    config: Optional[Path]
):
    """Generate master index PDF with all tags"""

    # Load config if provided
    if config:
        with open(config, 'rb') as f:
            config_data = tomllib.load(f)
        index_dir = Path(config_data.get('index_dir', index_dir))
        output_dir = Path(config_data.get('output_dir', output_dir))
        pattern = config_data.get('pattern', pattern)
        file_pattern = config_data.get('file_pattern', file_pattern)
        title = config_data.get('master_title', title)
        subtitle = config_data.get('master_subtitle', subtitle)

    if not index_dir.exists():
        click.echo(f"Error: Index directory '{index_dir}' does not exist.", err=True)
        sys.exit(1)

    # Find index files
    index_files = sorted(index_dir.glob(file_pattern))

    if not index_files:
        click.echo(f"No index files found in {index_dir} matching '{file_pattern}'", err=True)
        sys.exit(1)

    click.echo(f"Found {len(index_files)} index file(s)\n")

    # Parse all index files
    click.echo("Parsing index files...")
    all_entries = IndexParser.parse_multiple([str(f) for f in index_files], pattern)

    click.echo(f"Parsed {sum(len(e) for e in all_entries.values())} total slides\n")

    # Generate master index
    click.echo("Generating master index PDF...")
    output_dir.mkdir(parents=True, exist_ok=True)

    generator = MasterIndexGenerator(
        all_entries,
        str(output_dir),
        title=title,
        subtitle=subtitle
    )

    # Show statistics
    stats = generator.get_statistics()
    click.echo(f"\nStatistics:")
    click.echo(f"  Total Books: {stats['total_books']}")
    click.echo(f"  Total Slides: {stats['total_slides']}")
    click.echo(f"  Unique Tags: {stats['total_tags']}")

    click.echo(f"\nTop {top_tags} Most Common Tags:")
    for tag_info in stats['top_tags'][:top_tags]:
        tag = tag_info['tag'][1:] if tag_info['tag'].startswith('#') else tag_info['tag']
        click.echo(f"  {tag}: {tag_info['count']} occurrences across {tag_info['books']} book(s)")

    output_file = generator.generate()
    click.echo(f"\n[OK] Master index created: {output_file}")


@main.command()
@click.option(
    '-i', '--index-dir',
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default='Cards/Index',
    help='Directory containing index markdown files'
)
@click.option(
    '-o', '--output-dir',
    type=click.Path(path_type=Path),
    default='output',
    help='Output directory for generated PDF'
)
@click.option(
    '-p', '--pattern',
    type=str,
    help='Custom regex pattern for parsing entries'
)
@click.option(
    '--file-pattern',
    type=str,
    default='Book * Index.md',
    help='Glob pattern for finding index files'
)
@click.option(
    '--title',
    type=str,
    help='Custom title for compact index'
)
@click.option(
    '-c', '--config',
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help='Path to config file (TOML format)'
)
def compact(
    index_dir: Path,
    output_dir: Path,
    pattern: Optional[str],
    file_pattern: str,
    title: Optional[str],
    config: Optional[Path]
):
    """Generate compact two-column index PDF"""

    # Load config if provided
    if config:
        with open(config, 'rb') as f:
            config_data = tomllib.load(f)
        index_dir = Path(config_data.get('index_dir', index_dir))
        output_dir = Path(config_data.get('output_dir', output_dir))
        pattern = config_data.get('pattern', pattern)
        file_pattern = config_data.get('file_pattern', file_pattern)
        title = config_data.get('compact_title', title)

    if not index_dir.exists():
        click.echo(f"Error: Index directory '{index_dir}' does not exist.", err=True)
        sys.exit(1)

    # Find index files
    index_files = sorted(index_dir.glob(file_pattern))

    if not index_files:
        click.echo(f"No index files found in {index_dir} matching '{file_pattern}'", err=True)
        sys.exit(1)

    click.echo(f"Found {len(index_files)} index file(s)\n")

    # Parse all index files
    click.echo("Parsing index files...")
    all_entries = IndexParser.parse_multiple([str(f) for f in index_files], pattern)

    click.echo(f"Parsed {sum(len(e) for e in all_entries.values())} total slides\n")

    # Generate compact index
    click.echo("Generating compact two-column index PDF...")
    output_dir.mkdir(parents=True, exist_ok=True)

    generator = CompactIndexGenerator(all_entries, str(output_dir), title=title)

    # Show statistics
    stats = generator.get_statistics()
    click.echo(f"\nStatistics:")
    click.echo(f"  Total Books: {stats['total_books']}")
    click.echo(f"  Total Slides: {stats['total_slides']}")
    click.echo(f"  Unique Tags: {stats['total_tags']}")

    output_file = generator.generate()
    click.echo(f"\n[OK] Compact index created: {output_file}")
    click.echo(f"Format: Two columns per page with B#:P# notation")


@main.command()
@click.option(
    '-i', '--index-dir',
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default='Cards/Index',
    help='Directory containing index markdown files'
)
@click.option(
    '-o', '--output-dir',
    type=click.Path(path_type=Path),
    default='output',
    help='Output directory for generated PDFs'
)
@click.option(
    '-c', '--config',
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help='Path to config file (TOML format)'
)
def all(index_dir: Path, output_dir: Path, config: Optional[Path]):
    """Generate all PDFs (books, master index, and compact index)"""

    click.echo("=" * 70)
    click.echo("indxr - Generating All PDFs")
    click.echo("=" * 70)
    click.echo()

    # Pass config to each subcommand
    ctx = click.get_current_context()

    click.echo("=" * 70)
    click.echo("FEATURE 1: Generating Per-Book Content PDFs")
    click.echo("=" * 70)
    click.echo()
    ctx.invoke(books, index_dir=index_dir, output_dir=output_dir, pattern=None,
               file_pattern='Book * Index.md', title_prefix=None, config=config)

    click.echo()
    click.echo("=" * 70)
    click.echo("FEATURE 2: Generating Master Index PDF")
    click.echo("=" * 70)
    click.echo()
    ctx.invoke(master, index_dir=index_dir, output_dir=output_dir, pattern=None,
               file_pattern='Book * Index.md', title=None, subtitle=None, top_tags=10, config=config)

    click.echo()
    click.echo("=" * 70)
    click.echo("FEATURE 3: Generating Compact Index PDF")
    click.echo("=" * 70)
    click.echo()
    ctx.invoke(compact, index_dir=index_dir, output_dir=output_dir, pattern=None,
               file_pattern='Book * Index.md', title=None, config=config)

    click.echo()
    click.echo("=" * 70)
    click.echo("All PDFs generated successfully!")
    click.echo("=" * 70)
    click.echo(f"\nCheck the '{output_dir}' directory for your PDFs.")


if __name__ == '__main__':
    main()
