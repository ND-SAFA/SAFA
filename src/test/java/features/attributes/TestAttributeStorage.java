package features.attributes;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeExtraInfoType;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.FloatAttributeInfo;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.IntegerAttributeInfo;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.SelectionAttributeOption;
import edu.nd.crc.safa.features.attributes.entities.db.values.ArtifactAttributeVersion;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;
import edu.nd.crc.safa.features.attributes.services.AttributeValueService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import common.ApplicationBaseTest;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class TestAttributeStorage extends ApplicationBaseTest {

    @Autowired
    AttributeValueService attributeValueService;

    @Autowired
    AttributeSystemServiceProvider serviceProvider;

    private final Map<CustomAttributeType, AttributeInfo> attributes = Map.of(
        CustomAttributeType.TEXT, new AttributeInfo("Text goes here", "textField", "Text Value", "Second text value"),
        CustomAttributeType.PARAGRAPH, new AttributeInfo("Longer text goes here", "paragraphField", "Paragraph Value", "Second paragraph value"),
        CustomAttributeType.SELECT, new AttributeInfo("A selection goes here", "selectField", "str1", "str2"),
        CustomAttributeType.MULTISELECT, new AttributeInfo("A multiselection goes here", "multiselectField", "[\"str2\",\"str3\"]", "[\"str1\",\"str2\"]"),
        CustomAttributeType.RELATION, new AttributeInfo("A relation goes here", "relationField", "[\"val1\",\"val2\"]", "[\"val2\",\"val3\"]"),
        CustomAttributeType.DATE, new AttributeInfo("A date goes here", "dateField", "Date value", "Second date value"),
        CustomAttributeType.INT, new AttributeInfo("An int goes here", "intField", "10", "11"),
        CustomAttributeType.FLOAT, new AttributeInfo("A float goes here", "floatField", "123.2", "321.1"),
        CustomAttributeType.BOOLEAN, new AttributeInfo("A bool goes here", "booleanField", "true", "false")
    );

    private final float floatMax = 100.5f;
    private final float floatMin = -24.7f;
    private final int intMax = 99;
    private final int intMin = 1;
    private final List<String> selections = List.of("str1", "str2", "str3");

    private Project project;
    private ArtifactVersion artifactVersion;

    @BeforeEach
    public void setup() throws IOException {
        String typeName = "ArtifactTypeName";
        String artifactName = "ArtifactName";
        String artifactSummary = "This is a summary";
        String artifactContent = "This is the full content of the artifact";

        dbEntityBuilder.createEmptyData();
        project = dbEntityBuilder.newProjectWithReturn(projectName);

        dbEntityBuilder.newVersion(projectName)
            .newType(projectName, typeName)
            .newArtifact(projectName, typeName, artifactName);

        artifactVersion = dbEntityBuilder.newArtifactBodyWithReturn(projectName, 0,
            ModificationType.ADDED, artifactName, artifactSummary, artifactContent);

        for (CustomAttributeType attributeType : attributes.keySet()) {
            AttributeInfo schemaInfo = attributes.get(attributeType);

            CustomAttribute attribute = setupAttribute(attributeType, schemaInfo);

            attributeValueService.saveAttributeValue(attribute, artifactVersion, schemaInfo.value);
        }
    }

    private CustomAttribute setupAttribute(CustomAttributeType attributeType, AttributeInfo schemaInfo) {
        CustomAttribute attribute = dbEntityBuilder.newCustomAttributeWithReturn(projectName, attributeType,
            schemaInfo.displayName, schemaInfo.keyName);

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

        return attribute;
    }

    @Test
    public void testSchemaCreation() {
        List<CustomAttribute> artifactAttributes = serviceProvider.getCustomAttributeRepository().findByProject(project);
        assertEquals(attributes.size(), artifactAttributes.size());

        for (CustomAttribute attribute : artifactAttributes) {
            AttributeInfo schemaInfo = attributes.get(attribute.getType());
            assertEquals(schemaInfo.displayName, attribute.getLabel());
            assertEquals(schemaInfo.keyName, attribute.getKeyname());

            if (attribute.getType().getExtraInfoType() == CustomAttributeExtraInfoType.FLOAT_BOUNDS) {
                Optional<FloatAttributeInfo> floatAttributeInfo = serviceProvider.getFloatAttributeInfoRepository().findByAttribute(attribute);
                assertTrue(floatAttributeInfo.isPresent());
                assertEquals(floatMax, floatAttributeInfo.get().getMax());
                assertEquals(floatMin, floatAttributeInfo.get().getMin());
            } else if (attribute.getType().getExtraInfoType() == CustomAttributeExtraInfoType.INT_BOUNDS) {
                Optional<IntegerAttributeInfo> integerAttributeInfo = serviceProvider.getIntegerAttributeInfoRepository().findByAttribute(attribute);
                assertTrue(integerAttributeInfo.isPresent());
                assertEquals(intMax, integerAttributeInfo.get().getMax());
                assertEquals(intMin, integerAttributeInfo.get().getMin());
            } else if (attribute.getType().getExtraInfoType() == CustomAttributeExtraInfoType.OPTIONS) {
                List<SelectionAttributeOption> options = serviceProvider.getSelectionAttributeOptionRepository().findByAttribute(attribute);
                List<String> values = options.stream().map(SelectionAttributeOption::getValue).collect(Collectors.toList());
                assertEquals(selections, values);
            }
        }
    }

    @Test
    public void testAttributeValueCreation() throws JsonProcessingException {
        List<ArtifactAttributeVersion> attributeVersions = serviceProvider.getArtifactAttributeVersionRepository().findByArtifactVersion(artifactVersion);
        assertEquals(attributes.size(), attributeVersions.size());

        assertAttributeValues(attributeVersions, AttributeInfo::getValue);
    }

    private void updateAttributes() {
        for (CustomAttributeType attributeType : attributes.keySet()) {
            AttributeInfo schemaInfo = attributes.get(attributeType);

            Optional<CustomAttribute> attributeOpt = serviceProvider.getCustomAttributeRepository()
                    .findByProjectAndKeyname(project, schemaInfo.keyName);

            assertTrue(attributeOpt.isPresent());

            attributeValueService.saveAttributeValue(attributeOpt.get(), artifactVersion, schemaInfo.altValue);
        }
    }

    private void assertAttributeValues(List<ArtifactAttributeVersion> attributeVersions, Function<AttributeInfo, String> expectedValueFunc) throws JsonProcessingException {
        for (ArtifactAttributeVersion attributeVersion : attributeVersions) {
            AttributeInfo schemaInfo = attributes.get(attributeVersion.getAttribute().getType());
            String expectedValue = expectedValueFunc.apply(schemaInfo);

            switch (attributeVersion.getValueType()) {
                case STRING:
                    String stringValue = attributeVersion.getStringValue();
                    assertEquals(expectedValue, stringValue);
                    break;
                case INTEGER:
                    int intValue = attributeVersion.getIntegerValue();
                    assertEquals(Integer.parseInt(expectedValue), intValue);
                    break;
                case BOOLEAN:
                    boolean boolValue = attributeVersion.getBooleanValue();
                    assertEquals(Boolean.parseBoolean(expectedValue), boolValue);
                    break;
                case FLOAT:
                    float floatValue = attributeVersion.getFloatValue();
                    assertEquals(Float.parseFloat(expectedValue), floatValue);
                    break;
                case STRING_ARRAY:
                    List<String> stringArrayValue = attributeVersion.getStringArrayValue();
                    assertEquals(Arrays.asList(new ObjectMapper().readValue(expectedValue, String[].class)), stringArrayValue);
                    break;
            }
        }
    }

    @Test
    public void testAttributeValueUpdate() throws JsonProcessingException {
        updateAttributes();

        List<ArtifactAttributeVersion> attributeVersions = serviceProvider.getArtifactAttributeVersionRepository().findByArtifactVersion(artifactVersion);
        assertEquals(attributes.size(), attributeVersions.size());

        assertAttributeValues(attributeVersions, AttributeInfo::getAltValue);
    }

    @AllArgsConstructor
    @Data
    private static class AttributeInfo {
        public String displayName;
        public String keyName;
        public String value;
        public String altValue;
    }
}
