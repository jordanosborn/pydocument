"""Main."""


def main():
    """Run main."""
    from pydocument import doc, docx_parser
    a = doc('demo2.docx')

    docx_parser.parse(a)
    a.save('output.docx')

main()
