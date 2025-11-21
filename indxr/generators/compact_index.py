"""
Compact Index Generator - Creates two-column quick reference with B#:P# notation
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, Frame, PageTemplate, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus.doctemplate import BaseDocTemplate
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

from ..parser import SlideEntry


class CompactIndexGenerator:
    """Generates a compact two-column index PDF with just book/page references"""

    def __init__(
        self,
        all_entries: Dict[int, List[SlideEntry]],
        output_dir: str = "output",
        title: str = None
    ):
        """
        Initialize generator

        Args:
            all_entries: Dictionary of book_number -> list of SlideEntry
            output_dir: Directory to save PDF
            title: Custom title (default: "Compact Index")
        """
        self.all_entries = all_entries
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.title = title or "Compact Index"
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
        """Generate the compact index PDF with two columns"""
        output_path = self.output_dir / "Compact_Index.pdf"

        # Create PDF document with two-column layout
        doc = BaseDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.75*inch,
            bottomMargin=0.5*inch
        )

        # Define two-column frame layout
        frame_width = (letter[0] - 1.25*inch) / 2
        frame_height = letter[1] - 1.25*inch

        frame1 = Frame(
            0.5*inch, 0.5*inch,
            frame_width, frame_height,
            id='col1',
            showBoundary=0
        )

        frame2 = Frame(
            0.5*inch + frame_width + 0.25*inch, 0.5*inch,
            frame_width, frame_height,
            id='col2',
            showBoundary=0
        )

        template = PageTemplate(id='TwoCol', frames=[frame1, frame2], onPage=self._add_page_number)
        doc.addPageTemplates([template])

        story = []
        styles = getSampleStyleSheet()

        # Title page
        story.extend(self._create_title_page(styles))

        # Generate compact index entries
        sorted_tags = sorted(self.tag_index.keys())

        for tag in sorted_tags:
            entries = self.tag_index[tag]
            story.extend(self._create_compact_tag_entry(tag, entries, styles))

        # Build PDF
        doc.build(story)

        return str(output_path)

    def _add_page_number(self, canvas, doc):
        """Add page number to the bottom center of each page"""
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor('#7F8C8D'))
        canvas.drawCentredString(letter[0] / 2, 0.5 * inch, text)
        canvas.restoreState()

    def _create_title_page(self, styles) -> List:
        """Create the title page"""
        elements = []

        title_style = ParagraphStyle(
            'CompactTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=15,
            alignment=TA_CENTER
        )

        title = Paragraph(self.title, title_style)
        elements.append(Spacer(1, 0.5*inch))
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))

        subtitle_style = ParagraphStyle(
            'CompactSubtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_CENTER,
            spaceAfter=20
        )

        subtitle = Paragraph("Quick Reference: Book &amp; Page Numbers Only", subtitle_style)
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3*inch))

        # Statistics
        total_slides = sum(len(entries) for entries in self.all_entries.values())
        total_books = len(self.all_entries)
        total_tags = len(self.tag_index)

        stats_style = ParagraphStyle(
            'CompactStats',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#34495E'),
            alignment=TA_CENTER,
            spaceAfter=10,
            leading=14
        )

        stats_text = f"""
        <b>{total_books}</b> Books | <b>{total_slides}</b> Slides | <b>{total_tags}</b> Topics
        """

        stats = Paragraph(stats_text, stats_style)
        elements.append(stats)
        elements.append(Spacer(1, 0.2*inch))

        # Format explanation
        format_style = ParagraphStyle(
            'FormatExplain',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#95A5A6'),
            alignment=TA_CENTER,
            spaceAfter=20,
            leading=11
        )

        format_text = """
        Format: <b>B#:P#</b> = Book Number : Page Number<br/>
        Example: <b>B1:42</b> = Book 1, Page 42
        """

        format_explain = Paragraph(format_text, format_style)
        elements.append(format_explain)
        elements.append(PageBreak())

        return elements

    def _create_compact_tag_entry(self, tag: str, entries: List[SlideEntry], styles) -> List:
        """Create a compact entry for a single tag"""
        elements = []

        tag_style = ParagraphStyle(
            'CompactTag',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#2980B9'),
            fontName='Helvetica-Bold',
            spaceAfter=2,
            spaceBefore=6,
            leftIndent=0
        )

        location_style = ParagraphStyle(
            'CompactLocation',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#34495E'),
            fontName='Helvetica',
            spaceAfter=3,
            leftIndent=10,
            leading=10
        )

        # Remove the # from tag for display
        tag_display = tag if not tag.startswith('#') else tag[1:]

        # Create compact location references: B1:6, B1:10, B2:15
        locations = [f"B{entry.book_number}:{entry.page_number}" for entry in entries]
        location_text = ", ".join(locations)

        # Add tag heading
        tag_para = Paragraph(f"<b>{tag_display}</b>", tag_style)

        # Add locations
        location_para = Paragraph(location_text, location_style)

        # Keep tag and locations together
        tag_entry = KeepTogether([tag_para, location_para])
        elements.append(tag_entry)

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
