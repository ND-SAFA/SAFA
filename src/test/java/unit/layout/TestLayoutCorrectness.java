package unit.layout;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.layout.LayoutPosition;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

public class TestLayoutCorrectness extends ApplicationBaseTest {
    String projectName = "project name";
    String artifactType = "Requirement";
    String artifactBody = "This is body";

    @Test
    public void simpleLayout() throws Exception {
        String a1Name = "R1";
        String a2Name = "R2";
        String a3Name = "R3";

        // Step - Create project
        ProjectVersion projectVersion = this.dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);
        this.jsonBuilder.withProject(projectName, projectName, "");
        commit(CommitBuilder.withVersion(projectVersion)
            .withAddedArtifact(createArtifact(a1Name))
            .withAddedArtifact(createArtifact(a2Name))
            .withAddedArtifact(createArtifact(a3Name))
            .withAddedTrace(jsonBuilder.createTrace(a2Name, a1Name))
            .withAddedTrace(jsonBuilder.createTrace(a3Name, a1Name)));

        // Step - Create layout
        ProjectAppEntity project = getProjectAtVersion(projectVersion);

        // Step - Extract positions
        LayoutPosition a1Pos = getPosition(project, a1Name);
        LayoutPosition a2Pos = getPosition(project, a2Name);
        LayoutPosition a3Pos = getPosition(project, a3Name);

        // VP - Verify that root has greatest y
        assertThat(a1Pos.getY()).isLessThan(a2Pos.getY());
        assertThat(a1Pos.getY()).isLessThan(a3Pos.getY());
    }

    private JSONObject createArtifact(String artifactName) {
        return jsonBuilder.withArtifactAndReturn(
            projectName, "", artifactName, artifactType, artifactBody
        );
    }

    private LayoutPosition getPosition(ProjectAppEntity project, String artifactName) {
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
}
