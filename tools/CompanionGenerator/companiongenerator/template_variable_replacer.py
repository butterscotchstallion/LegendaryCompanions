class TemplateVariableReplacer:
    def replace_placeholders(self, input_text: str, replacements: dict) -> str:
        """Replaces template variables and returns text with replacements"""
        replaced_text = input_text

        if len(replacements) == 0:
            raise RuntimeError("No replacements set!")

        for replacer_var_name in replacements:
            if "{{" not in replacer_var_name or "}}" not in replacer_var_name:
                raise RuntimeError(
                    f"Replacer variable {replacer_var_name} incorrectly formatted!"
                )

            if replacer_var_name in replaced_text:
                replacement = str(replacements[replacer_var_name])
                replaced_text = replaced_text.replace(replacer_var_name, replacement)
            else:
                err_msg = f"Could not find replacer variable '{replacer_var_name}' in template!"
                raise RuntimeError(err_msg)

        return replaced_text
