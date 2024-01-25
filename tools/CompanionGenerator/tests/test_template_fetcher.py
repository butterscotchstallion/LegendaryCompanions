from companiongenerator.template_fetcher import TemplateFetcher


def test_template_fetcher():
    fetcher = TemplateFetcher()
    tpl_contents = fetcher.get_template_text("rt_object_scroll.xml")
    assert len(tpl_contents) > 0
