package edu.nd.crc.safa.utilities.reqif.datatypes;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

import lombok.Getter;
import lombok.Setter;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "xhtml.sup.type", propOrder = {})
@XmlRootElement(name = "sup", namespace = "http://www.w3.org/1999/xhtml")
@Getter
@Setter
public class XhtmlSupType extends XhtmlInlPresType {
}
