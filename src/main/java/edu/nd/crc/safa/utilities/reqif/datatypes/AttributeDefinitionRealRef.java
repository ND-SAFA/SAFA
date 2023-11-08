package edu.nd.crc.safa.utilities.reqif.datatypes;

import jakarta.xml.bind.annotation.XmlAccessType;
import jakarta.xml.bind.annotation.XmlAccessorType;
import jakarta.xml.bind.annotation.XmlIDREF;
import jakarta.xml.bind.annotation.XmlRootElement;
import jakarta.xml.bind.annotation.XmlSchemaType;
import jakarta.xml.bind.annotation.XmlValue;
import lombok.Getter;
import lombok.Setter;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlRootElement(name = "ATTRIBUTE-DEFINITION-REAL-REF", namespace = "")
@Getter
@Setter
public class AttributeDefinitionRealRef extends AttributeDefinitionRef {
    @XmlValue
    @XmlIDREF
    @XmlSchemaType(name = "IDREF")
    private AttributeDefinitionReal attributeDefinition;
}
