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
                    "Replaced {name} with {value}",
                    extra=dict(
                        name=replacer_var_name,
                        value=replacements[replacer_var_name],
                    ),
                )
            else:
                log.error(
                    "Could not find replacer variable in template: {name}",
                    extra=dict(name=replacer_var_name),
                )
        return replaced_text
