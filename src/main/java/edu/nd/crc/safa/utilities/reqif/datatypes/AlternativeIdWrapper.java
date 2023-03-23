package edu.nd.crc.safa.utilities.reqif.datatypes;

import javax.annotation.Generated;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "alternativeid"
})
@Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
public class AlternativeIdWrapper {

    @XmlElement(name = "ALTERNATIVE-ID", namespace = "")
    @Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
    protected AlternativeId alternativeid;

    /**
     * Gets the value of the alternativeid property.
     *
     * @return
     *     possible object is
     *     {@link AlternativeId }
     *
     */
    @Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
    public AlternativeId getAlternativeId() {
        return alternativeid;
    }

    /**
     * Sets the value of the alternativeid property.
     *
     * @param value
     *     allowed object is
     *     {@link AlternativeId }
     *
     */
    @Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
    public void setAlternativeId(AlternativeId value) {
        this.alternativeid = value;
    }
}
