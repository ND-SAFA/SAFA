package edu.nd.crc.safa.test.utilities;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertSame;

import java.io.File;
import java.io.IOException;
import java.math.BigInteger;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.xml.datatype.DatatypeFactory;
import javax.xml.stream.XMLStreamException;

import edu.nd.crc.safa.utilities.reqif.datatypes.AttributeDefinition;
import edu.nd.crc.safa.utilities.reqif.datatypes.AttributeDefinitionInteger;
import edu.nd.crc.safa.utilities.reqif.datatypes.AttributeDefinitionIntegerRef;
import edu.nd.crc.safa.utilities.reqif.datatypes.AttributeDefinitionRef;
import edu.nd.crc.safa.utilities.reqif.datatypes.AttributeDefinitionString;
import edu.nd.crc.safa.utilities.reqif.datatypes.AttributeValue;
import edu.nd.crc.safa.utilities.reqif.datatypes.AttributeValueInteger;
import edu.nd.crc.safa.utilities.reqif.datatypes.AttributeValueString;
import edu.nd.crc.safa.utilities.reqif.datatypes.DatatypeDefinition;
import edu.nd.crc.safa.utilities.reqif.datatypes.DatatypeDefinitionInteger;
import edu.nd.crc.safa.utilities.reqif.datatypes.DatatypeDefinitionString;
import edu.nd.crc.safa.utilities.reqif.datatypes.ReqIf;
import edu.nd.crc.safa.utilities.reqif.datatypes.ReqIfContent;
import edu.nd.crc.safa.utilities.reqif.datatypes.ReqIfHeader;
import edu.nd.crc.safa.utilities.reqif.datatypes.SpecHierarchy;
import edu.nd.crc.safa.utilities.reqif.datatypes.SpecObject;
import edu.nd.crc.safa.utilities.reqif.datatypes.SpecObjectType;
import edu.nd.crc.safa.utilities.reqif.datatypes.SpecType;
import edu.nd.crc.safa.utilities.reqif.datatypes.Specification;
import edu.nd.crc.safa.utilities.reqif.parsing.ReqIfFileParser;

import jakarta.xml.bind.JAXBException;
import org.junit.jupiter.api.Test;
import org.springframework.core.io.ClassPathResource;

public class TestReqIfParsing {

    private static final String filename = "mock/reqif/test_reqif.xml";

    private final Map<String, Object> objects = new HashMap<>();
    private final DatatypeFactory factory = DatatypeFactory.newDefaultInstance();

    @Test
    public void test() throws IOException, JAXBException, XMLStreamException {
        File reqIfFile = new ClassPathResource(filename).getFile();
        ReqIf reqIf = ReqIfFileParser.parseReqIfFile(reqIfFile);

        assertHeader(reqIf);
        assertCoreContent(reqIf);
    }

    private void assertCoreContent(ReqIf reqIf) {
        assertNotNull(reqIf);
        assertNotNull(reqIf.getCoreContent());
        assertNotNull(reqIf.getCoreContent().getReqIfContent());

        ReqIfContent content = reqIf.getCoreContent().getReqIfContent();
        assertDatatypes(content);
        assertSpecTypes(content);
        assertSpecObjects(content);
        assertSpecifications(content);
    }

    private void assertSpecifications(ReqIfContent content) {
        assertNotNull(content.getSpecifications());
        assertNotNull(content.getSpecifications().getSpecifications());

        List<Specification> specifications = content.getSpecifications().getSpecifications();
        assertEquals(1, specifications.size());

        Specification specification = specifications.get(0);
        assertEquals("spec-12345", specification.getIdentifier());

        List<SpecHierarchy> specificationChildren = specification.getChildren().getSpecHierarchy();
        assertEquals(1, specificationChildren.size());

        SpecHierarchy childSpec = specificationChildren.get(0);
        assertEquals("3dd45190-59d1-11da-a4bd-f3b1a51212c8", childSpec.getIdentifier());
        assertEquals(factory.newXMLGregorianCalendar("2005-05-31T10:58:13+02:00"), childSpec.getLastChange());
        assertEquals("Requirements document structure", childSpec.getLongName());
        assertSame(objects.get("2c84e85a-59d1-11da-8ef5-afdbd01c7a79"), childSpec.getObject().getSpecObject());

        List<AttributeDefinitionRef> editableAttrs = childSpec.getEditableAttributes().getAttributeDefinitions();
        assertEquals(1, editableAttrs.size());
        assertInstanceOf(AttributeDefinitionIntegerRef.class, editableAttrs.get(0));

        AttributeDefinitionIntegerRef editableAttr = (AttributeDefinitionIntegerRef) editableAttrs.get(0);
        assertSame(objects.get("356b02ec-59d1-11da-afa6-6b90abdfb5dc"), editableAttr.getAttributeDefinition());

        List<SpecHierarchy> specificationGrandChildren = childSpec.getChildren().getSpecHierarchy();
        assertEquals(1, specificationGrandChildren.size());

        SpecHierarchy grandchild = specificationGrandChildren.get(0);
        assertEquals("3dd6f17a-59d1-11da-9119-43bf5a5fdf50", grandchild.getIdentifier());
        assertSame(objects.get("2c84e85a-59d1-11da-8ef5-afdbd01c7a71"), grandchild.getObject().getSpecObject());
    }

