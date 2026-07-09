from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "CV_RitheshKumar.pdf"
TEXT_WIDTH = letter[0] - (2 * 0.72 * inch)
DATE_WIDTH = 1.12 * inch
LOGO_SIZE = 10
LOGOS = {
    "openai": str(ROOT / "img" / "cv-openai.png"),
    "adobe": str(ROOT / "img" / "cv-adobe.png"),
    "descript": str(ROOT / "img" / "cv-descript.png"),
}


def link(text, url, underline=False):
    if underline:
        text = f"<u>{text}</u>"
    return f'<link href="{url}" color="black">{text}</link>'


styles = getSampleStyleSheet()

title = ParagraphStyle(
    "Title",
    parent=styles["Normal"],
    fontName="Times-Bold",
    fontSize=20,
    leading=23,
    alignment=TA_CENTER,
    spaceAfter=5,
)

subtitle = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontName="Times-Roman",
    fontSize=10.5,
    leading=13,
    alignment=TA_CENTER,
    spaceAfter=2,
)

contact = ParagraphStyle(
    "Contact",
    parent=styles["Normal"],
    fontName="Times-Roman",
    fontSize=9.5,
    leading=12,
    alignment=TA_CENTER,
    spaceAfter=16,
)

section = ParagraphStyle(
    "Section",
    parent=styles["Normal"],
    fontName="Times-Bold",
    fontSize=10.2,
    leading=12,
    spaceBefore=8,
    spaceAfter=3,
    textTransform="uppercase",
)

body = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Times-Roman",
    fontSize=9.3,
    leading=11.8,
    spaceAfter=5,
)

small = ParagraphStyle(
    "Small",
    parent=body,
    fontSize=8.8,
    leading=11.2,
    spaceAfter=4,
)

entry_title = ParagraphStyle(
    "EntryTitle",
    parent=styles["Normal"],
    fontName="Times-Bold",
    fontSize=9.5,
    leading=11.6,
    spaceBefore=2,
    spaceAfter=1,
)

date_style = ParagraphStyle(
    "Date",
    parent=styles["Normal"],
    fontName="Times-Roman",
    fontSize=8.9,
    leading=11.6,
    alignment=TA_RIGHT,
    textColor=colors.black,
)

right_detail = ParagraphStyle(
    "RightDetail",
    parent=styles["Normal"],
    fontName="Times-Roman",
    fontSize=8.8,
    leading=11.2,
    alignment=TA_RIGHT,
    textColor=colors.black,
)

entry_body = ParagraphStyle(
    "EntryBody",
    parent=body,
    leftIndent=0,
    spaceAfter=6,
)

pub = ParagraphStyle(
    "Publication",
    parent=small,
    leftIndent=19,
    firstLineIndent=-19,
    spaceAfter=4,
)

venue_group = ParagraphStyle(
    "VenueGroup",
    parent=small,
    fontName="Times-Bold",
    fontSize=8.7,
    leading=10.6,
    spaceBefore=2,
    spaceAfter=1,
)


def section_header(text):
    return [
        Paragraph(text.upper(), section),
        HRFlowable(width="100%", thickness=0.45, color=colors.black, spaceBefore=0, spaceAfter=4),
    ]


