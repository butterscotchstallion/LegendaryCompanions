import logging as log


class TemplateVariableReplacer:
    def replace(self, input_text, replacements) -> str:
        """Replaces template variables and returns text with replacements"""
        replaced_text = input_text
        for replacer_var_name in replacements:
            if replacer_var_name in replaced_text:
                replaced_text = replaced_text.replace(
                    replacer_var_name, replacements[replacer_var_name]
                )
                log.debug(
                    f"Replaced {replacer_var_name} with {replacements[replacer_var_name]}"
                )
            else:
                log.error(
                    f"Could not find replacer variable {replacer_var_name} in template: {replaced_text}"
                )
        return replaced_text
