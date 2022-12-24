package features.artifacts;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactFieldType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactFieldExtraInfoType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.CustomAttribute;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.FloatFieldInfo;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.IntegerFieldInfo;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.SelectionFieldOption;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.services.ArtifactFieldValueService;
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

public class TestArtifactFieldStorage extends ApplicationBaseTest {

    @Autowired
    ArtifactFieldValueService artifactFieldValueService;

    private final Map<ArtifactFieldType, FieldSchemaInfo> fields = Map.of(
        ArtifactFieldType.TEXT, new FieldSchemaInfo("Text goes here", "textField", "Text Value", "Second text value"),
        ArtifactFieldType.PARAGRAPH, new FieldSchemaInfo("Longer text goes here", "paragraphField", "Paragraph Value", "Second paragraph value"),
        ArtifactFieldType.SELECT, new FieldSchemaInfo("A selection goes here", "selectField", "str1", "str2"),
        ArtifactFieldType.MULTISELECT, new FieldSchemaInfo("A multiselection goes here", "multiselectField", "[\"str2\",\"str3\"]", "[\"str1\",\"str2\"]"),
        ArtifactFieldType.RELATION, new FieldSchemaInfo("A relation goes here", "relationField", "[\"val1\",\"val2\"]", "[\"val2\",\"val3\"]"),
        ArtifactFieldType.DATE, new FieldSchemaInfo("A date goes here", "dateField", "Date value", "Second date value"),
        ArtifactFieldType.INT, new FieldSchemaInfo("An int goes here", "intField", "10", "11"),
        ArtifactFieldType.FLOAT, new FieldSchemaInfo("A float goes here", "floatField", "123.2", "321.1"),
        ArtifactFieldType.BOOLEAN, new FieldSchemaInfo("A bool goes here", "booleanField", "true", "false")
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

        for (ArtifactFieldType fieldType : fields.keySet()) {
            FieldSchemaInfo schemaInfo = fields.get(fieldType);

            CustomAttribute field = setupSchemaField(fieldType, schemaInfo);

            artifactFieldValueService.saveAttributeValue(field, artifactVersion, schemaInfo.value);
        }
    }

    private CustomAttribute setupSchemaField(ArtifactFieldType fieldType, FieldSchemaInfo schemaInfo) {
        CustomAttribute field = dbEntityBuilder.newCustomAttributeWithReturn(projectName, fieldType,
            schemaInfo.displayName, schemaInfo.keyName);

        if (fieldType.getExtraInfoType() == ArtifactFieldExtraInfoType.FLOAT_BOUNDS) {
            FloatFieldInfo floatFieldInfo = new FloatFieldInfo(field, floatMin, floatMax);
            serviceProvider.getFloatFieldInfoRepository().save(floatFieldInfo);
        } else if (fieldType.getExtraInfoType() == ArtifactFieldExtraInfoType.INT_BOUNDS) {
            IntegerFieldInfo intFieldInfo = new IntegerFieldInfo(field, intMin, intMax);
            serviceProvider.getIntegerFieldInfoRepository().save(intFieldInfo);
        } else if (fieldType.getExtraInfoType() == ArtifactFieldExtraInfoType.OPTIONS) {
            for (String selection : selections) {
                SelectionFieldOption option = new SelectionFieldOption(field, selection);
                serviceProvider.getSelectionFieldOptionRepository().save(option);
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

            if (field.getType().getExtraInfoType() == ArtifactFieldExtraInfoType.FLOAT_BOUNDS) {
                Optional<FloatFieldInfo> floatFieldInfo = serviceProvider.getFloatFieldInfoRepository().findBySchemaField(field);
                assertTrue(floatFieldInfo.isPresent());
                assertEquals(floatMax, floatFieldInfo.get().getMax());
                assertEquals(floatMin, floatFieldInfo.get().getMin());
            } else if (field.getType().getExtraInfoType() == ArtifactFieldExtraInfoType.INT_BOUNDS) {
                Optional<IntegerFieldInfo> integerFieldInfo = serviceProvider.getIntegerFieldInfoRepository().findBySchemaField(field);
                assertTrue(integerFieldInfo.isPresent());
                assertEquals(intMax, integerFieldInfo.get().getMax());
                assertEquals(intMin, integerFieldInfo.get().getMin());
            } else if (field.getType().getExtraInfoType() == ArtifactFieldExtraInfoType.OPTIONS) {
                List<SelectionFieldOption> options = serviceProvider.getSelectionFieldOptionRepository().findBySchemaField(field);
                List<String> values = options.stream().map(SelectionFieldOption::getValue).collect(Collectors.toList());
                assertEquals(selections, values);
            }
        }
    }

    @Test
    public void testFieldValueCreation() throws JsonProcessingException {
        List<ArtifactFieldVersion> fieldVersions = serviceProvider.getArtifactFieldVersionRepository().findByArtifactVersion(artifactVersion);
        assertEquals(fields.size(), fieldVersions.size());

        assertAttributeValues(fieldVersions, FieldSchemaInfo::getValue);
    }

    private void updateAttributes() {
        for (ArtifactFieldType fieldType : fields.keySet()) {
            FieldSchemaInfo schemaInfo = fields.get(fieldType);

            Optional<CustomAttribute> fieldOpt =
                artifactFieldValueService.getServiceProvider().getCustomAttributeRepository()
                    .findByProjectAndKeyname(project, schemaInfo.keyName);

            assertTrue(fieldOpt.isPresent());

            artifactFieldValueService.saveAttributeValue(fieldOpt.get(), artifactVersion, schemaInfo.altValue);
        }
    }

    private void assertAttributeValues(List<ArtifactFieldVersion> fieldVersions, Function<FieldSchemaInfo, String> expectedValueFunc) throws JsonProcessingException {
        for (ArtifactFieldVersion fieldVersion : fieldVersions) {
            FieldSchemaInfo schemaInfo = fields.get(fieldVersion.getSchemaField().getType());
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

        List<ArtifactFieldVersion> fieldVersions = serviceProvider.getArtifactFieldVersionRepository().findByArtifactVersion(artifactVersion);
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
