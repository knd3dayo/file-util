import base64
import os
from magika import Magika
from magika.types import MagikaResult 
from chardet.universaldetector import UniversalDetector
from pathlib import Path
from file_util.core.excel_util import ExcelUtil
from file_util.core.ppt_util import PPTUtil
from file_util.core.word_util import WordUtil
from file_util.core.text_util import TextUtil
from file_util.core.pdf_util import PDFUtil

from pydantic import BaseModel, Field
import file_util.log.log_settings as log_settings
logger = log_settings.getLogger(__name__)


class DocumentType(BaseModel):
    mime_type: str = Field(..., description="MIME type of the document type")

    def is_text(self) -> bool:
        """Check if the document type is a text type based on its MIME type."""
        return self.mime_type.startswith("text/")
    
    def is_pdf(self) -> bool:
        """Check if the document type is a PDF type based on its MIME type."""
        return self.mime_type == "application/pdf"
    
    def is_excel(self) -> bool:
        """Check if the document type is an Excel type based on its MIME type."""
        return self.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    def is_word(self) -> bool:
        """Check if the document type is a Word type based on its MIME type."""
        return self.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    def is_ppt(self) -> bool:
        """Check if the document type is a PowerPoint type based on its MIME type."""
        return self.mime_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    
    def is_image(self) -> bool:
        """Check if the document type is an image type based on its MIME type."""
        return self.mime_type.startswith("image/")
    
    def is_office_document(self) -> bool:
        """Check if the document type is any Office document type based on its MIME type."""
        return self.is_excel() or self.is_word() or self.is_ppt()
    
    def is_unsupported(self) -> bool:
        """Check if the document type is unsupported based on its MIME type."""
        return not (self.is_text() or self.is_pdf() or self.is_office_document() or self.is_image())
    
class FileUtil:
    """ファイル操作のユーティリティクラス"""

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """テキストをサニタイズする

        複数の改行や空白を1つにまとめて、テキストを整形します。

        Args:
            text: サニタイズ対象のテキスト

        Returns:
            サニタイズされたテキスト。入力が空の場合は空文字列
        """
        # textが空の場合は空の文字列を返す
        if not text or len(text) == 0:
            return ""
        import re
        # 1. 複数の改行を1つの改行に変換
        text = re.sub(r'\n+', '\n', text)
        # 2. 複数のスペースを1つのスペースに変換
        text = re.sub(r' +', ' ', text)

        return text

    @classmethod
    def identify_type(cls, filename):
        """ファイルのMIMEタイプとエンコーディングを判定する

        Args:
            filename: 判定対象のファイルパス

        Returns:
            tuple[MagikaResult | None, str | None]:
                MagikaResultオブジェクトとエンコーディング文字列のタプル。
                判定失敗時は(None, None)
        """
        m = Magika()
        # ファイルの種類を判定
        path = Path(filename)
        try:
            res: MagikaResult = m.identify_path(path) # type: ignore
            encoding = None
            if res.dl.is_text:
                encoding = cls.get_encoding(filename)
        except Exception as e:
            logger.debug(e)
            return None, None

        return res, encoding

    @classmethod
    def get_encoding(cls, filename):
        """ファイルのエンコーディングを判定する

        ファイルの先頭8192バイトを読み込んで、エンコーディングを判定します。

        Args:
            filename: 判定対象のファイルパス

        Returns:
            str | None: エンコーディング文字列。判定失敗時はNone
        """
        # ファイルのbyte列を取得
        # アクセスできない場合は例外をキャッチ
        try:
            with open(filename, "rb") as f:
                # 1KB読み込む
                byte_data = f.read(8192)
                if not byte_data:
                    return None, None
        except Exception as e:
            logger.error(e)
            import traceback
            logger.error(traceback.format_exc())

            return None, None
        # エンコーディング判定
        encoding = cls.get_encoding_from_bytes(byte_data)
        return encoding
    
    @classmethod
    def get_encoding_from_bytes(cls, byte_data: bytes):
        """バイト列からエンコーディングを判定する

        Args:
            byte_data: 判定対象のバイト列

        Returns:
            str: エンコーディング文字列
        """
        detector = UniversalDetector()
        detector.feed(byte_data)
        detector.close()
        encoding = detector.result['encoding']  
        return encoding

    @classmethod
    def get_mime_type(cls, filename):
        """ファイルのMIMEタイプを取得する

        Args:
            filename: 対象ファイルパス

        Returns:
            str | None: MIMEタイプ文字列。判定失敗時はNone
        """
        res, encoding = cls.identify_type(filename)
        if res is None:
            return None
        return res.output.mime_type

    @classmethod
    async def extract_text_from_file_async(cls, filename) -> str:
        """ファイルからテキストを非同期で抽出する

        対応形式: テキストファイル、PDF、Excel、Word、PowerPoint

        Args:
            filename: 抽出対象のファイルパス

        Returns:
            str: 抽出されたテキスト。サニタイズ済み。非対応形式の場合は空文字列
        """
        res, encoding = cls.identify_type(filename)
        
        if res is None:
            return ""
        logger.debug(res.output.mime_type)
        result = None        
        document_type = DocumentType(mime_type=res.output.mime_type)
        if document_type.is_text():
            # テキストファイルの場合
            result = await TextUtil.process_text_async(filename, res, encoding)

        # application/pdf
        elif document_type.is_pdf():
            result = PDFUtil.extract_text_from_pdf(filename)
            
        # application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
        elif document_type.is_excel():
            result = ExcelUtil.extract_text_from_sheet(filename)
            
        # application/vnd.openxmlformats-officedocument.wordprocessingml.document
        elif document_type.is_word():
            result = WordUtil.extract_text_from_docx(filename)
            
        # application/vnd.openxmlformats-officedocument.presentationml.presentation
        elif document_type.is_ppt():
            result = PPTUtil.extract_text_from_pptx(filename)

        else:
            logger.error("Unsupported file type: " + res.output.mime_type)

        return cls.sanitize_text(result if result is not None else "")

    @classmethod
    async def extract_base64_to_text(cls, extension: str, base64_data: str) -> str:

        # サイズが0の場合は空文字を返す
        if not base64_data or len(base64_data) == 0:
            return ""

        # base64からバイナリデータに変換
        base64_data_bytes = base64.b64decode(base64_data)

        # 拡張子の指定。extensionがNoneまたは空の場合は設定しない.空でない場合は"."を先頭に付与
        suffix = ""
        if extension is not None and extension != "":
            suffix = "." + extension
        # base64データから一時ファイルを生成
        import aiofiles.tempfile
        async with aiofiles.tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=suffix) as temp:
            await temp.write(base64_data_bytes)
            await temp.close()
            # 一時ファイルからテキストを抽出
            temp_path = temp.name if isinstance(temp.name, str) else str(temp.name)
            text = await FileUtil.extract_text_from_file_async(temp_path)
            # 一時ファイルを削除
            os.remove(temp_path)
            return text

        return text
