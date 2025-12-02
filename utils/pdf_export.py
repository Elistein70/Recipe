"""
PDF export functionality for EatKosher recipes
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
import io
from utils.recipe_parser import parse_recipe


def create_recipe_pdf(recipe_text, rating=None):
    """
    Creates a beautiful PDF from recipe text.

    Args:
        recipe_text (str): Recipe in markdown format
        rating (int): Optional 1-5 star rating

    Returns:
        bytes: PDF file content
    """
    # Parse recipe
    recipe_data = parse_recipe(recipe_text)

    # Create PDF buffer
    buffer = io.BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles with royal blue theme
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1E3A8A'),  # Royal blue
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#1E3A8A'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_LEFT
    )

    meta_style = ParagraphStyle(
        'CustomMeta',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#4B5563'),
        spaceAfter=6,
        alignment=TA_CENTER
    )

    # Build PDF content
    story = []

    # Header with EatKosher branding
    header = Paragraph("EatKosher – אכילת כשר", title_style)
    story.append(header)
    story.append(Spacer(1, 0.2*inch))

    # Recipe title
    if recipe_data['title']:
        title = Paragraph(recipe_data['title'], heading_style)
        story.append(title)
        story.append(Spacer(1, 0.1*inch))

    # Rating
    if rating:
        stars = "★" * rating + "☆" * (5 - rating)
        rating_text = Paragraph(f"<b>Rating:</b> {stars}", meta_style)
        story.append(rating_text)

    # Metadata
    meta_parts = []
    if recipe_data['prep_time']:
        meta_parts.append(f"<b>Prep:</b> {recipe_data['prep_time']}")
    if recipe_data['cook_time']:
        meta_parts.append(f"<b>Cook:</b> {recipe_data['cook_time']}")
    if recipe_data['servings']:
        meta_parts.append(f"<b>Serves:</b> {recipe_data['servings']}")

    if meta_parts:
        meta_text = " | ".join(meta_parts)
        meta = Paragraph(meta_text, meta_style)
        story.append(meta)

    # Tags
    if recipe_data['tags']:
        tags = Paragraph(f"<b>Tags:</b> {recipe_data['tags']}", meta_style)
        story.append(tags)

    story.append(Spacer(1, 0.3*inch))

    # Ingredients
    if recipe_data['ingredients']:
        ingredients_heading = Paragraph("Ingredients", heading_style)
        story.append(ingredients_heading)

        for ingredient in recipe_data['ingredients']:
            # Add checkbox symbol
            ingredient_text = f"☐ {ingredient}"
            ingredient_para = Paragraph(ingredient_text, body_style)
            story.append(ingredient_para)

        story.append(Spacer(1, 0.2*inch))

    # Instructions
    if recipe_data['instructions']:
        instructions_heading = Paragraph("Step-by-Step Instructions", heading_style)
        story.append(instructions_heading)

        # Process instructions - handle numbered lists
        instructions_lines = recipe_data['instructions'].split('\n')
        for line in instructions_lines:
            if line.strip():
                instruction_para = Paragraph(line.strip(), body_style)
                story.append(instruction_para)

        story.append(Spacer(1, 0.2*inch))

    # Notes
    if recipe_data['notes']:
        notes_heading = Paragraph("Notes & Substitutions", heading_style)
        story.append(notes_heading)

        notes_lines = recipe_data['notes'].split('\n')
        for line in notes_lines:
            if line.strip():
                note_para = Paragraph(line.strip(), body_style)
                story.append(note_para)

    # Build PDF
    doc.build(story)

    # Get PDF content
    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content
