package unit.project.artifacts;

import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.server.entities.app.DocumentColumnDataType;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.repositories.artifacts.IProjectEntityRetriever;
import edu.nd.crc.safa.server.repositories.artifacts.ProjectRetriever;
import edu.nd.crc.safa.utilities.JSONHelper;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that the client is allowed to CRUD Safety Case Artifacts
 */
public class TestFMEAArtifacts extends ArtifactBaseTest<Artifact> {

    String artifactType = "requirements";
    Map<String, String> customFields = new Hashtable<>() {{
        put("someField", "someValue");
    }};

    @Autowired
    ProjectRetriever artifactRepository;

    @Autowired
    JSONHelper jsonHelper;

    @Override
    public JSONObject getArtifactJson(String projectName, String artifactName, String artifactBody) {
        return this.jsonBuilder
            .withProject(projectName, projectName, projectDescription)
            .withFMEAArtifact(projectName, artifactName, artifactType, artifactBody, jsonHelper.map2Json(customFields))
            .getArtifact(projectName, artifactName);
    }

    @Override
    public String getArtifactType() {
        return artifactType;
    }

    @Override
    public DocumentType getDocumentType() {
        return DocumentType.FMEA;
    }

    @Override
    public Map<String, Object> getJsonExpectedProperties() {
        Map<String, Object> expectedProperties = new Hashtable<>();
        expectedProperties.put("customFields", jsonHelper.map2Json(customFields));
        return expectedProperties;
    }

    @Override
    public Map<String, Object> getEntityExpectedProperties() {
        return new Hashtable<>();
    }

    @Override
    public IProjectEntityRetriever<Artifact> getArtifactRepository() {
        return artifactRepository;
    }

    @Override
    public Class getArtifactClass() {
        return Artifact.class;
    }

    @Override
    protected JSONObject createDocumentJson() {
        JSONObject documentJson = super.createDocumentJson();
        JSONObject columnsJson = this.jsonBuilder.createDocumentColumn("", documentName,
            DocumentColumnDataType.SELECT);
        documentJson.put("columns", List.of(columnsJson));
        return documentJson;
    }
}
