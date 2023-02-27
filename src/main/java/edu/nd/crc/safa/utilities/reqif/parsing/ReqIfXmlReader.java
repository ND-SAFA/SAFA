package edu.nd.crc.safa.utilities.reqif.parsing;

import javax.xml.stream.XMLStreamReader;
import javax.xml.stream.util.StreamReaderDelegate;

/**
 * This class is used to strip namespace information out of XML files. Otherwise,
 * XML files which do not have exact matching namespaces will fail to be parsed
 * despite having correct data.
 */
public class ReqIfXmlReader extends StreamReaderDelegate {

    public ReqIfXmlReader(XMLStreamReader paramXMLStreamReader) {
        super(paramXMLStreamReader);
    }

    @Override
    public String getAttributeNamespace(int paramInt) {
        return "";
    }

    @Override
    public String getNamespaceURI() {
        return "";
    }

}
