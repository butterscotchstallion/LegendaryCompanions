from uuid import uuid4


class AutomationStateHandler:
    """
    Handles state management for each automation run
    """

    run_id: str
    is_dry_run: bool = True

    def __init__(self):
        self.run_id = uuid4()

    def set_is_dry_run(self, is_dry_run: bool) -> None:
        """
        Whether this should be a dry run where we don't actually
        write or edit any files
        """
        self.is_dry_run = is_dry_run
