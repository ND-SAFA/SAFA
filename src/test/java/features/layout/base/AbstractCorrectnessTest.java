package features.layout.base;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import com.fasterxml.jackson.core.JsonProcessingException;
import features.base.ApplicationBaseTest;
import org.json.JSONArray;
import org.json.JSONObject;

public abstract class AbstractCorrectnessTest extends ApplicationBaseTest {
    protected String projectName = "project name";
    protected String artifactType = "Requirement";
    protected String artifactBody = "This is body";

    protected String a1Name = "R1";
    protected String a2Name = "R2";
    protected String a3Name = "R3";

    protected ProjectVersion projectVersion;

    public JSONObject createProject() throws Exception {
        this.jsonBuilder.withProject(projectName, projectName, "");
        this.projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        this.jsonBuilder.withProject(projectName, projectName, "");
        return commit(CommitBuilder.withVersion(projectVersion)
            .withAddedArtifact(createArtifact(a1Name))
            .withAddedArtifact(createArtifact(a2Name))
            .withAddedArtifact(createArtifact(a3Name))
            .withAddedTrace(jsonBuilder.createTrace(a2Name, a1Name))
            .withAddedTrace(jsonBuilder.createTrace(a3Name, a1Name)));
    }

    /**
     * Makes the following assertions about the following structure:
     * - Root node is above both children
     * - Children have the same height
     *
     * @param rootPos        The position of the root node.
     * @param firstChildPos  The position of one of the children.
     * @param secondChildPos The position of the other child.
     */
    protected void assertLayoutCorrectness(LayoutPosition rootPos,
                                           LayoutPosition firstChildPos,
                                           LayoutPosition secondChildPos) {
        assertThat(rootPos.getY()).isLessThan(firstChildPos.getY());
        assertThat(rootPos.getY()).isLessThan(secondChildPos.getY());
        assertThat(firstChildPos.getY()).isEqualTo(secondChildPos.getY());
    }

    protected JSONObject createArtifact(String artifactName) {
        return jsonBuilder.withArtifactAndReturn(
            projectName, "", artifactName, artifactType, artifactBody
        );
    }

    protected LayoutPosition getPosition(ProjectAppEntity project, String artifactName) {
        ArtifactAppEntity artifact =
            project
                .artifacts
                .stream()
                .filter(a -> a.name.equals(artifactName))
                .collect(Collectors.toList())
                .get(0);
        String id = artifact.getId();
        return project.getLayout().get(id);
    }

    protected LayoutPosition getArtifactPositionInProjectLayout(ProjectAppEntity project,
                                                                String documentId,
                                                                String artifactName) {
        String artifactId = getArtifactId(project.artifacts, artifactName);
        return project
            .getDocuments()
            .stream()
            .filter(d -> d.getDocumentId().toString().equals(documentId))
            .findFirst()
            .get()
            .getLayout()
            .get(artifactId);
    }

    protected List<String> getArtifactIds(JSONObject projectCommit) {
        return new ArrayList<>(getArtifactNameToIdMap(projectCommit).values());
    }

    protected String getArtifactIdFromProjectCommit(JSONObject projectCommit, String artifactName) {
        return getArtifactNameToIdMap(projectCommit).get(artifactName);
    }

    protected List<LayoutPosition> getArtifactPositionsInDocument(
        JSONObject projectCommit,
        JSONObject documentJson,
        List<String> artifactNames) throws JsonProcessingException {
        DocumentAppEntity document = toClass(documentJson.toString(), DocumentAppEntity.class);
        return artifactNames.stream()
            .map(artifactName -> {
                String artifactId = getArtifactIdFromProjectCommit(projectCommit, artifactName);
                return document.getLayout().get(artifactId);
            })
            .collect(Collectors.toList());
    }

    private Map<String, String> getArtifactNameToIdMap(JSONObject projectCommit) {
        Map<String, String> name2id = new Hashtable<>();
        JSONArray artifactsJson = projectCommit.getJSONObject("artifacts").getJSONArray("added");
        for (int i = 0; i < artifactsJson.length(); i++) {
            JSONObject artifactAdded = artifactsJson.getJSONObject(i);
            String artifactId = artifactAdded.getString("id");
            String artifactName = artifactAdded.getString("name");
            name2id.put(artifactName, artifactId);
        }
        return name2id;
    }
}
