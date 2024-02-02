from companiongenerator.file_handler import FileHandler
from companiongenerator.root_template_node_entry import RootTemplateNodeEntry
from companiongenerator.root_template_parser import RootTemplateParser


class RootTemplateAggregator:
    def __init__(self, **kwargs) -> None:
        self.file_handler = FileHandler(is_dry_run=kwargs["is_dry_run"])
        self.root_template_parser = RootTemplateParser()
        self.entries: list[RootTemplateNodeEntry] = []

    def add_entry(self, rt_xml: str, comment: str):
        self.entries.append(
            RootTemplateNodeEntry(
                # comment=f"<!--{comment}-->",
                comment=comment,
                root_template_xml=rt_xml,
            )
        )

    def write_root_template(self, file_path: str) -> bool | None:
        xml_merged_str = self.root_template_parser.append_nodes_to_children(
            "./companiongenerator/templates/merged.lsx", self.entries
        )

        if xml_merged_str:
            return self.file_handler.write_string_to_file(file_path, xml_merged_str)
