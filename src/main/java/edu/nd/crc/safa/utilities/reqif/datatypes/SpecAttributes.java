package edu.nd.crc.safa.utilities.reqif.datatypes;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElements;
import javax.xml.bind.annotation.XmlType;

import lombok.Getter;

/**
 * Java class for anonymous complex type.
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "attributeDefinitions"
})
@Getter
public class SpecAttributes {
    @XmlElements({
        @XmlElement(name = "ATTRIBUTE-DEFINITION-BOOLEAN", namespace = "",
            type = AttributeDefinitionBoolean.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-DATE", namespace = "",
            type = AttributeDefinitionDate.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-ENUMERATION", namespace = "",
            type = AttributeDefinitionEnumeration.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-INTEGER", namespace = "",
            type = AttributeDefinitionInteger.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-REAL", namespace = "",
            type = AttributeDefinitionReal.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-STRING", namespace = "",
            type = AttributeDefinitionString.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-XHTML", namespace = "",
            type = AttributeDefinitionXhtml.class)
    })
    private List<AttributeDefinition> attributeDefinitions = new ArrayList<>();
}
