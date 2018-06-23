"""Main."""


def main():
    """Run main."""
    from pydocument import doc, templater
    a = doc('demo2.docx')
    t = templater(a, 'settings.json', 'output', ('contract', 'NAME', ' '))
    t.generate(10)


main()
