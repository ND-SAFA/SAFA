package features.artifacts;

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

public class TestArtifactFieldStorage extends ApplicationBaseTest {

    @Autowired
    AttributeValueService attributeValueService;

    @Autowired
    AttributeSystemServiceProvider serviceProvider;

    private final Map<CustomAttributeType, FieldSchemaInfo> fields = Map.of(
        CustomAttributeType.TEXT, new FieldSchemaInfo("Text goes here", "textField", "Text Value", "Second text value"),
        CustomAttributeType.PARAGRAPH, new FieldSchemaInfo("Longer text goes here", "paragraphField", "Paragraph Value", "Second paragraph value"),
        CustomAttributeType.SELECT, new FieldSchemaInfo("A selection goes here", "selectField", "str1", "str2"),
        CustomAttributeType.MULTISELECT, new FieldSchemaInfo("A multiselection goes here", "multiselectField", "[\"str2\",\"str3\"]", "[\"str1\",\"str2\"]"),
        CustomAttributeType.RELATION, new FieldSchemaInfo("A relation goes here", "relationField", "[\"val1\",\"val2\"]", "[\"val2\",\"val3\"]"),
        CustomAttributeType.DATE, new FieldSchemaInfo("A date goes here", "dateField", "Date value", "Second date value"),
        CustomAttributeType.INT, new FieldSchemaInfo("An int goes here", "intField", "10", "11"),
        CustomAttributeType.FLOAT, new FieldSchemaInfo("A float goes here", "floatField", "123.2", "321.1"),
        CustomAttributeType.BOOLEAN, new FieldSchemaInfo("A bool goes here", "booleanField", "true", "false")
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

        for (CustomAttributeType fieldType : fields.keySet()) {
            FieldSchemaInfo schemaInfo = fields.get(fieldType);

            CustomAttribute field = setupSchemaField(fieldType, schemaInfo);

            attributeValueService.saveAttributeValue(field, artifactVersion, schemaInfo.value);
        }
    }

    private CustomAttribute setupSchemaField(CustomAttributeType fieldType, FieldSchemaInfo schemaInfo) {
        CustomAttribute field = dbEntityBuilder.newCustomAttributeWithReturn(projectName, fieldType,
            schemaInfo.displayName, schemaInfo.keyName);

        if (fieldType.getExtraInfoType() == CustomAttributeExtraInfoType.FLOAT_BOUNDS) {
            FloatAttributeInfo floatAttributeInfo = new FloatAttributeInfo(field, floatMin, floatMax);
            serviceProvider.getFloatAttributeInfoRepository().save(floatAttributeInfo);
        } else if (fieldType.getExtraInfoType() == CustomAttributeExtraInfoType.INT_BOUNDS) {
            IntegerAttributeInfo intFieldInfo = new IntegerAttributeInfo(field, intMin, intMax);
            serviceProvider.getIntegerAttributeInfoRepository().save(intFieldInfo);
        } else if (fieldType.getExtraInfoType() == CustomAttributeExtraInfoType.OPTIONS) {
            for (String selection : selections) {
                SelectionAttributeOption option = new SelectionAttributeOption(field, selection);
                serviceProvider.getSelectionAttributeOptionRepository().save(option);
            }
        }

        return field;
    }

