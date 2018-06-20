"""Main."""


def main():
    """Run main."""
    from pydocument import doc, docx_parser
    a = doc('demo2.docx')

    docx_parser.parse(a)
    print(a)

    b = doc.from_raw('test.txt', 'txt', {'document.txt': b'hello world'})
    print(b)
    print(a.convert('html5'))

main()
