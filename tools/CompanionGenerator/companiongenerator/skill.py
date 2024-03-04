from companiongenerator.template_replacer_base import TemplateReplacerBase


class Skill(TemplateReplacerBase):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.template_filename = "skill.xml"
        self.replacements = {
            "{{name}}": self.name,
        }
