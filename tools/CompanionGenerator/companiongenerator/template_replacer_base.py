from companiongenerator.logger import logger
from companiongenerator.template_fetcher import TemplateFetcher
from companiongenerator.template_variable_replacer import TemplateVariableReplacer


class TemplateReplacerBase:
    """
    Template replacement functionality which is used
    in a few places
    """

    def __init__(self):
        self.template_filename = ""
        self.replacements = {}
        self.template_fetcher = TemplateFetcher()

    def _get_template_text(self) -> str:
        """
        Fetches template from filesystem
        """
        if self.template_filename:
            return self.template_fetcher.get_template_text(
                self.template_filename
            ).strip()
        else:
            logger.error("No template name defined!")
            return ""

    def get_tpl_with_replacements(self) -> str:
        """
        Replaces using map
        """
        tpl_text = self._get_template_text()
        if tpl_text:
            replacer = TemplateVariableReplacer()
            return replacer.replace_placeholders(tpl_text, self.replacements)
        else:
            return ""
