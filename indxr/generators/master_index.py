"""
Master Index Generator - Creates comprehensive alphabetical index across all books
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

from ..parser import SlideEntry


class MasterIndexGenerator:
    """Generates a master index PDF with all tags across all books"""

    def __init__(
        self,
        all_entries: Dict[int, List[SlideEntry]],
        output_dir: str = "output",
        title: str = None,
        subtitle: str = None
    ):
        """
        Initialize generator

        Args:
            all_entries: Dictionary of book_number -> list of SlideEntry
            output_dir: Directory to save PDF
            title: Custom title (default: "Master Index")
            subtitle: Custom subtitle
        """
        self.all_entries = all_entries
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.title = title or "Master Index"
        self.subtitle = subtitle or "Comprehensive Topic Index Across All Books"
        self.tag_index = self._build_tag_index()

    def _build_tag_index(self) -> Dict[str, List[SlideEntry]]:
        """Build a comprehensive tag index from all entries"""
        tag_map = defaultdict(list)

        for book_num, entries in self.all_entries.items():
            for entry in entries:
                for tag in entry.tags:
                    tag_map[tag].append(entry)

        # Sort entries within each tag by book number, then page number
        for tag in tag_map:
            tag_map[tag].sort(key=lambda e: (e.book_number, self._parse_page_num(e.page_number)))

        return dict(tag_map)

    @staticmethod
    def _parse_page_num(page_str: str) -> int:
        """Parse page number string, handling ranges like '120-121'"""
        if '-' in page_str:
            return int(page_str.split('-')[0])
        try:
            return int(page_str)
        except ValueError:
            return 0

    def generate(self) -> str:
        """Generate the master index PDF"""
        output_path = self.output_dir / "Master_Index.pdf"

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )

        story = []
        styles = getSampleStyleSheet()

        # Title page
        story.extend(self._create_title_page(styles))

        # Generate index entries for each tag (sorted alphabetically)
        sorted_tags = sorted(self.tag_index.keys())

        for tag in sorted_tags:
            entries = self.tag_index[tag]
            story.extend(self._create_tag_section(tag, entries, styles))

        # Build PDF
        doc.build(story)

        return str(output_path)

    def _create_title_page(self, styles) -> List:
        """Create the title page"""
        elements = []

        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=20,
            alignment=TA_CENTER
        )

        title = Paragraph(self.title, title_style)
        elements.append(Spacer(1, 1.5*inch))
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))

        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_CENTER,
            spaceAfter=30
        )

        subtitle = Paragraph(self.subtitle, subtitle_style)
        elements.append(subtitle)
        elements.append(Spacer(1, 0.5*inch))

        # Statistics
        total_slides = sum(len(entries) for entries in self.all_entries.values())
        total_books = len(self.all_entries)
        total_tags = len(self.tag_index)

        stats_style = ParagraphStyle(
            'Stats',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#34495E'),
            alignment=TA_CENTER,
            spaceAfter=10,
            leading=18
        )

        stats_text = f"""
        <b>Total Books:</b> {total_books}<br/>
        <b>Total Slides:</b> {total_slides}<br/>
        <b>Total Unique Tags:</b> {total_tags}
        """

        stats = Paragraph(stats_text, stats_style)
        elements.append(stats)
        elements.append(PageBreak())

        return elements

    def _create_tag_section(self, tag: str, entries: List[SlideEntry], styles) -> List:
        """Create a section for a single tag with all its occurrences"""
        elements = []

        tag_style = ParagraphStyle(
            'TagHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2980B9'),
            spaceAfter=10,
            spaceBefore=15,
            leftIndent=0,
            fontName='Helvetica-Bold'
        )

        tag_display = tag if not tag.startswith('#') else tag[1:]
        tag_heading = Paragraph(
            f"<b>{tag}</b>  <font size=10 color='#95A5A6'>({len(entries)} occurrence{'s' if len(entries) != 1 else ''})</font>",
            tag_style
        )

        # Create table for entries
        table_data = []
        for entry in entries:
            location = f"Book {entry.book_number}, Page {entry.page_number}"
            table_data.append([location, entry.slide_title])

        col_widths = [1.5*inch, 5*inch]
        table = Table(table_data, colWidths=col_widths)

        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2C3E50')),
        ]))

        tag_section = KeepTogether([tag_heading, table, Spacer(1, 0.15*inch)])
        elements.append(tag_section)

        return elements

    def get_statistics(self) -> Dict:
        """Get statistics about the index"""
        total_slides = sum(len(entries) for entries in self.all_entries.values())

        tag_stats = []
        for tag, entries in sorted(self.tag_index.items(), key=lambda x: len(x[1]), reverse=True):
            tag_stats.append({
                'tag': tag,
                'count': len(entries),
                'books': len(set(e.book_number for e in entries))
            })

        return {
            'total_books': len(self.all_entries),
            'total_slides': total_slides,
            'total_tags': len(self.tag_index),
            'top_tags': tag_stats[:20]
        }
