package edu.nd.crc.safa.utilities.reqif.datatypes;

import javax.annotation.Generated;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlIDREF;
import javax.xml.bind.annotation.XmlType;

/**
 * <p>Java class for anonymous complex type.
 *
 * <p>The following schema fragment specifies the expected content contained within this class.
 *
 * <pre>
 * &lt;complexType&gt;
 *   &lt;complexContent&gt;
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType"&gt;
 *       &lt;choice&gt;
 *         &lt;element name="SPEC-OBJECT-REF" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}GLOBAL-REF"/&gt;
 *       &lt;/choice&gt;
 *     &lt;/restriction&gt;
 *   &lt;/complexContent&gt;
 * &lt;/complexType&gt;
 * </pre>
 *
 *
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "specobjectref"
})
@Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
public class SpecObjectRef {
    @XmlElement(name = "SPEC-OBJECT-REF", namespace = "")
    @XmlIDREF
    @Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
    protected SpecObject specobjectref;

    /**
     * Gets the value of the specobjectref property.
     *
     * @return
     *     possible object is
     *     {@link SpecObject }
     *
     */
    @Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
    public SpecObject getSpecObjectRef() {
        return specobjectref;
    }

    /**
     * Sets the value of the specobjectref property.
     *
     * @param value
     *     allowed object is
     *     {@link SpecObject }
     *
     */
    @Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
    public void setSpecObjectRef(SpecObject value) {
        this.specobjectref = value;
    }
}
