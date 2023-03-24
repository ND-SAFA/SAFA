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
    "attributeValues"
})
@Getter
public class Values {
    @XmlElements({
        @XmlElement(name = "ATTRIBUTE-VALUE-BOOLEAN", namespace = "", type = AttributeValueBoolean.class),
        @XmlElement(name = "ATTRIBUTE-VALUE-DATE", namespace = "", type = AttributeValueDate.class),
        @XmlElement(name = "ATTRIBUTE-VALUE-ENUMERATION", namespace = "", type = AttributeValueEnumeration.class),
        @XmlElement(name = "ATTRIBUTE-VALUE-INTEGER", namespace = "", type = AttributeValueInteger.class),
        @XmlElement(name = "ATTRIBUTE-VALUE-REAL", namespace = "", type = AttributeValueReal.class),
        @XmlElement(name = "ATTRIBUTE-VALUE-STRING", namespace = "", type = AttributeValueString.class),
        @XmlElement(name = "ATTRIBUTE-VALUE-XHTML", namespace = "", type = AttributeValueXhtml.class)
    })
    protected List<AttributeValue> attributeValues = new ArrayList<>();
}
