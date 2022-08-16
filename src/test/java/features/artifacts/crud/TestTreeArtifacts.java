package features.artifacts.crud;

import java.util.Hashtable;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.app.IProjectEntityRetriever;

import features.artifacts.base.AbstractArtifactTest;
import org.json.JSONObject;

/**
 * Tests that the client is allowed to:
 * 1. Add new artifacts
 * 2. Modify existing artifacts
 * 3. Delete existing artifacts
 */
public class TestTreeArtifacts extends AbstractArtifactTest<Artifact> {

    String artifactType = "requirements";

    @Override
    public JSONObject getArtifactJson(String projectName, String artifactName, String artifactBody) {
        return jsonBuilder
            .withProject(projectName, projectName, "")
            .withArtifactAndReturn(projectName, "", artifactName, "requirements", "this is a body");
    }

    @Override
    public String getArtifactType() {
        return artifactType;
    }

    @Override
    public DocumentType getDocumentType() {
        return DocumentType.ARTIFACT_TREE;
    }

    @Override
    public Map<String, Object> getJsonExpectedProperties() {
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
}
