package edu.nd.crc.safa.utilities.reqif.datatypes;

import jakarta.xml.bind.annotation.XmlAccessType;
import jakarta.xml.bind.annotation.XmlAccessorType;
import jakarta.xml.bind.annotation.XmlRootElement;
import jakarta.xml.bind.annotation.XmlType;

import lombok.Getter;
import lombok.Setter;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "xhtml.tt.type", propOrder = {})
@XmlRootElement(name = "tt", namespace = "http://www.w3.org/1999/xhtml")
@Getter
@Setter
public class XhtmlTtType extends XhtmlInlPresType {
}