    private void assertSpecObjects(ReqIfContent content) {
        assertNotNull(content.getSpecObjects());
        assertNotNull(content.getSpecObjects().getSpecObjects());

        List<SpecObject> specObjects = content.getSpecObjects().getSpecObjects();
        assertEquals(2, specObjects.size());

        SpecObject specObject = specObjects.get(0);
        assertEquals("2c84e85a-59d1-11da-8ef5-afdbd01c7a79", specObject.getIdentifier());
        assertEquals(factory.newXMLGregorianCalendar("2005-05-30T17:22:47+02:00"), specObject.getLastChange());
        assertSame(objects.get("3631dcd2-59d1-11da-beb2-6fbc179f63e2"), specObject.getType().getSpecObjectType());
        assertSpecObjectValues(specObject, "Max Mustermann", 2);
        objects.put(specObject.getIdentifier(), specObject);

        specObject = specObjects.get(1);
        assertEquals("2c84e85a-59d1-11da-8ef5-afdbd01c7a71", specObject.getIdentifier());
        assertEquals(factory.newXMLGregorianCalendar("2008-05-30T17:22:47+02:00"), specObject.getLastChange());
        assertSame(objects.get("3631dcd2-59d1-11da-beb2-6fbc179f63e2"), specObject.getType().getSpecObjectType());
        assertSpecObjectValues(specObject, "Hugo", 10);
        objects.put(specObject.getIdentifier(), specObject);
    }

    private void assertSpecObjectValues(SpecObject specObject, String author, int idNum) {
        assertNotNull(specObject.getValues());
        assertNotNull(specObject.getValues().getAttributeValues());

        List<AttributeValue> values = specObject.getValues().getAttributeValues();
        assertEquals(2, values.size());

        assertInstanceOf(AttributeValueString.class, values.get(0));
        AttributeValueString stringAttr = (AttributeValueString) values.get(0);
        assertEquals(author, stringAttr.getValue());
        assertSame(objects.get("356b02ec-59d1-11da-afa6-6b90abdfb5db"),
            stringAttr.getDefinition().getAttributeDefinition());

        assertInstanceOf(AttributeValueInteger.class, values.get(1));
        AttributeValueInteger intAttr = (AttributeValueInteger) values.get(1);
        assertEquals(BigInteger.valueOf(idNum), intAttr.getValue());
        assertSame(objects.get("356b02ec-59d1-11da-afa6-6b90abdfb5dc"),
            intAttr.getDefinition().getAttributeDefinition());
    }

    private void assertSpecTypes(ReqIfContent content) {
        assertNotNull(content.getSpecTypes());
        assertNotNull(content.getSpecTypes().getSpecTypes());

        List<SpecType> specTypes = content.getSpecTypes().getSpecTypes();
        assertEquals(1, specTypes.size());

        assertInstanceOf(SpecObjectType.class, specTypes.get(0));
        SpecObjectType specType = (SpecObjectType) specTypes.get(0);
        assertEquals("This is an example SpecType with some common attributes.", specType.getDesc());
        assertEquals("3631dcd2-59d1-11da-beb2-6fbc179f63e2", specType.getIdentifier());
        assertEquals(factory.newXMLGregorianCalendar("2005-05-30T11:42:19+02:00"), specType.getLastChange());
        assertEquals("Example SpecType", specType.getLongName());
        objects.put(specType.getIdentifier(), specType);

        assertSpecTypeAttributes(specType);
    }

