from companiongenerator.template_fetcher import TemplateFetcher
from companiongenerator.template_variable_replacer import TemplateVariableReplacer


class TemplateReplacerBase:
    """
    Template replacement functionality which is used
    in a few places
    """

    def __init__(self):
        self.filename = ""
        self.replacements = {}
        self.template_fetcher = TemplateFetcher()

    def _get_template_text(self):
        """
        Fetches template from filesystem
        """
        return self.template_fetcher.get_template_text(self.filename).strip()

    def get_tpl_with_replacements(self):
        """
        Replaces using map
        """
        tpl_text = self._get_template_text()
        replacer = TemplateVariableReplacer()
        return replacer.replace_placeholders(tpl_text, self.replacements)
