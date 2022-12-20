package features.artifacts;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactFieldType;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactFieldExtraInfoType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactSchemaField;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.FloatFieldInfo;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.IntegerFieldInfo;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.SelectionFieldOption;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.BooleanFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.FloatFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.IntegerFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.StringArrayFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.StringFieldValue;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.artifacts.repositories.schema.ArtifactSchemaFieldRepository;
import edu.nd.crc.safa.features.artifacts.repositories.schema.FloatFieldInfoRepository;
import edu.nd.crc.safa.features.artifacts.repositories.schema.IntegerFieldInfoRepository;
import edu.nd.crc.safa.features.artifacts.repositories.schema.SelectionFieldOptionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.ArtifactFieldVersionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.BooleanFieldValueRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.FloatFieldValueRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.IntegerFieldValueRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.StringArrayFieldValueRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.StringFieldValueRepository;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import common.ApplicationBaseTest;
import lombok.AllArgsConstructor;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestArtifactFieldStorage extends ApplicationBaseTest {

    private final String typeName = "ArtifactTypeName";
    private final String artifactName = "ArtifactName";
    private final String artifactSummary = "This is a summary";
    private final String artifactContent = "This is the full content of the artifact";

    private final Map<ArtifactFieldType, FieldSchemaInfo> fields = Map.of(
        ArtifactFieldType.TEXT, new FieldSchemaInfo("Text goes here", "textField", "Text Value"),
        ArtifactFieldType.PARAGRAPH, new FieldSchemaInfo("Longer text goes here", "paragraphField", "Paragraph Value"),
        ArtifactFieldType.SELECT, new FieldSchemaInfo("A selection goes here", "selectField", "str1"),
        ArtifactFieldType.MULTISELECT, new FieldSchemaInfo("A multiselection goes here", "multiselectField", List.of("str2", "str3")),
        ArtifactFieldType.RELATION, new FieldSchemaInfo("A relation goes here", "relationField", List.of("val1", "val2")),
        ArtifactFieldType.DATE, new FieldSchemaInfo("A date goes here", "dateField", "Date value"),
        ArtifactFieldType.INT, new FieldSchemaInfo("An int goes here", "intField", 10),
        ArtifactFieldType.FLOAT, new FieldSchemaInfo("A float goes here", "floatField", 123.2f),
        ArtifactFieldType.BOOLEAN, new FieldSchemaInfo("A bool goes here", "booleanField", true)
    );

    private final float floatMax = 100.5f;
    private final float floatMin = -24.7f;
    private final int intMax = 99;
    private final int intMin = 1;
    private final List<String> selections = List.of("str1", "str2", "str3");

    @Autowired ArtifactSchemaFieldRepository artifactSchemaFieldRepository;
    @Autowired ArtifactTypeRepository artifactTypeRepository;
    @Autowired SelectionFieldOptionRepository selectionFieldOptionRepository;
    @Autowired IntegerFieldInfoRepository integerFieldInfoRepository;
    @Autowired FloatFieldInfoRepository floatFieldInfoRepository;

    @Autowired FloatFieldValueRepository floatFieldValueRepository;
    @Autowired IntegerFieldValueRepository integerFieldValueRepository;
    @Autowired BooleanFieldValueRepository booleanFieldValueRepository;
    @Autowired StringFieldValueRepository stringFieldValueRepository;
    @Autowired StringArrayFieldValueRepository stringArrayFieldValueRepository;
    @Autowired ArtifactFieldVersionRepository artifactFieldVersionRepository;

    private Project project;
    private ArtifactVersion artifactVersion;

    @BeforeEach
    public void setup() throws IOException {
        dbEntityBuilder.createEmptyData();
        project = dbEntityBuilder.newProjectWithReturn(projectName);
        ProjectVersion projectVersion = dbEntityBuilder.newVersionWithReturn(projectName);

        ArtifactType artifactType = dbEntityBuilder.newTypeAndReturn(projectName, typeName);
        Artifact artifact = dbEntityBuilder.newArtifactWithReturn(projectName, typeName, artifactName);
        artifactVersion = dbEntityBuilder.newArtifactBodyWithReturn(projectName, 0,
            ModificationType.ADDED, artifactName, artifactSummary, artifactContent);

        for (ArtifactFieldType fieldType : fields.keySet()) {
            FieldSchemaInfo schemaInfo = fields.get(fieldType);

            ArtifactSchemaField field = new ArtifactSchemaField();
            setupSchemaField(field, artifactType, fieldType, schemaInfo);

            ArtifactFieldVersion fieldVersion = new ArtifactFieldVersion();
            setupFieldVersion(fieldVersion, field, artifactVersion, fieldType, schemaInfo);
        }
    }

    private void setupSchemaField(ArtifactSchemaField field, ArtifactType artifactType, ArtifactFieldType fieldType, FieldSchemaInfo schemaInfo) {
        field.setArtifactType(artifactType);
        field.setType(fieldType);
        field.setLabel(schemaInfo.displayName);
        field.setKeyname(schemaInfo.keyName);
        artifactSchemaFieldRepository.save(field);

        if (fieldType.getExtraInfoType() == ArtifactFieldExtraInfoType.FLOAT_BOUNDS) {
            FloatFieldInfo floatFieldInfo = new FloatFieldInfo();
            floatFieldInfo.setSchemaField(field);
            floatFieldInfo.setMax(floatMax);
            floatFieldInfo.setMin(floatMin);
            floatFieldInfoRepository.save(floatFieldInfo);
        } else if (fieldType.getExtraInfoType() == ArtifactFieldExtraInfoType.INT_BOUNDS) {
            IntegerFieldInfo intFieldInfo = new IntegerFieldInfo();
            intFieldInfo.setSchemaField(field);
            intFieldInfo.setMax(intMax);
            intFieldInfo.setMin(intMin);
            integerFieldInfoRepository.save(intFieldInfo);
        } else if (fieldType.getExtraInfoType() == ArtifactFieldExtraInfoType.OPTIONS) {
            for (String selection : selections) {
                SelectionFieldOption option = new SelectionFieldOption();
                option.setSchemaField(field);
                option.setValue(selection);
                selectionFieldOptionRepository.save(option);
            }
        }
    }

    private void setupFieldVersion(ArtifactFieldVersion fieldVersion, ArtifactSchemaField field, ArtifactVersion artifactVersion, ArtifactFieldType fieldType, FieldSchemaInfo schemaInfo) {
        fieldVersion.setSchemaField(field);
        fieldVersion.setArtifactVersion(artifactVersion);
        artifactFieldVersionRepository.save(fieldVersion);

        switch (fieldType.getStorageType()) {
            case FLOAT:
                FloatFieldValue floatFieldValue = new FloatFieldValue();
                floatFieldValue.setFieldVersion(fieldVersion);
                floatFieldValue.setValue((Float) schemaInfo.value);
                floatFieldValueRepository.save(floatFieldValue);
                break;
            case STRING:
                StringFieldValue stringFieldValue = new StringFieldValue();
                stringFieldValue.setFieldVersion(fieldVersion);
                stringFieldValue.setValue((String) schemaInfo.value);
                stringFieldValueRepository.save(stringFieldValue);
                break;
            case BOOLEAN:
                BooleanFieldValue boolFieldValue = new BooleanFieldValue();
                boolFieldValue.setFieldVersion(fieldVersion);
                boolFieldValue.setValue((Boolean) schemaInfo.value);
                booleanFieldValueRepository.save(boolFieldValue);
                break;
            case INTEGER:
                IntegerFieldValue integerFieldValue = new IntegerFieldValue();
                integerFieldValue.setFieldVersion(fieldVersion);
                integerFieldValue.setValue((Integer) schemaInfo.value);
                integerFieldValueRepository.save(integerFieldValue);
                break;
            case STRING_ARRAY:
                List<String> values = (List<String>) schemaInfo.value;
                for (String value : values) {
                    StringArrayFieldValue stringArrayFieldValue = new StringArrayFieldValue();
                    stringArrayFieldValue.setFieldVersion(fieldVersion);
                    stringArrayFieldValue.setValue(value);
                    stringArrayFieldValueRepository.save(stringArrayFieldValue);
                }
                break;
        }
    }

    @Test
    public void testSchemaCreation() {
        Optional<ArtifactType> artifactTypeOptional = artifactTypeRepository.findByProjectAndNameIgnoreCase(project, typeName);
        assertTrue(artifactTypeOptional.isPresent());

        ArtifactType artifactType = artifactTypeOptional.get();
        List<ArtifactSchemaField> artifactFields = artifactSchemaFieldRepository.findByArtifactType(artifactType);
        assertEquals(fields.size(), artifactFields.size());

        for (ArtifactSchemaField field : artifactFields) {
            FieldSchemaInfo schemaInfo = fields.get(field.getType());
            assertEquals(schemaInfo.displayName, field.getLabel());
            assertEquals(schemaInfo.keyName, field.getKeyname());

            if (field.getType().getExtraInfoType() == ArtifactFieldExtraInfoType.FLOAT_BOUNDS) {
                Optional<FloatFieldInfo> floatFieldInfo = floatFieldInfoRepository.findBySchemaField(field);
                assertTrue(floatFieldInfo.isPresent());
                assertEquals(floatMax, floatFieldInfo.get().getMax());
                assertEquals(floatMin, floatFieldInfo.get().getMin());
            } else if (field.getType().getExtraInfoType() == ArtifactFieldExtraInfoType.INT_BOUNDS) {
                Optional<IntegerFieldInfo> integerFieldInfo = integerFieldInfoRepository.findBySchemaField(field);
                assertTrue(integerFieldInfo.isPresent());
                assertEquals(intMax, integerFieldInfo.get().getMax());
                assertEquals(intMin, integerFieldInfo.get().getMin());
            } else if (field.getType().getExtraInfoType() == ArtifactFieldExtraInfoType.OPTIONS) {
                List<SelectionFieldOption> options = selectionFieldOptionRepository.findBySchemaField(field);
                List<String> values = options.stream().map(SelectionFieldOption::getValue).collect(Collectors.toList());
                assertEquals(selections, values);
            }
        }
    }

    @Test
    public void testFieldValueCreation() {
        List<ArtifactFieldVersion> fieldVersions = artifactFieldVersionRepository.findByArtifactVersion(artifactVersion);
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
                    assertEquals(schemaInfo.value, intValue);
                    break;
                case BOOLEAN:
                    boolean boolValue = fieldVersion.getBooleanValue();
                    assertEquals(schemaInfo.value, boolValue);
                    break;
                case FLOAT:
                    float floatValue = fieldVersion.getFloatValue();
                    assertEquals(schemaInfo.value, floatValue);
                    break;
                case STRING_ARRAY:
                    List<String> stringArrayValue = fieldVersion.getStringArrayValue();
                    assertEquals(schemaInfo.value, stringArrayValue);
                    break;
            }
        }
    }

    @AllArgsConstructor
    private static class FieldSchemaInfo {
        public String displayName;
        public String keyName;
        public Object value;
    }
}
