from companiongenerator.constants import MOD_FILENAMES
from companiongenerator.file_handler import FileHandler
from companiongenerator.root_template_node_entry import RootTemplateNodeEntry
from companiongenerator.root_template_parser import RootTemplateParser


class RootTemplateAggregator:
    def __init__(self, **kwargs) -> None:
        self.file_handler = FileHandler(is_dry_run=kwargs["is_dry_run"])
        self.root_template_parser = RootTemplateParser()
        self.entries: set[RootTemplateNodeEntry] = set([])

    def add_entry(self, rt_xml: str, comment: str, name: str):
        self.entries.add(
            RootTemplateNodeEntry(
                comment=comment,
                root_template_xml=rt_xml,
                name=name,
            )
        )

    def append_root_template(self) -> bool | None:
        """
        1. Find existing backups, if any
        2. Overwrite existing backup if exists, or create new one
        3. Parse RT and append new nodes to it
        4. If write successful, remove backup

        Args:
            file_path (str): Path to root template

        Returns:
            bool | None: Returns true if successful
        """
        xml_merged_str = self.root_template_parser.append_nodes_to_children(
            MOD_FILENAMES["root_template_merged"], self.entries
        )

        if xml_merged_str:
            # Returns None
            self.root_template_parser.write()
            return True
