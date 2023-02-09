package edu.nd.crc.safa.test.features.attributes;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeExtraInfoType;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.FloatAttributeInfo;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.IntegerAttributeInfo;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.SelectionAttributeOption;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;
import edu.nd.crc.safa.test.builders.DbEntityBuilder;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.BooleanNode;
import com.fasterxml.jackson.databind.node.FloatNode;
import com.fasterxml.jackson.databind.node.IntNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.TextNode;
import lombok.AllArgsConstructor;
import lombok.Data;

public class AttributesForTesting {
    public final Map<CustomAttributeType, AttributeInfo> attributes = Map.of(
            CustomAttributeType.TEXT, new AttributeInfo("Text goes here", "textField",
                    TextNode.valueOf("Text Value"), TextNode.valueOf("Second text value")),

            CustomAttributeType.PARAGRAPH, new AttributeInfo("Longer text goes here", "paragraphField",
                    TextNode.valueOf("Paragraph Value"), TextNode.valueOf("Second paragraph value")),

            CustomAttributeType.SELECT, new AttributeInfo("A selection goes here", "selectField",
                    TextNode.valueOf("str1"), TextNode.valueOf("str2")),

            CustomAttributeType.MULTISELECT, new AttributeInfo("A multiselection goes here", "multiselectField",
                    new ArrayNode(JsonNodeFactory.instance, List.of(
                        TextNode.valueOf("str2"), TextNode.valueOf("str3"))),
                    new ArrayNode(JsonNodeFactory.instance, List.of(
                        TextNode.valueOf("str1"), TextNode.valueOf("str2")))),

            CustomAttributeType.RELATION, new AttributeInfo("A relation goes here", "relationField",
                    new ArrayNode(JsonNodeFactory.instance, List.of(
                        TextNode.valueOf("val1"), TextNode.valueOf("val2"))),
                    new ArrayNode(JsonNodeFactory.instance, List.of(
                        TextNode.valueOf("val2"), TextNode.valueOf("val3")))),

            CustomAttributeType.DATE, new AttributeInfo("A date goes here", "dateField",
                    TextNode.valueOf("Date value"), TextNode.valueOf("Second date value")),

            CustomAttributeType.INT, new AttributeInfo("An int goes here", "intField",
                    IntNode.valueOf(10), IntNode.valueOf(11)),

            CustomAttributeType.FLOAT, new AttributeInfo("A float goes here", "floatField",
                    FloatNode.valueOf(123.2f), FloatNode.valueOf(321.1f)),

            CustomAttributeType.BOOLEAN, new AttributeInfo("A bool goes here", "booleanField",
                    BooleanNode.TRUE, BooleanNode.FALSE)
    );

    public static final float floatMax = 100.5f;
    public static final float floatMin = -24.7f;
    public static final int intMax = 99;
    public static final int intMin = 1;
    public static final List<String> selections = List.of("str1", "str2", "str3");

    public static final float altFloatMax = 4.20f;
    public static final float altFloatMin = 13.37f;
    public static final int altIntMax = 7;
    public static final int altIntMin = 6;
    public static final List<String> altSelections = List.of("str4", "str5", "str6");

    public CustomAttribute setupAttribute(DbEntityBuilder dbEntityBuilder, String projectName,
                                          AttributeSystemServiceProvider serviceProvider,
                                          CustomAttributeType attributeType) {

        AttributeInfo schemaInfo = attributes.get(attributeType);

        CustomAttribute attribute = dbEntityBuilder.newCustomAttributeWithReturn(projectName, attributeType,
                schemaInfo.displayName, schemaInfo.keyName);

        addExtraInfo(attribute, serviceProvider);

        return attribute;
    }

    public static void addExtraInfo(CustomAttribute attribute, AttributeSystemServiceProvider serviceProvider) {
        CustomAttributeType attributeType = attribute.getType();

        if (attributeType.getExtraInfoType() == CustomAttributeExtraInfoType.FLOAT_BOUNDS) {
            FloatAttributeInfo floatAttributeInfo = new FloatAttributeInfo(attribute, floatMin, floatMax);
            serviceProvider.getFloatAttributeInfoRepository().save(floatAttributeInfo);
        } else if (attributeType.getExtraInfoType() == CustomAttributeExtraInfoType.INT_BOUNDS) {
            IntegerAttributeInfo intAttributeInfo = new IntegerAttributeInfo(attribute, intMin, intMax);
            serviceProvider.getIntegerAttributeInfoRepository().save(intAttributeInfo);
        } else if (attributeType.getExtraInfoType() == CustomAttributeExtraInfoType.OPTIONS) {
            for (String selection : selections) {
                SelectionAttributeOption option = new SelectionAttributeOption(attribute, selection);
                serviceProvider.getSelectionAttributeOptionRepository().save(option);
            }
        }
    }

    public CustomAttributeAppEntity setupAttributeAppEntity(CustomAttributeType type) {
        AttributeInfo schemaInfo = attributes.get(type);

        CustomAttributeAppEntity appEntity = new CustomAttributeAppEntity(schemaInfo.keyName,
            schemaInfo.displayName, type);

        if (type.getExtraInfoType() == CustomAttributeExtraInfoType.FLOAT_BOUNDS) {
            appEntity.setMin(floatMin);
            appEntity.setMax(floatMax);
        } else if (type.getExtraInfoType() == CustomAttributeExtraInfoType.INT_BOUNDS) {
            appEntity.setMin(intMin);
            appEntity.setMax(intMax);
        } else if (type.getExtraInfoType() == CustomAttributeExtraInfoType.OPTIONS) {
            appEntity.setOptions(selections);
        }

        return appEntity;
    }

    public CustomAttributeAppEntity setupAltAttributeAppEntity(CustomAttributeType type) {
        AttributeInfo schemaInfo = attributes.get(type);

        CustomAttributeAppEntity appEntity = new CustomAttributeAppEntity(schemaInfo.keyName,
            schemaInfo.displayName + "-alt", type);

        if (type.getExtraInfoType() == CustomAttributeExtraInfoType.FLOAT_BOUNDS) {
            appEntity.setMin(altFloatMin);
            appEntity.setMax(altFloatMax);
        } else if (type.getExtraInfoType() == CustomAttributeExtraInfoType.INT_BOUNDS) {
            appEntity.setMin(altIntMin);
            appEntity.setMax(altIntMax);
        } else if (type.getExtraInfoType() == CustomAttributeExtraInfoType.OPTIONS) {
            appEntity.setOptions(altSelections);
        }

        return appEntity;
    }

    @AllArgsConstructor
    @Data
    public static class AttributeInfo {
        public String displayName;
        public String keyName;
        public JsonNode value;
        public JsonNode altValue;
    }
}
