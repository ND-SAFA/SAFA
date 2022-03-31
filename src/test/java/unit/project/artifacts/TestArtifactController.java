package unit.project.artifacts;

import java.util.Hashtable;
import java.util.Map;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.repositories.artifacts.IProjectEntityRetriever;

import org.json.JSONObject;

/**
 * Tests that the client is allowed to:
 * 1. Add new artifacts
 * 2. Modify existing artifacts
 * 3. Delete existing artifacts
 */
public class TestArtifactController extends ArtifactBaseTest<Artifact> {

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
