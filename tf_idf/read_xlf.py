import xml.dom.minidom as dom
from .helpers import getText
from zipfile import ZipFile
from .NLP_helpers import preproc, word_frequencies, idf, tf_idf


def read_XLZ(file):
    if file.endswith('.xlf') or file.endswith('.xliff') or file.endswith('.sdlxliff'):
        fh = open(file, 'r', encoding='utf-8')
    elif file.endswith('.xlz'):
        zip = ZipFile(file, 'r')
        for filename in ZipFile.namelist(zip):
            if filename.endswith('.xlf') or filename.endswith('.xliff'):
                fh = zip.open(filename)
    #elif PATH.endswith('.sdlxliff'):
    #    fh = open(PATH, 'r', encoding='utf-8')
    # elif file.endswith('.xml'):
    #     fh = open(file, 'r', encoding='utf-8')
    else:
        raise Exception('File {} is not in XLIFF format. We only work with XLIFF files, sorry :('.format(file))
    return dom.parse(fh).documentElement


def get_words(files):
    words = []
    for filename in files:
        doc = read_XLZ(filename)
        for el in doc.getElementsByTagName('source'):
            raw = getText(el.childNodes)
            words += preproc(raw)
    return words


if __name__ == '__main__':
    # argvs: files, term length
    # files = ["test.xml", "test.xlz", 'test.sdlxliff', 'test.xlf']

    # prep
    files = ["test.xlz"]
    words = get_words(files)

    # calc tf_idf
    tfs = word_frequencies(words)
    idfs = idf(tfs.keys())
    tf_idf_gen = tf_idf(tfs, idfs)

    # write to file
    with open('export.csv', 'w') as CSV:
        counter = 0
        while counter < 10:
            # print(next(tf_idf_gen)[0])
            CSV.write(next(tf_idf_gen)[0] + '\n')
            counter += 1
        CSV.close()
