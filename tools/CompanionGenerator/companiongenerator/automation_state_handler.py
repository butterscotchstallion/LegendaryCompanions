class AutomationStateHandler:
    """
    Handles name -> identifier mappings
    Automation state such as isDryRun
    """

    run_id: int | None = None
    is_dry_run: bool = True

    def set_is_dry_run(self, is_dry_run: bool) -> None:
        """
        Whether this should be a dry run where we don't actually
        write or edit any files
        """
        self.is_dry_run = is_dry_run
