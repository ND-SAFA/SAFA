package edu.nd.crc.safa.utilities.reqif.datatypes;

import java.util.ArrayList;
import java.util.List;
import javax.annotation.Generated;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElements;
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
 *       &lt;choice maxOccurs="unbounded" minOccurs="0"&gt;
 *         &lt;element name="ATTRIBUTE-VALUE-BOOLEAN" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-VALUE-BOOLEAN"/&gt;
 *         &lt;element name="ATTRIBUTE-VALUE-DATE" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-VALUE-DATE"/&gt;
 *         &lt;element name="ATTRIBUTE-VALUE-ENUMERATION" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-VALUE-ENUMERATION"/&gt;
 *         &lt;element name="ATTRIBUTE-VALUE-INTEGER" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-VALUE-INTEGER"/&gt;
 *         &lt;element name="ATTRIBUTE-VALUE-REAL" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-VALUE-REAL"/&gt;
 *         &lt;element name="ATTRIBUTE-VALUE-STRING" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-VALUE-STRING"/&gt;
 *         &lt;element name="ATTRIBUTE-VALUE-XHTML" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-VALUE-XHTML"/&gt;
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
    "attributevaluebooleanOrATTRIBUTEVALUEDATEOrATTRIBUTEVALUEENUMERATION"
})
@Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
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
    @Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
    protected List<Object> attributevaluebooleanOrATTRIBUTEVALUEDATEOrATTRIBUTEVALUEENUMERATION;

    /**
     * Gets the value of the attributevaluebooleanOrATTRIBUTEVALUEDATEOrATTRIBUTEVALUEENUMERATION property.
     *
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the attributevaluebooleanOrATTRIBUTEVALUEDATEOrATTRIBUTEVALUEENUMERATION property.
     *
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getATTRIBUTEVALUEBOOLEANOrATTRIBUTEVALUEDATEOrATTRIBUTEVALUEENUMERATION().add(newItem);
     * </pre>
     *
     *
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link AttributeValueBoolean }
     * {@link AttributeValueDate }
     * {@link AttributeValueEnumeration }
     * {@link AttributeValueInteger }
     * {@link AttributeValueReal }
     * {@link AttributeValueString }
     * {@link AttributeValueXhtml }
     *
     *
     */
    @Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
    public List<Object> getValues() {
        if (attributevaluebooleanOrATTRIBUTEVALUEDATEOrATTRIBUTEVALUEENUMERATION == null) {
            attributevaluebooleanOrATTRIBUTEVALUEDATEOrATTRIBUTEVALUEENUMERATION = new ArrayList<Object>();
        }
        return this.attributevaluebooleanOrATTRIBUTEVALUEDATEOrATTRIBUTEVALUEENUMERATION;
    }
}
