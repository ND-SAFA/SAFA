package unit.project.artifacts;

import java.util.Hashtable;
import java.util.Map;

import edu.nd.crc.safa.server.entities.app.FTANodeType;
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

    FTANodeType ftaNodeType = FTANodeType.AND;
    String ftaType = ftaNodeType.toString();

    @Autowired
    FTAArtifactRepository ftaArtifactRepository;


    @Override
    public JSONObject getArtifactJson(String projectName, String artifactName, String artifactBody) {
        return jsonBuilder
            .withProject(projectName, projectName, "")
            .withFTAArtifact(projectName, artifactName, ftaType, artifactBody, ftaNodeType)
            .getArtifact(projectName, artifactName);
    }

    @Override
    public String getArtifactType() {
        return ftaType;
    }

    @Override
    public DocumentType getDocumentType() {
        return DocumentType.FTA;
    }

    @Override
    public Map<String, Object> getJsonExpectedProperties() {
        Hashtable<String, Object> expectedProperties = new Hashtable<>();
        expectedProperties.put("logicType", ftaNodeType);
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
