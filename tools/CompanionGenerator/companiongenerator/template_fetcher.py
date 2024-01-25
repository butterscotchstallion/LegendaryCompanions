from pathlib import Path

from companiongenerator.logger import log

logger = log.getLogger(__name__)


class TemplateFetcher:
    """
    Fetches templates from file system path provided
    """

    def __init__(self) -> None:
        self.base_path = "./companiongenerator/templates/"

    def get_template_text(self, filename) -> str:
        """
        Reads template file
        """
        template_path = f"{self.base_path}{filename}"
        return Path(template_path).read_text().strip()
