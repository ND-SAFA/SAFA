package features.artifacts.crud;

import java.util.Hashtable;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.SafetyCaseType;
import edu.nd.crc.safa.features.artifacts.entities.db.SafetyCaseArtifact;
import edu.nd.crc.safa.features.artifacts.repositories.SafetyCaseArtifactRepository;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.app.IProjectEntityRetriever;
import edu.nd.crc.safa.features.projects.services.AppEntityRetrievalService;

import features.artifacts.base.AbstractArtifactTest;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that the client is allowed to CRUD Safety Case Artifacts
 */
public class TestSafetyCaseArtifacts extends AbstractArtifactTest<SafetyCaseArtifact> {

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
