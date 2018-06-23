"""Main."""


def main():
    """Run main."""
    from pydocument import doc, docx_parser, templater
    a = doc('demo2.docx')
    t = templater(a, 'settings.json', 'output', ('contract', 'NAME', ' '))
    docx_parser.parse(a)
    a.save('output.docx')

main()