def title_with_logo(text, logo_path=None, content_width=TEXT_WIDTH - DATE_WIDTH):
    title_text = Paragraph(f"<b>{text}</b>", entry_title)
    if not logo_path:
        return title_text
    logo = Image(logo_path, width=LOGO_SIZE, height=LOGO_SIZE)
    logo_table = Table(
        [[logo, title_text]],
        colWidths=[0.17 * inch, content_width - 0.17 * inch],
        hAlign="LEFT",
    )
    logo_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, 0), 3),
                ("RIGHTPADDING", (1, 0), (1, 0), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return logo_table


def annotated_item(date, title_flowable, detail_flowables, bottom_padding=3):
    table = Table(
        [[title_flowable, Paragraph(date, date_style)]],
        colWidths=[TEXT_WIDTH - DATE_WIDTH, DATE_WIDTH],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, -1), 8),
                ("RIGHTPADDING", (1, 0), (1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return KeepTogether([table, *detail_flowables, Spacer(1, bottom_padding)])


def entry(role, date, description, logo_path=None):
    descriptions = description if isinstance(description, list) else [description]
    return annotated_item(
        date,
        title_with_logo(role, logo_path),
        [Paragraph(item, entry_body) for item in descriptions],
    )


def education_entry(date, degree, institution, stats, notes=None):
    flowables = [Paragraph(stats, small)]
    if notes:
        flowables.append(Paragraph(notes, small))
    return annotated_item(
        date,
        Paragraph(f"<b>{degree}</b>, <b>{institution}</b>", entry_title),
        flowables,
    )


def product_entry(date, name, description, url):
    return annotated_item(
        date,
        Paragraph(f"<b>{link(name, url)}</b>", entry_title),
        [Paragraph(description, small)],
        bottom_padding=2,
    )


story = []

story.append(Paragraph("Rithesh Kumar", title))
story.append(Paragraph("Member of Technical Staff, OpenAI", subtitle))
story.append(
    Paragraph(
        "San Francisco, CA &nbsp;|&nbsp; "
        "+1 510-318-0216 &nbsp;|&nbsp; "
        f"{link('ritheshkumar.95@gmail.com', 'mailto:ritheshkumar.95@gmail.com', True)} &nbsp;|&nbsp; "
        f"{link('ritheshkumar.com', 'https://ritheshkumar.com', True)}",
        contact,
    )
)

story.extend(section_header("Research Focus"))
story.append(
    Paragraph(
        "I work on building realtime interface to AGI at OpenAI. My work spans voice assistants, "
        "generative audio, speech synthesis, diffusion models, efficient distillation and "
        "text-based audio editing. My research has been rooted in the fundamentals of generative "
        "modeling and deep learning since 2016.",
        body,
    )
)

story.extend(section_header("Experience"))
story.append(
    entry(
        "Member of Technical Staff, OpenAI",
        "2025-present",
        "Building next-generation voice interfaces to AGI.",
        LOGOS["openai"],
    )
)
story.append(
    entry(
        "Senior Research Scientist, Adobe Research",
        "2023-2025",
        "Led speech generation research for controllable text-to-speech synthesis, automatic dubbing, "
        f"and speech editing. Shipped core models behind Adobe Firefly {link('Translate Video and Audio', 'https://firefly.adobe.com/upload/translate')}, "
        "Text-to-Avatar, and Adobe TTS API. Developed broadcast-quality audio diffusion models and efficient "
        "distillation algorithms for voice translation and controllable TTS across 25+ languages and dialects.",
        LOGOS["adobe"],
    )
)
story.append(
    entry(
        "Technical Lead, Audio Research, Descript (prev. Lyrebird)",
        "2019-2023",
        "Led audio research across neural text-to-speech, voice cloning, speech editing, and audio language "
        f"modeling. Shipped 4+ research models powering {link('Overdub', 'https://www.descript.com/overdub')}, "
        f"{link('Regenerate', 'https://www.descript.com/regenerate')}, and AI Voices. Developed audio language models "
        "and high-fidelity voice cloning systems for text-based speech correction and 44.1 kHz voice generation.",
        LOGOS["descript"],
    )
)

story.extend(section_header("Shipped Products"))
products = [
    (
        "GPT Live 1",
        "2026",
        "A new generation of voice models for natural human-AI interaction, now powering ChatGPT Voice.",
        "https://openai.com/index/introducing-gpt-live/",
    ),
    (
        "Adobe Firefly Translate Video and Audio, Text-to-Avatar",
        "2025",
        "Speaker-preserving voice translation for multilingual media workflows, plus voice generation for animated avatars.",
        "https://firefly.adobe.com/upload/translate",
    ),
    (
        "Descript Regenerate",
        "2023",
        "Speech editing and audio repair that turns awkward cuts, gaps, and retakes into smooth generated speech.",
        "https://www.descript.com/regenerate",
    ),
    (
        "Descript AI Voices / Overdub",
        "2018",
        "Voice cloning and text-to-speech systems behind Overdub and later AI voice creation workflows.",
        "https://www.descript.com/ai-voices",
    ),
]
for name, date, desc, url in products:
    story.append(product_entry(date, name, desc, url))

story.extend(section_header("Education"))
story.append(
    education_entry(
        "2017-2019",
        "M.Sc., Computer Science",
        f"{link('Mila', 'https://mila.quebec/en')} - Universite de Montreal",
        "CGPA: 4.15 / 4.3.",
        "Supervised by Prof. "
        f"{link('Yoshua Bengio', 'http://www.iro.umontreal.ca/~bengioy/yoshua_en/')}. "
        "Thesis: Maximum Entropy Generators for Energy-Based Models.",
    )
)
story.append(
    education_entry(
        "2013-2017",
        "B.E., Computer Science and Engineering",
        "Anna University",
        "CGPA: 8.63 / 10.0",
        "Rank: 46 among 16,449 candidates.",
    )
)

story.append(PageBreak())
story.extend(section_header("Publications"))
publication_groups = [
    (
        "ICML",
        [
            (
                "AudioChat: Unified Audio Storytelling, Editing, and Understanding with Transfusion Forcing",
                "ICML 2026",
                "William Chen, Prem Seetharaman, Rithesh Kumar, Oriol Nieto, Shinji Watanabe, Justin Salamon, Zeyu Jin",
                "https://arxiv.org/abs/2602.17097",
                "",
            ),
            (
                "DMOSpeech: Direct Metric Optimization via Distilled Diffusion Model in Zero-Shot Speech Synthesis",
                "ICML 2025",
                "Yinghao Aaron Li, Rithesh Kumar, Zeyu Jin",
                "https://arxiv.org/abs/2410.11097",
                "",
            ),
        ],
    ),
    (
        "ICLR",
        [
            (
                "SpeechOp: Inference-Time Task Composition for Generative Speech Processing",
                "ICLR 2026",
                "Justin Lovelace, Rithesh Kumar, Jiaqi Su, Ke Chen, Kilian Q. Weinberger, Zeyu Jin",
                "https://arxiv.org/abs/2509.14298",
                "",
            ),
            (
                "Chunked Autoregressive GAN for Conditional Waveform Synthesis",
                "ICLR 2022",
                "Max Morrison, Rithesh Kumar, Kundan Kumar, Prem Seetharaman, Aaron Courville, Yoshua Bengio",
                "https://arxiv.org/abs/2110.10139",
                "",
            ),
            (
                "SampleRNN: An Unconditional End-to-End Neural Audio Generation Model",
                "ICLR 2017",
                "Soroush Mehri, Kundan Kumar, Ishaan Gulrajani, Rithesh Kumar, Shubham Jain, Jose Sotelo, Aaron Courville, Yoshua Bengio",
                "https://arxiv.org/abs/1612.07837",
                "",
            ),
        ],
    ),
    (
        "NeurIPS",
        [
            (
                "High-Fidelity Audio Compression with Improved RVQGAN",
                "NeurIPS 2023",
                "Rithesh Kumar, Prem Seetharaman, Alejandro Luebs, Ishaan Kumar, Kundan Kumar",
                "https://arxiv.org/abs/2306.06546",
                "Spotlight.",
            ),
            (
                "MelGAN: Generative Adversarial Networks for Conditional Waveform Synthesis",
                "NeurIPS 2019",
                "Kundan Kumar, Rithesh Kumar, Thibault de Boissiere, Lucas Gestin, Wei Zhen Teoh, Jose Sotelo, Alexandre de Brebisson, Yoshua Bengio, Aaron Courville",
                "https://arxiv.org/abs/1910.06711",
                "",
            ),
        ],
    ),
    (
        "ICASSP",
        [
            (
                "Taming Audio VAEs via Target-KL Regularization",
                "ICASSP 2026",
                "Prem Seetharaman*, Rithesh Kumar*",
                "https://arxiv.org/abs/2605.17085",
                "Equal contribution.",
            ),
            (
                "PromptSep: Generative Audio Separation via Multimodal Prompting",
                "ICASSP 2026",
                "Yutong Wen, Ke Chen, Prem Seetharaman, Oriol Nieto, Jiaqi Su, Rithesh Kumar, Minje Kim, Paris Smaragdis, Zeyu Jin, Justin Salamon",
                "https://arxiv.org/abs/2511.04623",
                "",
            ),
            (
                "DiTSE: High-Fidelity Generative Speech Enhancement via Latent Diffusion Transformers",
                "ICASSP 2026",
                "Heitor R. Guimaraes, Jiaqi Su, Rithesh Kumar, Tiago H. Falk, Zeyu Jin",
                "https://arxiv.org/abs/2504.09381",
                "",
            ),
        ],
    ),
    (
        "ISMIR",
        [
            (
                "VampNet: Music Generation via Masked Acoustic Token Modeling",
                "ISMIR 2023",
                "Hugo Flores Garcia, Prem Seetharaman, Rithesh Kumar, Bryan Pardo",
                "https://arxiv.org/abs/2307.04686",
                "",
            ),
        ],
    ),
    (
        "WASPAA",
        [
            (
                "DiTVC: One-Shot Voice Conversion via Diffusion Transformer with Environment and Speaking Rate Cloning",
                "WASPAA 2025",
                "Yunyun Wang, Jiaqi Su, Adam Finkelstein, Rithesh Kumar, Ke Chen, Zeyu Jin",
                "https://doi.org/10.1109/WASPAA66052.2025.11230986",
                "",
            ),
        ],
    ),
    (
        "CHI",
        [
            (
                "SpeakEasy: Enhancing Text-to-Speech Interactions for Expressive Content Creation",
                "CHI 2025",
                "Stephen Brade, Sam Anderson, Rithesh Kumar, Zeyu Jin, Anh Truong",
                "https://arxiv.org/abs/2504.05106",
                "",
            ),
        ],
    ),
    (
        "Thesis / Preprints / Other",
        [
            (
                "TAC: Timestamped Audio Captioning",
                "2026",
                "Sonal Kumar, Prem Seetharaman, Ke Chen, Oriol Nieto, Jiaqi Su, Zhepei Wang, Rithesh Kumar, Dinesh Manocha, Nicholas J. Bryan, Zeyu Jin, Justin Salamon",
                "https://arxiv.org/abs/2602.15766",
                "",
            ),
            (
                "NU-GAN: High resolution neural upsampling with GAN",
                "2020",
                "Rithesh Kumar, Kundan Kumar, Vicki Anand, Yoshua Bengio, Aaron Courville",
                "https://arxiv.org/abs/2010.11362",
                "",
            ),
            (
                "Maximum Entropy Generators for Energy-Based Models",
                "M.Sc. Thesis, 2019",
                "Rithesh Kumar, Sherjil Ozair, Anirudh Goyal, Aaron Courville, Yoshua Bengio",
                "https://arxiv.org/abs/1901.08508",
                "",
            ),
            (
                "Harmonic Recomposition using Conditional Autoregressive Modeling",
                "2018",
                "Kyle Kastner, Rithesh Kumar, Tim Cooijmans, Aaron Courville",
                "https://arxiv.org/abs/1811.07426",
                "",
            ),
            (
                "ObamaNet: Photo-realistic lip-sync from text",
                "2017",
                "Rithesh Kumar, Jose Sotelo, Kundan Kumar, Alexandre de Brebisson, Yoshua Bengio",
                "https://arxiv.org/abs/1801.01442",
                "",
            ),
        ],
    ),
]
pub_index = 1
for group_name, group_items in publication_groups:
    story.append(Paragraph(group_name, venue_group))
    for name, venue, authors, url, note in group_items:
        note_text = f" {note}" if note else ""
        story.append(Paragraph(f"[{pub_index}] {authors}. \"{link(name, url)}.\" <i>{venue}</i>.{note_text}", pub))
        pub_index += 1

OUT.parent.mkdir(parents=True, exist_ok=True)

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=letter,
    rightMargin=0.72 * inch,
    leftMargin=0.72 * inch,
    topMargin=0.62 * inch,
    bottomMargin=0.62 * inch,
    title="CV_RitheshKumar",
    author="Rithesh Kumar",
)

doc.build(story)
print(OUT)
