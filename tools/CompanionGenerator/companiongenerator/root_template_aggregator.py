from companiongenerator.file_handler import FileHandler


class RootTemplateAggregator:
    def __init__(self, **kwargs):
        self.file_handler = FileHandler(is_dry_run=kwargs["is_dry_run"])
        self.rt_xml_list: list[str] = []

    def add_entry(self, entry: str, comment: str):
        entry_with_comment = f"<!-- {comment} -->\n{entry}"
        self.rt_xml_list.append(entry_with_comment)

    def write_root_template(self, file_path: str) -> bool:
        return self.file_handler.write_string_to_file(
            file_path, "\n".join(self.rt_xml_list)
        )

    def get_rt_xml_list(self):
        return self.rt_xml_list
