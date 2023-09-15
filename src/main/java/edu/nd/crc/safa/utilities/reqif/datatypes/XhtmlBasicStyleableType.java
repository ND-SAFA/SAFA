package edu.nd.crc.safa.utilities.reqif.datatypes;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;

import lombok.Getter;
import lombok.Setter;

@XmlAccessorType(XmlAccessType.FIELD)
@Getter
@Setter
public class XhtmlBasicStyleableType extends XhtmlBasicClassType {
    @XmlAttribute(name = "lang", namespace = "http://www.w3.org/XML/1998/namespace")
    private String lang;

    @XmlAttribute(name = "style")
    private String style;
}
