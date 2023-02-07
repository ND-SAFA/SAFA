package features.flatfiles.logic;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Map;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.utilities.FileUtilities;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import common.ApplicationBaseTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import requests.SafaRequest;

public class TestCustomAttributes extends ApplicationBaseTest {

    @Test
    void testCsvImport() throws Exception {
        String baseRoute = AppRoutes.FlatFiles.PARSE_ARTIFACT_FILE;
        String type = "Requirement";
        String pathToFile = FileUtilities.buildPath(ProjectPaths.Resources.Tests.CUSTOM_ATTRIBUTES, "Requirements.csv");

        JSONObject resultJson = SafaRequest
                .withRoute(baseRoute)
                .withArtifactType(type)
                .getFlatFileHelper()
                .postWithFile(pathToFile);

        System.out.println(resultJson);

        EntityParsingResult<ArtifactAppEntity, String> result = JsonFileUtilities.parse(resultJson.toString(), new TypeReference<>(){});

        assertEquals(0, result.getErrors().size());
        assertEquals(1, result.getEntities().size());

        ArtifactAppEntity parsedEntity = result.getEntities().get(0);
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
}
