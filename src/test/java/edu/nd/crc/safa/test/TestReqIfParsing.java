package edu.nd.crc.safa.test;

import edu.nd.crc.safa.utilities.reqif.ReqIf;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import com.fasterxml.jackson.module.jaxb.JaxbAnnotationModule;
import org.junit.jupiter.api.Test;

public class TestReqIfParsing {

    String file = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" +
        "<REQ-IF xmlns=\"http://www.omg.org/spec/ReqIF/20101201\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.omg.org/spec/ReqIF/20110401/reqif.xsd reqif.xsd http://www.w3.org/1999/xhtml driver.xsd\">\n" +
        "  <THE-HEADER>\n" +
        "    <REQ-IF-HEADER IDENTIFIER=\"3dd1a60c-59d1-11da-86ca-4bda04a730ce\">\n" +
        "      <COMMENT>Embedded OLE object with multiple representation forms.</COMMENT>\n" +
        "      <CREATION-TIME>2005-05-23T12:00:00+02:00</CREATION-TIME>\n" +
        "      <SOURCE-TOOL-ID>Manually written</SOURCE-TOOL-ID>\n" +
        "      <TITLE>Test data RIF72</TITLE>\n" +
        "    </REQ-IF-HEADER>\n" +
        "  </THE-HEADER>\n" +
        "  <CORE-CONTENT>\n" +
        "    <REQ-IF-CONTENT>\n" +
        "      <DATATYPES>\n" +
        "        <DATATYPE-DEFINITION-STRING DESC=\"This is a standard string type.\" IDENTIFIER=\"3631dcd2-59d1-11da-beb2-6fbc179f63e3\" LONG-NAME=\"Standard String Type\" MAX-LENGTH=\"65535\"/>\n" +
        "        <DATATYPE-DEFINITION-INTEGER DESC=\"This is a standard integer type.\" IDENTIFIER=\"3631dcd2-59d1-11da-beb2-6fbc179f63e4\" LONG-NAME=\"Standard Integer Type\"/>\n" +
        "      </DATATYPES>\n" +
        "      <SPEC-TYPES>\n" +
        "        <SPEC-OBJECT-TYPE DESC=\"This is an example SpecType with some common attributes.\" IDENTIFIER=\"3631dcd2-59d1-11da-beb2-6fbc179f63e2\" LAST-CHANGE=\"2005-05-30T11:42:19+02:00\" LONG-NAME=\"Example SpecType\">\n" +
        "          <SPEC-ATTRIBUTES>\n" +
        "            <ATTRIBUTE-DEFINITION-STRING DESC=\"This attribute contains the author of the requirement as a string.\" IDENTIFIER=\"356b02ec-59d1-11da-afa6-6b90abdfb5db\" LAST-CHANGE=\"2005-05-30T11:51:25+02:00\" LONG-NAME=\"Author\">\n" +
        "              <DEFAULT-VALUE>\n" +
        "                <ATTRIBUTE-VALUE-STRING THE-VALUE=\"TBD\"/>\n" +
        "              </DEFAULT-VALUE>\n" +
        "              <TYPE>\n" +
        "                <DATATYPE-DEFINITION-STRING-REF>3631dcd2-59d1-11da-beb2-6fbc179f63e3</DATATYPE-DEFINITION-STRING-REF>\n" +
        "              </TYPE>\n" +
        "            </ATTRIBUTE-DEFINITION-STRING>\n" +
        "            <ATTRIBUTE-DEFINITION-INTEGER DESC=\"This attribute contains the id of the requirement as a integer.\" IDENTIFIER=\"356b02ec-59d1-11da-afa6-6b90abdfb5dc\" LAST-CHANGE=\"2005-05-30T11:51:25+02:00\" LONG-NAME=\"Age\">\n" +
        "              <DEFAULT-VALUE>\n" +
        "                <ATTRIBUTE-VALUE-INTEGER THE-VALUE=\"0\"/>\n" +
        "              </DEFAULT-VALUE>\n" +
        "              <TYPE>\n" +
        "                <DATATYPE-DEFINITION-INTEGER-REF>3631dcd2-59d1-11da-beb2-6fbc179f63e4</DATATYPE-DEFINITION-INTEGER-REF>\n" +
        "              </TYPE>\n" +
        "            </ATTRIBUTE-DEFINITION-INTEGER>\n" +
        "          </SPEC-ATTRIBUTES>\n" +
        "        </SPEC-OBJECT-TYPE>\n" +
        "      </SPEC-TYPES>\n" +
        "      <SPEC-OBJECTS>\n" +
        "        <SPEC-OBJECT IDENTIFIER=\"2c84e85a-59d1-11da-8ef5-afdbd01c7a79\" LAST-CHANGE=\"2005-05-30T17:22:47+02:00\">\n" +
        "          <VALUES>\n" +
        "            <ATTRIBUTE-VALUE-STRING THE-VALUE=\"Max Mustermann\">\n" +
        "              <DEFINITION>\n" +
        "                <ATTRIBUTE-DEFINITION-STRING-REF>356b02ec-59d1-11da-afa6-6b90abdfb5db</ATTRIBUTE-DEFINITION-STRING-REF>\n" +
        "              </DEFINITION>\n" +
        "            </ATTRIBUTE-VALUE-STRING>\n" +
        "            <ATTRIBUTE-VALUE-INTEGER THE-VALUE=\"2\">\n" +
        "              <DEFINITION>\n" +
        "                <ATTRIBUTE-DEFINITION-INTEGER-REF>356b02ec-59d1-11da-afa6-6b90abdfb5dc</ATTRIBUTE-DEFINITION-INTEGER-REF>\n" +
        "              </DEFINITION>\n" +
        "            </ATTRIBUTE-VALUE-INTEGER>\n" +
        "          </VALUES>\n" +
        "          <TYPE>\n" +
        "            <SPEC-OBJECT-TYPE-REF>3631dcd2-59d1-11da-beb2-6fbc179f63e2</SPEC-OBJECT-TYPE-REF>\n" +
        "          </TYPE>\n" +
        "        </SPEC-OBJECT>\n" +
        "        <SPEC-OBJECT IDENTIFIER=\"2c84e85a-59d1-11da-8ef5-afdbd01c7a71\" LAST-CHANGE=\"2008-05-30T17:22:47+02:00\">\n" +
        "          <VALUES>\n" +
        "            <ATTRIBUTE-VALUE-STRING THE-VALUE=\"Hugo\">\n" +
        "              <DEFINITION>\n" +
        "                <ATTRIBUTE-DEFINITION-STRING-REF>356b02ec-59d1-11da-afa6-6b90abdfb5db</ATTRIBUTE-DEFINITION-STRING-REF>\n" +
        "              </DEFINITION>\n" +
        "            </ATTRIBUTE-VALUE-STRING>\n" +
        "            <ATTRIBUTE-VALUE-INTEGER THE-VALUE=\"10\">\n" +
        "              <DEFINITION>\n" +
        "                <ATTRIBUTE-DEFINITION-INTEGER-REF>356b02ec-59d1-11da-afa6-6b90abdfb5dc</ATTRIBUTE-DEFINITION-INTEGER-REF>\n" +
        "              </DEFINITION>\n" +
        "            </ATTRIBUTE-VALUE-INTEGER>\n" +
        "          </VALUES>\n" +
        "          <TYPE>\n" +
        "            <SPEC-OBJECT-TYPE-REF>3631dcd2-59d1-11da-beb2-6fbc179f63e2</SPEC-OBJECT-TYPE-REF>\n" +
        "          </TYPE>\n" +
        "        </SPEC-OBJECT>\n" +
        "      </SPEC-OBJECTS>\n" +
        "      <SPECIFICATIONS>\n" +
        "        <SPECIFICATION IDENTIFIER=\"spec-12345\">\n" +
        "          <CHILDREN>\n" +
        "            <SPEC-HIERARCHY IDENTIFIER=\"3dd45190-59d1-11da-a4bd-f3b1a51212c8\" LAST-CHANGE=\"2005-05-31T10:58:13+02:00\" LONG-NAME=\"Requirements document structure\">\n" +
        "              <CHILDREN>\n" +
        "                <SPEC-HIERARCHY IDENTIFIER=\"3dd6f17a-59d1-11da-9119-43bf5a5fdf50\">\n" +
        "                  <OBJECT>\n" +
        "                    <SPEC-OBJECT-REF>2c84e85a-59d1-11da-8ef5-afdbd01c7a71</SPEC-OBJECT-REF>\n" +
        "                  </OBJECT>\n" +
        "                </SPEC-HIERARCHY>\n" +
        "              </CHILDREN>\n" +
        "              <OBJECT>\n" +
        "                <SPEC-OBJECT-REF>2c84e85a-59d1-11da-8ef5-afdbd01c7a79</SPEC-OBJECT-REF>\n" +
        "              </OBJECT>\n" +
        "            </SPEC-HIERARCHY>\n" +
        "          </CHILDREN>\n" +
        "        </SPECIFICATION>\n" +
        "      </SPECIFICATIONS>\n" +
        "    </REQ-IF-CONTENT>\n" +
        "  </CORE-CONTENT>\n" +
        "</REQ-IF>";

    @Test
    public void test() throws JsonProcessingException {
        XmlMapper mapper = new XmlMapper();
        mapper.registerModule(new JaxbAnnotationModule());
        ReqIf reqIf = mapper.readValue(file, new TypeReference<>() {});
    }
}
