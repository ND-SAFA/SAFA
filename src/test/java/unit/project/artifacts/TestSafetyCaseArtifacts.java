package unit.project.artifacts;

import java.util.Hashtable;
import java.util.Map;

import edu.nd.crc.safa.server.entities.app.SafetyCaseType;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.SafetyCaseArtifact;
import edu.nd.crc.safa.server.repositories.artifacts.IProjectEntityRetriever;
import edu.nd.crc.safa.server.repositories.artifacts.SafetyCaseArtifactRepository;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that the client is allowed to CRUD Safety Case Artifacts
 */
public class TestSafetyCaseArtifacts extends ArtifactBaseTest<SafetyCaseArtifact> {

    SafetyCaseType safetyCaseType = SafetyCaseType.SOLUTION;
    String safetyCaseTypeName = safetyCaseType.toString();
    DocumentType documentType = DocumentType.SAFETY_CASE;

    @Autowired
    SafetyCaseArtifactRepository safetyCaseArtifactRepository;

    @Autowired
    AppEntityRetrievalService appEntityRetrievalService;

    @Override
    public JSONObject getArtifactJson(String projectName, String artifactName, String artifactBody) {
        return jsonBuilder
            .withProject(projectName, projectName, "")
            .withSafetyCaseArtifact(projectName, artifactName, safetyCaseTypeName, artifactBody, safetyCaseType)
            .getArtifact(projectName, artifactName);
    }

    @Override
    public String getArtifactType() {
        return safetyCaseTypeName;
    }

    @Override
    public DocumentType getDocumentType() {
        return documentType;
    }

    @Override
    public Map<String, Object> getJsonExpectedProperties() {
        Hashtable<String, Object> expectedProperties = new Hashtable<>();
        expectedProperties.put("safetyCaseType", safetyCaseType);
        return expectedProperties;
    }

    @Override
    public IProjectEntityRetriever getArtifactRepository() {
        return safetyCaseArtifactRepository;
    }

    @Override
    public Class getArtifactClass() {
        return SafetyCaseArtifact.class;
    }

}
