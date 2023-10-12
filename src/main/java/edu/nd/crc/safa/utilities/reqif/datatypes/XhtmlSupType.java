package edu.nd.crc.safa.utilities.reqif.datatypes;

import jakarta.xml.bind.annotation.XmlAccessType;
import jakarta.xml.bind.annotation.XmlAccessorType;
import jakarta.xml.bind.annotation.XmlRootElement;
import jakarta.xml.bind.annotation.XmlType;
import lombok.Getter;
import lombok.Setter;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "xhtml.sup.type", propOrder = {})
@XmlRootElement(name = "sup", namespace = "http://www.w3.org/1999/xhtml")
@Getter
@Setter
public class XhtmlSupType extends XhtmlInlPresType {
}
