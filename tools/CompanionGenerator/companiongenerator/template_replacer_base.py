from companiongenerator.template_variable_replacer import TemplateVariableReplacer


class TemplateReplacerBase:
    """
    Template replacement functionality which is used
    in a few places
    """

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
