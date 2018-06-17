"""Main."""


def main():
    """Run main."""
    from pydocument import doc, docx_parser
    a = doc('demo.docx')

    docx_parser.parse(a)


if __name__ == '_main__':
    main()