    @Test
    public void testSchemaCreation() {
        List<CustomAttribute> artifactFields = serviceProvider.getCustomAttributeRepository().findByProject(project);
        assertEquals(fields.size(), artifactFields.size());

        for (CustomAttribute field : artifactFields) {
            FieldSchemaInfo schemaInfo = fields.get(field.getType());
            assertEquals(schemaInfo.displayName, field.getLabel());
            assertEquals(schemaInfo.keyName, field.getKeyname());

            if (field.getType().getExtraInfoType() == CustomAttributeExtraInfoType.FLOAT_BOUNDS) {
                Optional<FloatAttributeInfo> floatFieldInfo = serviceProvider.getFloatAttributeInfoRepository().findByAttribute(field);
                assertTrue(floatFieldInfo.isPresent());
                assertEquals(floatMax, floatFieldInfo.get().getMax());
                assertEquals(floatMin, floatFieldInfo.get().getMin());
            } else if (field.getType().getExtraInfoType() == CustomAttributeExtraInfoType.INT_BOUNDS) {
                Optional<IntegerAttributeInfo> integerFieldInfo = serviceProvider.getIntegerAttributeInfoRepository().findByAttribute(field);
                assertTrue(integerFieldInfo.isPresent());
                assertEquals(intMax, integerFieldInfo.get().getMax());
                assertEquals(intMin, integerFieldInfo.get().getMin());
            } else if (field.getType().getExtraInfoType() == CustomAttributeExtraInfoType.OPTIONS) {
                List<SelectionAttributeOption> options = serviceProvider.getSelectionAttributeOptionRepository().findByAttribute(field);
                List<String> values = options.stream().map(SelectionAttributeOption::getValue).collect(Collectors.toList());
                assertEquals(selections, values);
            }
        }
    }

    @Test
    public void testFieldValueCreation() throws JsonProcessingException {
        List<ArtifactAttributeVersion> fieldVersions = serviceProvider.getArtifactAttributeVersionRepository().findByArtifactVersion(artifactVersion);
        assertEquals(fields.size(), fieldVersions.size());

        assertAttributeValues(fieldVersions, FieldSchemaInfo::getValue);
    }

    private void updateAttributes() {
        for (CustomAttributeType fieldType : fields.keySet()) {
            FieldSchemaInfo schemaInfo = fields.get(fieldType);

            Optional<CustomAttribute> fieldOpt = serviceProvider.getCustomAttributeRepository()
                    .findByProjectAndKeyname(project, schemaInfo.keyName);

            assertTrue(fieldOpt.isPresent());

            attributeValueService.saveAttributeValue(fieldOpt.get(), artifactVersion, schemaInfo.altValue);
        }
    }

    private void assertAttributeValues(List<ArtifactAttributeVersion> fieldVersions, Function<FieldSchemaInfo, String> expectedValueFunc) throws JsonProcessingException {
        for (ArtifactAttributeVersion fieldVersion : fieldVersions) {
            FieldSchemaInfo schemaInfo = fields.get(fieldVersion.getAttribute().getType());
            String expectedValue = expectedValueFunc.apply(schemaInfo);

            switch (fieldVersion.getValueType()) {
                case STRING:
                    String stringValue = fieldVersion.getStringValue();
                    assertEquals(expectedValue, stringValue);
                    break;
                case INTEGER:
                    int intValue = fieldVersion.getIntegerValue();
                    assertEquals(Integer.parseInt(expectedValue), intValue);
                    break;
                case BOOLEAN:
                    boolean boolValue = fieldVersion.getBooleanValue();
                    assertEquals(Boolean.parseBoolean(expectedValue), boolValue);
                    break;
                case FLOAT:
                    float floatValue = fieldVersion.getFloatValue();
                    assertEquals(Float.parseFloat(expectedValue), floatValue);
                    break;
                case STRING_ARRAY:
                    List<String> stringArrayValue = fieldVersion.getStringArrayValue();
                    assertEquals(Arrays.asList(new ObjectMapper().readValue(expectedValue, String[].class)), stringArrayValue);
                    break;
            }
        }
    }

    @Test
    public void testFieldValueUpdate() throws JsonProcessingException {
        updateAttributes();

        List<ArtifactAttributeVersion> fieldVersions = serviceProvider.getArtifactAttributeVersionRepository().findByArtifactVersion(artifactVersion);
        assertEquals(fields.size(), fieldVersions.size());

        assertAttributeValues(fieldVersions, FieldSchemaInfo::getAltValue);
    }

    @AllArgsConstructor
    @Data
    private static class FieldSchemaInfo {
        public String displayName;
        public String keyName;
        public String value;
        public String altValue;
    }
}
