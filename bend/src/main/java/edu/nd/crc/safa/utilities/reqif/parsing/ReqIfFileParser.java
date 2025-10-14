package edu.nd.crc.safa.utilities.reqif.parsing;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;
import javax.xml.stream.util.StreamReaderDelegate;

import edu.nd.crc.safa.utilities.reqif.datatypes.ReqIf;

import jakarta.xml.bind.JAXBContext;
import jakarta.xml.bind.JAXBException;
import jakarta.xml.bind.Unmarshaller;

/**
 * Contains static functions for parsing ReqIf data.
 */
public interface ReqIfFileParser {

    /**
     * Parse ReqIf data from an XML input stream.
     *
     * @param inputStream Input stream containing ReqIf formatted data.
     * @return Parsed ReqIf content
     */
    static ReqIf parseReqIfFile(InputStream inputStream) throws JAXBException, XMLStreamException {
        XMLInputFactory inputFactory = XMLInputFactory.newInstance();
        inputFactory.setProperty(XMLInputFactory.IS_NAMESPACE_AWARE, false);

        XMLStreamReader streamReader = inputFactory.createXMLStreamReader(inputStream);

        JAXBContext context = JAXBContext.newInstance(ReqIf.class);
        Unmarshaller unmarshaller = context.createUnmarshaller();

        StreamReaderDelegate xmlReader = new StreamReaderDelegate(streamReader);

        return unmarshaller.unmarshal(xmlReader, ReqIf.class).getValue();
    }

    /**
     * Parse ReqIf data from an XML string.
     *
     * @param fileContents String containing ReqIf formatted data.
     * @return Parsed ReqIf content
     */
    static ReqIf parseReqIfFile(String fileContents) throws XMLStreamException, JAXBException {
        InputStream inputStream = new ByteArrayInputStream(fileContents.getBytes(StandardCharsets.UTF_8));
        return parseReqIfFile(inputStream);
    }

    /**
     * Parse ReqIf data from an XML file.
     *
     * @param file File containing ReqIf formatted data.
     * @return Parsed ReqIf content
     */
    static ReqIf parseReqIfFile(File file) throws FileNotFoundException, XMLStreamException, JAXBException {
        FileInputStream inputStream = new FileInputStream(file);
        return parseReqIfFile(inputStream);
    }
}
