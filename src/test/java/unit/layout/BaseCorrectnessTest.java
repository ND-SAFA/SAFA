package unit.layout;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import unit.ApplicationBaseTest;

public class BaseCorrectnessTest extends ApplicationBaseTest {
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

    protected void assertLayoutCorrectness(LayoutPosition a1Pos,
                                           LayoutPosition a2Pos,
                                           LayoutPosition a3Pos) {
        assertThat(a1Pos.getY()).isLessThan(a2Pos.getY());
        assertThat(a1Pos.getY()).isLessThan(a3Pos.getY());
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

    protected LayoutPosition getPositionInDocument(ProjectAppEntity project,
                                                   String documentId,
                                                   String artifactName) {
        return project
            .getDocumentLayouts()
            .get(documentId)
            .get(getArtifactId(project.artifacts, artifactName));
    }
}
