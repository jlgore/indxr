"""
Book PDF Generator - Creates individual PDFs for each book's contents
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from pathlib import Path
from typing import List

from ..parser import SlideEntry


class BookPDFGenerator:
    """Generates a PDF for a single book's contents"""

    def __init__(
        self,
        book_number: int,
        entries: List[SlideEntry],
        output_dir: str = "output",
        title_prefix: str = None
    ):
        """
        Initialize generator

        Args:
            book_number: Book number
            entries: List of slide entries for this book
            output_dir: Directory to save PDF
            title_prefix: Optional prefix for title (e.g., "SANS SEC504", "Course XYZ")
        """
        self.book_number = book_number
        self.entries = entries
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.title_prefix = title_prefix or "Study Material"

    def generate(self) -> str:
        """
        Generate the PDF file

        Returns:
            Path to the generated PDF file
        """
        output_path = self.output_dir / f"Book_{self.book_number}_Contents.pdf"

        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )

        # Build content
        story = []
        styles = getSampleStyleSheet()

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        title = Paragraph(f"{self.title_prefix} - Book {self.book_number} Contents", title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*inch))

        # Summary info
        summary_style = ParagraphStyle(
            'Summary',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_CENTER,
            spaceAfter=20
        )

        summary = Paragraph(
            f"Total Slides: {len(self.entries)} | "
            f"Page Range: {self._get_page_range()}",
            summary_style
        )
        story.append(summary)
        story.append(Spacer(1, 0.5*inch))

        # Create table data
        table_data = [['Book', 'Page', 'Slide Title']]

        for entry in self.entries:
            table_data.append([
                str(entry.book_number),
                str(entry.page_number),
                entry.slide_title
            ])

        # Create table with styling
        col_widths = [0.75*inch, 0.75*inch, 5*inch]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)

        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),

            # Body styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 1), (-1, -1), 6),
            ('RIGHTPADDING', (0, 1), (-1, -1), 6),

            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2980B9')),

            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
        ]))

        story.append(table)

        # Build PDF with page numbers
        doc.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)

        return str(output_path)

    def _add_page_number(self, canvas, doc):
        """Add page number to the bottom center of each page"""
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.saveState()
        canvas.setFont('Helvetica', 10)
        canvas.setFillColor(colors.black)
        canvas.drawCentredString(letter[0] / 2, 0.5 * inch, text)
        canvas.restoreState()

    def _get_page_range(self) -> str:
        """Get the page range covered by this book"""
        if not self.entries:
            return "N/A"

        # Extract numeric page numbers (handle ranges like "120-121")
        page_nums = []
        for entry in self.entries:
            page_str = str(entry.page_number)
            if '-' in page_str:
                page_nums.append(int(page_str.split('-')[0]))
            else:
                try:
                    page_nums.append(int(page_str))
                except ValueError:
                    continue

        if page_nums:
            return f"{min(page_nums)}-{max(page_nums)}"
        return "N/A"
