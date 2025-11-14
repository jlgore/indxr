"""
Index file parser for extracting structured slide data
"""

import re
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path


@dataclass
class SlideEntry:
    """Represents a single slide entry from an index file"""
    book_number: int
    page_number: str
    slide_title: str
    tags: List[str]

    def __repr__(self):
        tags_str = " ".join(self.tags)
        return f"Book {self.book_number}, Page {self.page_number}, Slide: \"{self.slide_title}\" {tags_str}"


class IndexParser:
    """Parses index files with configurable patterns"""

    # Default pattern: Book 1, Page 6, Slide: "Title" #tag1 #tag2
    DEFAULT_PATTERN = r'Book\s+(\d+),\s+Page\s+(\d+(?:-\d+)?),\s+Slide:\s+"([^"]+)"\s+(#[\w\-]+(?:\s+#[\w\-]+)*)'

    def __init__(self, index_file_path: str, pattern: str = None):
        """
        Initialize parser

        Args:
            index_file_path: Path to index markdown file
            pattern: Optional regex pattern override
        """
        self.index_file_path = Path(index_file_path)
        self.pattern = pattern or self.DEFAULT_PATTERN
        self.entries: List[SlideEntry] = []

        if not self.index_file_path.exists():
            raise FileNotFoundError(f"Index file not found: {index_file_path}")

    def parse(self) -> List[SlideEntry]:
        """Parse the index file and return list of SlideEntry objects"""
        try:
            with open(self.index_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise IOError(f"Error reading {self.index_file_path}: {e}")

        matches = re.finditer(self.pattern, content)

        for match in matches:
            try:
                book_num = int(match.group(1))
                page_num = match.group(2)  # Keep as string to handle ranges like "120-121"
                slide_title = match.group(3)
                tags_str = match.group(4)

                # Extract individual tags
                tags = re.findall(r'#[\w\-]+', tags_str)

                entry = SlideEntry(
                    book_number=book_num,
                    page_number=page_num,
                    slide_title=slide_title,
                    tags=tags
                )
                self.entries.append(entry)
            except (IndexError, ValueError) as e:
                # Skip malformed entries but continue parsing
                continue

        return self.entries

    @staticmethod
    def parse_multiple(index_file_paths: List[str], pattern: str = None) -> Dict[int, List[SlideEntry]]:
        """
        Parse multiple index files and return a dictionary keyed by book number

        Args:
            index_file_paths: List of paths to index files
            pattern: Optional regex pattern override

        Returns:
            Dictionary mapping book_number -> list of SlideEntry objects
        """
        all_entries = {}

        for file_path in index_file_paths:
            try:
                parser = IndexParser(file_path, pattern)
                entries = parser.parse()

                # Group by book number
                for entry in entries:
                    if entry.book_number not in all_entries:
                        all_entries[entry.book_number] = []
                    all_entries[entry.book_number].append(entry)
            except (FileNotFoundError, IOError) as e:
                print(f"Warning: Skipping {file_path}: {e}")
                continue

        return all_entries

    @staticmethod
    def get_all_tags(entries: List[SlideEntry]) -> Dict[str, List[SlideEntry]]:
        """
        Extract all unique tags and map them to their slide entries

        Args:
            entries: List of SlideEntry objects

        Returns:
            Dictionary mapping tag -> list of SlideEntry objects that contain that tag
        """
        tag_map = {}

        for entry in entries:
            for tag in entry.tags:
                if tag not in tag_map:
                    tag_map[tag] = []
                tag_map[tag].append(entry)

        return tag_map