    private void assertSpecTypeAttributes(SpecObjectType specType) {
        assertNotNull(specType.getSpecAttributes());
        assertNotNull(specType.getSpecAttributes().getAttributeDefinitions());

        List<AttributeDefinition> specAttributes = specType.getSpecAttributes().getAttributeDefinitions();
        assertEquals(2, specAttributes.size());

        assertInstanceOf(AttributeDefinitionString.class, specAttributes.get(0));
        AttributeDefinitionString stringAttr = (AttributeDefinitionString) specAttributes.get(0);
        assertEquals("This attribute contains the author of the requirement as a string.", stringAttr.getDesc());
        assertEquals("356b02ec-59d1-11da-afa6-6b90abdfb5db", stringAttr.getIdentifier());
        assertEquals(factory.newXMLGregorianCalendar("2005-05-30T11:51:25+02:00"), stringAttr.getLastChange());
        assertEquals("Author", stringAttr.getLongName());
        assertEquals("TBD", stringAttr.getDefaultValue().getAttributeValue().getValue());
        assertSame(objects.get("3631dcd2-59d1-11da-beb2-6fbc179f63e3"), stringAttr.getType().getDatatypeDefinition());
        objects.put(stringAttr.getIdentifier(), stringAttr);

        assertInstanceOf(AttributeDefinitionInteger.class, specAttributes.get(1));
        AttributeDefinitionInteger intAttr = (AttributeDefinitionInteger) specAttributes.get(1);
        assertEquals("This attribute contains the id of the requirement as a integer.", intAttr.getDesc());
        assertEquals("356b02ec-59d1-11da-afa6-6b90abdfb5dc", intAttr.getIdentifier());
        assertEquals(factory.newXMLGregorianCalendar("2005-05-30T11:51:25+02:00"), intAttr.getLastChange());
        assertEquals("Age", intAttr.getLongName());
        assertEquals(BigInteger.valueOf(0), intAttr.getDefaultValue().getAttributeValue().getValue());
        assertSame(objects.get("3631dcd2-59d1-11da-beb2-6fbc179f63e4"), intAttr.getType().getDatatypeDefinition());
        objects.put(intAttr.getIdentifier(), intAttr);
    }

    private void assertDatatypes(ReqIfContent content) {
        assertNotNull(content.getDataTypes());
        assertNotNull(content.getDataTypes().getDatatypeDefinitions());

        List<DatatypeDefinition> datatypeDefinitions = content.getDataTypes().getDatatypeDefinitions();
        assertEquals(2, datatypeDefinitions.size());

        assertInstanceOf(DatatypeDefinitionString.class, datatypeDefinitions.get(0));
        DatatypeDefinitionString stringDef = (DatatypeDefinitionString) datatypeDefinitions.get(0);
        assertEquals("This is a standard string type.", stringDef.getDesc());
        assertEquals("3631dcd2-59d1-11da-beb2-6fbc179f63e3", stringDef.getIdentifier());
        assertEquals("Standard String Type", stringDef.getLongName());
        assertEquals(BigInteger.valueOf(65535), stringDef.getMaxLength());
        objects.put(stringDef.getIdentifier(), stringDef);

        assertInstanceOf(DatatypeDefinitionInteger.class, datatypeDefinitions.get(1));
        DatatypeDefinitionInteger intDef = (DatatypeDefinitionInteger) datatypeDefinitions.get(1);
        assertEquals("This is a standard integer type.", intDef.getDesc());
        assertEquals("3631dcd2-59d1-11da-beb2-6fbc179f63e4", intDef.getIdentifier());
        assertEquals("Standard Integer Type", intDef.getLongName());
        assertEquals("abc-123", intDef.getAlternativeId().getAlternativeId().getIdentifier());
        objects.put(intDef.getIdentifier(), intDef);
    }

    private void assertHeader(ReqIf reqIf) {
        assertNotNull(reqIf);
        assertNotNull(reqIf.getTheHeader());
        assertNotNull(reqIf.getTheHeader().getReqIfHeader());

        ReqIfHeader reqIfHeader = reqIf.getTheHeader().getReqIfHeader();
        assertEquals("3dd1a60c-59d1-11da-86ca-4bda04a730ce", reqIfHeader.getIdentifier());
        assertEquals("Embedded OLE object with multiple representation forms.", reqIfHeader.getComment());
        assertEquals(factory.newXMLGregorianCalendar("2005-05-23T12:00:00+02:00"), reqIfHeader.getCreationTime());
        assertEquals("Manually written", reqIfHeader.getSourceToolId());
        assertEquals("Test data RIF72", reqIfHeader.getTitle());
    }
}
