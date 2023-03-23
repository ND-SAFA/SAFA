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
 *         &lt;element name="ATTRIBUTE-DEFINITION-BOOLEAN" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-DEFINITION-BOOLEAN"/&gt;
 *         &lt;element name="ATTRIBUTE-DEFINITION-DATE" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-DEFINITION-DATE"/&gt;
 *         &lt;element name="ATTRIBUTE-DEFINITION-ENUMERATION" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-DEFINITION-ENUMERATION"/&gt;
 *         &lt;element name="ATTRIBUTE-DEFINITION-INTEGER" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-DEFINITION-INTEGER"/&gt;
 *         &lt;element name="ATTRIBUTE-DEFINITION-REAL" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-DEFINITION-REAL"/&gt;
 *         &lt;element name="ATTRIBUTE-DEFINITION-STRING" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-DEFINITION-STRING"/&gt;
 *         &lt;element name="ATTRIBUTE-DEFINITION-XHTML" type="{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}ATTRIBUTE-DEFINITION-XHTML"/&gt;
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
    "attributedefinitionbooleanOrATTRIBUTEDEFINITIONDATEOrATTRIBUTEDEFINITIONENUMERATION"
})
@Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
public class SpecAttributes {
    @XmlElements({
        @XmlElement(name = "ATTRIBUTE-DEFINITION-BOOLEAN", namespace = "", type = AttributeDefinitionBoolean.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-DATE", namespace = "", type = AttributeDefinitionDate.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-ENUMERATION", namespace = "", type = AttributeDefinitionEnumeration.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-INTEGER", namespace = "", type = AttributeDefinitionInteger.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-REAL", namespace = "", type = AttributeDefinitionReal.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-STRING", namespace = "", type = AttributeDefinitionString.class),
        @XmlElement(name = "ATTRIBUTE-DEFINITION-XHTML", namespace = "", type = AttributeDefinitionXhtml.class)
    })
    @Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
    protected List<Object> attributedefinitionbooleanOrATTRIBUTEDEFINITIONDATEOrATTRIBUTEDEFINITIONENUMERATION;

    /**
     * Gets the value of the attributedefinitionbooleanOrATTRIBUTEDEFINITIONDATEOrATTRIBUTEDEFINITIONENUMERATION property.
     *
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the attributedefinitionbooleanOrATTRIBUTEDEFINITIONDATEOrATTRIBUTEDEFINITIONENUMERATION property.
     *
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getATTRIBUTEDEFINITIONBOOLEANOrATTRIBUTEDEFINITIONDATEOrATTRIBUTEDEFINITIONENUMERATION().add(newItem);
     * </pre>
     *
     *
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link AttributeDefinitionBoolean }
     * {@link AttributeDefinitionDate }
     * {@link AttributeDefinitionEnumeration }
     * {@link AttributeDefinitionInteger }
     * {@link AttributeDefinitionReal }
     * {@link AttributeDefinitionString }
     * {@link AttributeDefinitionXhtml }
     *
     *
     */
    @Generated(value = "com.sun.tools.xjc.Driver", date = "2023-02-27T12:07:33-06:00", comments = "JAXB RI v2.3.0.1")
    public List<Object> getAttributes() {
        if (attributedefinitionbooleanOrATTRIBUTEDEFINITIONDATEOrATTRIBUTEDEFINITIONENUMERATION == null) {
            attributedefinitionbooleanOrATTRIBUTEDEFINITIONDATEOrATTRIBUTEDEFINITIONENUMERATION = new ArrayList<Object>();
        }
        return this.attributedefinitionbooleanOrATTRIBUTEDEFINITIONDATEOrATTRIBUTEDEFINITIONENUMERATION;
    }
}
