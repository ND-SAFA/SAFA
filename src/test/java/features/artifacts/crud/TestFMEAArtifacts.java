package features.artifacts.crud;

import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.app.DocumentColumnDataType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.app.IProjectEntityRetriever;
import edu.nd.crc.safa.features.projects.entities.app.ProjectRetriever;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import features.artifacts.base.AbstractArtifactTest;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that the client is allowed to CRUD Safety Case Artifacts
 */
public class TestFMEAArtifacts extends AbstractArtifactTest<Artifact> {

    String artifactType = "requirements";
    Map<String, String> customFields = new Hashtable<>() {{
        put("someField", "someValue");
    }};

    @Autowired
    ProjectRetriever artifactRepository;

    @Override
    public JSONObject getArtifactJson(String projectName, String artifactName, String artifactBody) {
        return this.jsonBuilder
            .withProject(projectName, projectName, projectDescription)
            .withFMEAArtifact(projectName, artifactName, artifactType, artifactBody, JsonFileUtilities.toJson(customFields))
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
        expectedProperties.put("customFields", JsonFileUtilities.toJson(customFields));
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
