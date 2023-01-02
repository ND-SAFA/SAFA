package features.attributes;

import java.io.IOException;
import java.util.List;
import java.util.Optional;
import java.util.function.Function;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.values.ArtifactAttributeVersion;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;
import edu.nd.crc.safa.features.attributes.services.AttributeValueService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import com.fasterxml.jackson.core.JsonProcessingException;
import common.ApplicationBaseTest;
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

    private Project project;
    private ArtifactVersion artifactVersion;
    private final AttributesForTesting attributesForTesting = new AttributesForTesting();

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

        for (CustomAttributeType attributeType : CustomAttributeType.values()) {
            CustomAttribute attribute = attributesForTesting.setupAttribute(dbEntityBuilder, projectName, serviceProvider, attributeType);
            attributesForTesting.setupAttributeValueInitial(attribute, artifactVersion, attributeValueService);
        }
    }

    @Test
    public void testSchemaCreation() {
        List<CustomAttribute> artifactAttributes = serviceProvider.getCustomAttributeRepository().findByProject(project);
        assertEquals(CustomAttributeType.values().length, artifactAttributes.size());

        for (CustomAttribute attribute : artifactAttributes) {
            attributesForTesting.assertSchemaCorrectness(attribute, serviceProvider);
        }
    }

    @Test
    public void testAttributeValueCreation() throws JsonProcessingException {
        List<ArtifactAttributeVersion> attributeVersions = serviceProvider.getArtifactAttributeVersionRepository().findByArtifactVersion(artifactVersion);
        assertEquals(CustomAttributeType.values().length, attributeVersions.size());

        assertAttributeValues(attributeVersions, AttributesForTesting.AttributeInfo::getValue);
    }

    private void updateAttributes() {
        for (CustomAttributeType attributeType : CustomAttributeType.values()) {
            AttributesForTesting.AttributeInfo schemaInfo = attributesForTesting.attributes.get(attributeType);

            Optional<CustomAttribute> attributeOpt = serviceProvider.getCustomAttributeRepository()
                    .findByProjectAndKeyname(project, schemaInfo.keyName);

            assertTrue(attributeOpt.isPresent());

            attributeValueService.saveAttributeValue(attributeOpt.get(), artifactVersion, schemaInfo.altValue);
        }
    }

    private void assertAttributeValues(List<ArtifactAttributeVersion> attributeVersions,
                                       Function<AttributesForTesting.AttributeInfo, String> expectedValueFunc) throws JsonProcessingException {

        for (ArtifactAttributeVersion attributeVersion : attributeVersions) {
            attributesForTesting.assertAttributeValue(attributeVersion, expectedValueFunc);
        }
    }

    @Test
    public void testAttributeValueUpdate() throws JsonProcessingException {
        updateAttributes();

        List<ArtifactAttributeVersion> attributeVersions = serviceProvider.getArtifactAttributeVersionRepository().findByArtifactVersion(artifactVersion);
        assertEquals(CustomAttributeType.values().length, attributeVersions.size());

        assertAttributeValues(attributeVersions, AttributesForTesting.AttributeInfo::getAltValue);
    }

}
