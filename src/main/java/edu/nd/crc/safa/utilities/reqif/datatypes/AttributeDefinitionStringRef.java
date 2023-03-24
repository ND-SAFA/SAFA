package edu.nd.crc.safa.utilities.reqif.datatypes;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlIDREF;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlValue;

import lombok.Getter;
import lombok.Setter;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlRootElement(name = "ATTRIBUTE-DEFINITION-STRING-REF", namespace = "")
@Getter
@Setter
public class AttributeDefinitionStringRef extends AttributeDefinitionRef {
    @XmlValue
    @XmlIDREF
    @XmlSchemaType(name = "IDREF")
    protected AttributeDefinitionString attributeDefinition;
}
