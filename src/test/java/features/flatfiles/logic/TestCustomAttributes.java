package features.flatfiles.logic;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.File;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;
import edu.nd.crc.safa.features.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import common.ApplicationBaseTest;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import requests.SafaRequest;

public class TestCustomAttributes extends ApplicationBaseTest {

    @Autowired
    AttributeSystemServiceProvider attributeSystemServiceProvider;

    @Test
    void testCsv() throws Exception {
        runTest(ProjectPaths.Resources.Tests.CUSTOM_ATTRIBUTES_CSV, DataFileBuilder.AcceptedFileTypes.CSV);
    }

    @Test
    void testJson() throws Exception {
        runTest(ProjectPaths.Resources.Tests.CUSTOM_ATTRIBUTES_JSON, DataFileBuilder.AcceptedFileTypes.JSON);
    }

    private void runTest(String resourcePath, DataFileBuilder.AcceptedFileTypes fileType) throws Exception {
        // Upload CSV files into first project
        ProjectVersion projectVersion = createProject(projectName);
        JSONObject resultJson = SafaRequest
            .withRoute(AppRoutes.FlatFiles.UPDATE_PROJECT_VERSION_FROM_FLAT_FILES)
            .withVersion(projectVersion)
            .getFlatFileHelper()
            .postWithFilesInDirectory(resourcePath, new JSONObject());

        // Check that the artifact was parsed correctly
        assertParsedArtifactValues(resultJson);

        // Download CSV files
        List<File> projectFiles = new SafaRequest(AppRoutes.FlatFiles.DOWNLOAD_FLAT_FILES)
            .withVersion(projectVersion)
            .withFileType(fileType)
            .getWithFilesInZip();

        // Upload the downloaded CSV files
        ProjectVersion newProjectVersion = createProject(projectName + "new");
        JSONObject newResultJson = SafaRequest
            .withRoute(AppRoutes.FlatFiles.UPDATE_PROJECT_VERSION_FROM_FLAT_FILES)
            .withVersion(newProjectVersion)
            .getFlatFileHelper()
            .postWithFiles(projectFiles, new JSONObject());

        // Check that the artifact was still parsed correctly
        assertParsedArtifactValues(newResultJson);
    }

    private void assertParsedArtifactValues(JSONObject resultJson) throws JsonProcessingException {
        JSONArray artifactsJson = resultJson.getJSONArray("artifacts");
        assertNotNull(artifactsJson);

        List<ArtifactAppEntity> result = new ObjectMapper().readValue(artifactsJson.toString(), new TypeReference<>(){});
        assertEquals(1, result.size());

        ArtifactAppEntity parsedEntity = result.get(0);
        assertEquals(3, parsedEntity.getAttributes().size());

        Map<String, JsonNode> attributes = parsedEntity.getAttributes();
        assertTrue(attributes.get("listAttr").isArray());
        assertTrue(attributes.get("intAttr").isInt());
        assertTrue(attributes.get("strAttr").isTextual());

        assertEquals(1, attributes.get("intAttr").asInt());
        assertEquals("strValue", attributes.get("strAttr").asText());
        assertEquals("val1", attributes.get("listAttr").get(0).asText());
        assertEquals("val2", attributes.get("listAttr").get(1).asText());
    }

    private ProjectVersion createProject(String projectName) {
        return dbEntityBuilder
            .newProject(projectName)
            .newCustomAttribute(projectName, CustomAttributeType.TEXT, "strAttr", "strAttr")
            .newCustomAttribute(projectName, CustomAttributeType.RELATION, "listAttr", "listAttr")
            .newCustomAttribute(projectName, CustomAttributeType.INT, "intAttr", "intAttr")
            .newVersionWithReturn(projectName);
    }
}
