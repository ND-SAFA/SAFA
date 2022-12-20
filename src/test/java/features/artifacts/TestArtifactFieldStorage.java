package features.artifacts;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactFieldType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactFieldExtraInfoType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactSchemaField;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.FloatFieldInfo;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.IntegerFieldInfo;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.SelectionFieldOption;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldValueUtils;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactVersion;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.ArtifactType;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import common.ApplicationBaseTest;
import lombok.AllArgsConstructor;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestArtifactFieldStorage extends ApplicationBaseTest {

    private final String typeName = "ArtifactTypeName";

    private final Map<ArtifactFieldType, FieldSchemaInfo> fields = Map.of(
        ArtifactFieldType.TEXT, new FieldSchemaInfo("Text goes here", "textField", "Text Value"),
        ArtifactFieldType.PARAGRAPH, new FieldSchemaInfo("Longer text goes here", "paragraphField", "Paragraph Value"),
        ArtifactFieldType.SELECT, new FieldSchemaInfo("A selection goes here", "selectField", "str1"),
        ArtifactFieldType.MULTISELECT, new FieldSchemaInfo("A multiselection goes here", "multiselectField", "[\"str2\",\"str3\"]"),
        ArtifactFieldType.RELATION, new FieldSchemaInfo("A relation goes here", "relationField", "[\"val1\",\"val2\"]"),
        ArtifactFieldType.DATE, new FieldSchemaInfo("A date goes here", "dateField", "Date value"),
        ArtifactFieldType.INT, new FieldSchemaInfo("An int goes here", "intField", "10"),
        ArtifactFieldType.FLOAT, new FieldSchemaInfo("A float goes here", "floatField", "123.2"),
        ArtifactFieldType.BOOLEAN, new FieldSchemaInfo("A bool goes here", "booleanField", "true")
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
        dbEntityBuilder.createEmptyData();
        project = dbEntityBuilder.newProjectWithReturn(projectName);
        dbEntityBuilder.newVersionWithReturn(projectName);

        ArtifactType artifactType = dbEntityBuilder.newTypeAndReturn(projectName, typeName);
        String artifactName = "ArtifactName";
        dbEntityBuilder.newArtifactWithReturn(projectName, typeName, artifactName);
        String artifactSummary = "This is a summary";
        String artifactContent = "This is the full content of the artifact";
        artifactVersion = dbEntityBuilder.newArtifactBodyWithReturn(projectName, 0,
            ModificationType.ADDED, artifactName, artifactSummary, artifactContent);

        for (ArtifactFieldType fieldType : fields.keySet()) {
            FieldSchemaInfo schemaInfo = fields.get(fieldType);

            ArtifactSchemaField field = new ArtifactSchemaField();
            setupSchemaField(field, artifactType, fieldType, schemaInfo);

            ArtifactFieldValueUtils.saveArtifactValue(serviceProvider, field, artifactVersion, schemaInfo.value);
        }
    }

    private void setupSchemaField(ArtifactSchemaField field, ArtifactType artifactType, ArtifactFieldType fieldType, FieldSchemaInfo schemaInfo) {
        field.setArtifactType(artifactType);
        field.setType(fieldType);
        field.setLabel(schemaInfo.displayName);
        field.setKeyname(schemaInfo.keyName);
        serviceProvider.getArtifactSchemaFieldRepository().save(field);

        if (fieldType.getExtraInfoType() == ArtifactFieldExtraInfoType.FLOAT_BOUNDS) {
            FloatFieldInfo floatFieldInfo = new FloatFieldInfo();
            floatFieldInfo.setSchemaField(field);
            floatFieldInfo.setMax(floatMax);
            floatFieldInfo.setMin(floatMin);
            serviceProvider.getFloatFieldInfoRepository().save(floatFieldInfo);
        } else if (fieldType.getExtraInfoType() == ArtifactFieldExtraInfoType.INT_BOUNDS) {
            IntegerFieldInfo intFieldInfo = new IntegerFieldInfo();
            intFieldInfo.setSchemaField(field);
            intFieldInfo.setMax(intMax);
            intFieldInfo.setMin(intMin);
            serviceProvider.getIntegerFieldInfoRepository().save(intFieldInfo);
        } else if (fieldType.getExtraInfoType() == ArtifactFieldExtraInfoType.OPTIONS) {
            for (String selection : selections) {
                SelectionFieldOption option = new SelectionFieldOption();
                option.setSchemaField(field);
                option.setValue(selection);
                serviceProvider.getSelectionFieldOptionRepository().save(option);
            }
        }
    }

    @Test
    public void testSchemaCreation() {
        Optional<ArtifactType> artifactTypeOptional = artifactTypeRepository.findByProjectAndNameIgnoreCase(project, typeName);
        assertTrue(artifactTypeOptional.isPresent());

        ArtifactType artifactType = artifactTypeOptional.get();
        List<ArtifactSchemaField> artifactFields = serviceProvider.getArtifactSchemaFieldRepository().findByArtifactType(artifactType);
        assertEquals(fields.size(), artifactFields.size());

        for (ArtifactSchemaField field : artifactFields) {
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

        for (ArtifactFieldVersion fieldVersion : fieldVersions) {
            FieldSchemaInfo schemaInfo = fields.get(fieldVersion.getSchemaField().getType());

            switch (fieldVersion.getValueType()) {
                case STRING:
                    String stringValue = fieldVersion.getStringValue();
                    assertEquals(schemaInfo.value, stringValue);
                    break;
                case INTEGER:
                    int intValue = fieldVersion.getIntegerValue();
                    assertEquals(Integer.parseInt(schemaInfo.value), intValue);
                    break;
                case BOOLEAN:
                    boolean boolValue = fieldVersion.getBooleanValue();
                    assertEquals(Boolean.parseBoolean(schemaInfo.value), boolValue);
                    break;
                case FLOAT:
                    float floatValue = fieldVersion.getFloatValue();
                    assertEquals(Float.parseFloat(schemaInfo.value), floatValue);
                    break;
                case STRING_ARRAY:
                    List<String> stringArrayValue = fieldVersion.getStringArrayValue();
                    assertEquals(Arrays.asList(new ObjectMapper().readValue(schemaInfo.value, String[].class)), stringArrayValue);
                    break;
            }
        }
    }

    @AllArgsConstructor
    private static class FieldSchemaInfo {
        public String displayName;
        public String keyName;
        public String value;
    }
}
