package unit.project.artifacts;

import java.util.Hashtable;
import java.util.Map;

import edu.nd.crc.safa.server.entities.app.project.FTAType;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.FTAArtifact;
import edu.nd.crc.safa.server.repositories.artifacts.FTAArtifactRepository;
import edu.nd.crc.safa.server.repositories.artifacts.IProjectEntityRetriever;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that the client is allowed to CRUD Safety Case Artifacts
 */
public class TestFTAArtifacts extends ArtifactBaseTest<FTAArtifact> {

    FTAType ftaType = FTAType.AND;

    @Autowired
    FTAArtifactRepository ftaArtifactRepository;


    @Override
    public JSONObject getArtifactJson(String projectName, String artifactName, String artifactBody) {
        return jsonBuilder
            .withProject(projectName, projectName, "")
            .withFTAArtifact(projectName, artifactName, ftaType.name(), artifactBody, ftaType)
            .getArtifact(projectName, artifactName);
    }

    @Override
    public String getArtifactType() {
        return ftaType.name();
    }

    @Override
    public DocumentType getDocumentType() {
        return DocumentType.FTA;
    }

    @Override
    public Map<String, Object> getJsonExpectedProperties() {
        Hashtable<String, Object> expectedProperties = new Hashtable<>();
        expectedProperties.put("logicType", ftaType);
        return expectedProperties;
    }

    @Override
    public IProjectEntityRetriever<FTAArtifact> getArtifactRepository() {
        return ftaArtifactRepository;
    }

    @Override
    public Class getArtifactClass() {
        return FTAArtifact.class;
    }
}
