from xml.dom.minidom import getDOMImplementation
from xml.dom import minidom
import os


def export_CSV(path, words):
    with open(os.path.join(path, 'export.csv'), 'w', encoding='utf-8') as CSV:
        CSV.write('\n'.join(words))


def export_MultiTerm(path, words):
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "mtf", None)
    top_element = newdoc.documentElement

    for word in words:
        conceptGrp = newdoc.createElement("conceptGrp")
        top_element.appendChild(conceptGrp)
        languageGrp = newdoc.createElement("languageGrp")
        conceptGrp.appendChild(languageGrp)
        language = newdoc.createElement("language")
        # language ID variables - get from XLZ
        language.setAttribute("type", "English")
        language.setAttribute("lang", "EN-US")
        languageGrp.appendChild(language)
        termGrp = newdoc.createElement("termGrp")
        languageGrp.appendChild(termGrp)
        term = newdoc.createElement("term")
        term_text = newdoc.createTextNode(word)
        term.appendChild(term_text)
        termGrp.appendChild(term)

    with open(os.path.join(path, 'MultiTerm_export.xml'), 'w') as tb:
        newdoc.writexml(tb, indent="", newl="\n", addindent='\t', encoding="utf-8")


def export_TBX(path, words):
    # impl = getDOMImplementation()
    # newdoc = impl.createDocument(None, "martif", None)
    newdoc = minidom.Document()
    martif = newdoc.createElement("martif")
    martif.setAttribute("type","TBX")
    martif.setAttribute("xml:lang", "en-US")
    newdoc.appendChild(martif)
    # top_element = newdoc.documentElement
    martifHeader = newdoc.createElement("martifHeader")
    # top_element.appendChild(martifHeader)
    martif.appendChild(martifHeader)
    fileDesc = newdoc.createElement("fileDesc")
    martifHeader.appendChild(fileDesc)
    sourceDesc = newdoc.createElement("sourceDesc")
    fileDesc.appendChild(sourceDesc)
    p = newdoc.createElement("p")
    sourceDesc.appendChild(p)
    p_text = newdoc.createTextNode("Exported from Metamova TF*IDF Glossary Extractor")
    p.appendChild(p_text)
    text = newdoc.createElement("text")
    # top_element.appendChild(text)
    martif.appendChild(text)
    body = newdoc.createElement("body")
    text.appendChild(body)

    for word in words:
        termEntry = newdoc.createElement("termEntry")
        termEntry.setAttribute("id", "0")
        body.appendChild(termEntry)
        langSet = newdoc.createElement("langSet")
        langSet.setAttribute("xml:lang", "EN-GB")
        termEntry.appendChild(langSet)
        tig = newdoc.createElement("tig")
        langSet.appendChild(tig)
        term = newdoc.createElement("term")
        tig.appendChild(term)
        term_text = newdoc.createTextNode(word)
        term.appendChild(term_text)

    with open(os.path.join(path, 'TBX_export.xml'), 'w') as tb:
        newdoc.writexml(tb, indent="", newl="\n", addindent='\t', encoding="utf-8")
