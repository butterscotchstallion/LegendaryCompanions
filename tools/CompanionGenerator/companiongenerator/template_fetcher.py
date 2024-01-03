from pathlib import Path
import logging as log


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
        log.debug("Reading from file system")
        template_path = f"{self.base_path}{filename}"
        try:
            return Path(template_path).read_text()
        except IOError:
            log.error(f"Could not find path {template_path}")
            return ""
