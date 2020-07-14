import io
import re
import codecs

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):  # not my part of code. PDF-miner
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def main():
    #  Converting PDF file to txt format. Blocking method is quite dirty & will be updated.

    new_file = open("PATH_HERE", mode="w+", encoding="utf-8")

    new_file.write(convert_pdf_to_txt("PATH_HERE"))
    new_file.close()

    # Removing symbols from clipboard & re-writing into new file

    symbols = ["•", "·", "—", "", "�"]

    with codecs.open("PATH_HERE", "r", "utf_8_sig") as infile, \
            codecs.open("PATH_HERE", "w", "utf_8_sig") as outfile:
        in_cursor = infile.read()

        for symbol in symbols:
            in_cursor = in_cursor.replace(symbol, " ")

        outfile.write(in_cursor)

    # transforming paragraphs into solid strings & re-writing into new file

    with open("PATH_HERE", "r+", encoding="utf-8") as searchfile, \
            open("PATH_HERE", "w+", encoding="utf-8") as newfile:

        lines = searchfile.readlines()
        newline = ''

        for line in lines:
            line = line[:-1]

            # removing unnecessary parts in block starting with 'bracket_text'

            if len(line) == line.rfind('.') + 1 > 0:
                newline += line + '\n\n'

                bracket_text = re.search("\[.*?\]", newline)  # finding text in [] brackets
                bracket_digit = re.search("\({1}\d+\){1}", newline)  # finding digits in () brackets
                hashtag_digit = re.search("\({1}#\d+\){1}", newline)  # finding hash-tagged digits

                if bracket_text or bracket_digit or hashtag_digit:
                    newline = re.sub("\[.*?\]", "", re.sub("\({1}\d+\){1}", " ", re.sub("\({1}#\d+\){1}", "", newline)))

                print('writing line: ', newline)
                newfile.writelines(newline)
                newline = ''

            elif len(line) > 0:
                print('adding: ', line)
                newline += line + ' '

                bracket_text = re.search("\[.*?\]", newline)

                if bracket_text:
                    newline = re.sub("\[.*?\]", "", newline)

            else:
                pass

        newfile.writelines(newline[:-1] + '.')


if __name__ == "__main__":
    main()
