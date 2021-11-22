from datetime import datetime
from decimal import Decimal
from typing import Tuple
from api.transcripts.models import TranscriptModel

from api.users.models import UserModel
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.page_layout.multi_column_layout import \
    SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import \
    FixedColumnWidthTable
from borb.pdf.canvas.layout.table.flexible_column_width_table import \
    FlexibleColumnWidthTable
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from flask import current_app


class ReportService:
    @classmethod
    def make_report_users(cls) -> None:
        pdf, layout = cls._init_pdf()
        cls._create_header(layout, 'Listagem de Usuários da Plataforma.')
        cls._insert_users_info(layout)
        cls._save_report(pdf, 'all_users')

    @classmethod
    def make_report_transcripts(cls) -> None:
        pdf, layout = cls._init_pdf()
        cls._create_header(layout, 'Listagem de Transcrições da Plataforma.')
        cls._insert_transcripts_info(layout)
        cls._save_report(pdf, 'all_transcripts')

    @classmethod
    def make_report_user_detail(cls, user: UserModel) -> None:
        pdf, layout = cls._init_pdf()
        cls._create_header(layout, f'Detalhes de usuário: {user.username}')
        cls._insert_user_detail(layout, user)
        cls._save_report(pdf, user.username)

    @staticmethod
    def _init_pdf() -> Tuple[Document, SingleColumnLayout]:
        pdf = Document()
        page = Page()
        pdf.append_page(page)
        layout = SingleColumnLayout(page)
        return pdf, layout

    @staticmethod
    def _save_report(pdf: Document, report_name: str) -> None:
        folder = current_app.config['REPORT_FOLDER']

        with open(f'{folder}/{report_name}.pdf', 'wb') as pdf_file_handle:
            PDF.dumps(pdf_file_handle, pdf)

    @staticmethod
    def _insert_users_info(layout: SingleColumnLayout) -> None:
        layout.add(
            FixedColumnWidthTable(number_of_columns=2, number_of_rows=1, padding_top=Decimal(20))
            .add(Paragraph('ID'))
            .add(Paragraph('Username'))
            .no_borders()
        )

        users = UserModel.query.all()

        table = FixedColumnWidthTable(number_of_columns=2, number_of_rows=len(users))

        for user in users:
            table.add(Paragraph(f'{user.id}'))
            table.add(Paragraph(user.username))

        layout.add(table.no_borders())

    @staticmethod
    def _insert_transcripts_info(layout: SingleColumnLayout) -> None:
        layout.add(
            FixedColumnWidthTable(number_of_columns=4, number_of_rows=1, padding_top=Decimal(20))
            .add(Paragraph('ID'))
            .add(Paragraph('Text'))
            .add(Paragraph('Create At'))
            .add(Paragraph('Username'))
            .no_borders()
        )

        transcripts = TranscriptModel.query.all()

        table = FixedColumnWidthTable(number_of_columns=4, number_of_rows=len(transcripts))

        for transcript in transcripts:
            table.add(Paragraph(f'{transcript.id}', padding_right=Decimal(5)))
            table.add(Paragraph(transcript.text, padding_right=Decimal(5)))
            table.add(Paragraph(str(transcript.create_at), padding_right=Decimal(5)))
            table.add(Paragraph(transcript.user.username, padding_right=Decimal(5)))

        layout.add(table.no_borders())

    @staticmethod
    def _insert_user_detail(layout: SingleColumnLayout, user: UserModel) -> None:
        layout.add(Paragraph('User Data', font_color=HexColor('#2fb5c0'), font_size=Decimal(12), padding_top=Decimal(10)))

        layout.add(
            FixedColumnWidthTable(number_of_columns=1, number_of_rows=2)
            .add(Paragraph(f'ID: {user.id}'))
            .add(Paragraph(f'Email: {user.username}'))
            .no_borders()
        )

        layout.add(Paragraph('Transcripts Data', font_color=HexColor('#2fb5c0'), font_size=Decimal(12), padding_top=Decimal(10)))

        layout.add(
            FixedColumnWidthTable(number_of_columns=4, number_of_rows=1)
            .add(Paragraph('ID'))
            .add(Paragraph('Text'))
            .add(Paragraph('Create At'))
            .add(Paragraph('Username'))
            .no_borders()
        )

        transcripts = TranscriptModel.query.join(UserModel).\
            filter(UserModel.username == user.username)

        table = FixedColumnWidthTable(number_of_columns=4, number_of_rows=transcripts.count())

        for transcript in transcripts:
            table.add(Paragraph(f'{transcript.id}', padding_right=Decimal(5)))
            table.add(Paragraph(transcript.text, padding_right=Decimal(5)))
            table.add(Paragraph(str(transcript.create_at), padding_right=Decimal(5)))
            table.add(Paragraph(transcript.user.username, padding_right=Decimal(5)))

        layout.add(table.no_borders())

    @staticmethod
    def _create_header(layout: SingleColumnLayout, title: str) -> None:
        layout.add(
            FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=2)
            .add(
                TableCell(
                    Image(
                        'https://lirp.cdn-website.com/1180cc12/dms3rep/multi/opt/4Y2-fundo-claro-103w.png',
                        width=Decimal(64),
                        height=Decimal(50),
                    ),
                    row_span=2
                )
            )
            .add(
                Paragraph(
                    title,
                    padding_top=Decimal(10),
                    padding_left=Decimal(10),
                    font_color=HexColor('#666666'),
                    font_size=Decimal(14)
                ))
            .add(
                Paragraph(
                    datetime.now().strftime('%A %d %B, %Y'),
                    padding_left=Decimal(10),
                    font_color=HexColor('#2fb5c0'),
                    font_size=Decimal(11),
                )).no_borders()
        )
