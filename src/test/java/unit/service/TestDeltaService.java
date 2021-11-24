package unit.service;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.server.entities.app.ProjectDelta;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.services.DeltaService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;

public class TestDeltaService extends EntityBaseTest {

    @Autowired
    DeltaService deltaService;

    @Test
    public void calculateModifiedSingleArtifact() throws ServerError {
        String projectName = "test-project";
        String artifactType = "requirement";
        String artifactName = "RE-8";
        String artifactSummary = "this is a summary";
        String artifactBody = "this is a body";
        String newArtifactBody = "this is a different body";

        // Step - Create project with: type, artifact, and body
        dbEntityBuilder
            .newProject(projectName)
            .newType(projectName, artifactType)
            .newVersion(projectName)
            .newArtifact(projectName, artifactType, artifactName)
            .newArtifactBody(projectName, artifactName, artifactSummary, artifactBody); // first body

        // VP - Delta against same version is empty
        ProjectVersion firstVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        ProjectDelta deltaZero = deltaService.calculateProjectDelta(firstVersion, firstVersion);
        assertThat(deltaZero.getModified().size()).isEqualTo(0);
        assertThat(deltaZero.getRemoved().size()).isEqualTo(0);
        assertThat(deltaZero.getAdded().size()).isEqualTo(0);

        // Step - Create second version with modified artifacts
        ProjectVersion secondVersion = dbEntityBuilder.newVersionWithReturn(projectName);
        dbEntityBuilder
            .newArtifactBody(projectName, 1, ModificationType.MODIFIED, artifactName, artifactSummary, newArtifactBody);

        // VP - Verify that system able to detect if modified
        ProjectDelta deltaOne = deltaService.calculateProjectDelta(firstVersion, secondVersion);
        assertThat(deltaOne.getModified().size()).isEqualTo(1);
        assertThat(deltaOne.getRemoved().size()).isEqualTo(0);
        assertThat(deltaOne.getAdded().size()).isEqualTo(0);

        // VP - Remove artifact
        ProjectVersion thirdVersion = dbEntityBuilder.newVersionWithReturn(projectName);
        dbEntityBuilder
            .newArtifactBody(projectName, 2, ModificationType.REMOVED, artifactName, "", "");
        ProjectDelta deltaTwo = deltaService.calculateProjectDelta(secondVersion, thirdVersion);
        assertThat(deltaTwo.getModified().size()).isEqualTo(0);
        assertThat(deltaTwo.getRemoved().size()).isEqualTo(1);
        assertThat(deltaTwo.getAdded().size()).isEqualTo(0);

        // VP - Remove artifact
        ProjectVersion fourthVersion = dbEntityBuilder.newVersionWithReturn(projectName);
        dbEntityBuilder
            .newArtifactBody(projectName, 3, artifactName, artifactSummary, artifactBody);
        ProjectDelta deltaThree = deltaService.calculateProjectDelta(thirdVersion, fourthVersion);
        assertThat(deltaThree.getModified().size()).isEqualTo(0);
        assertThat(deltaThree.getRemoved().size()).isEqualTo(0);
        assertThat(deltaThree.getAdded().size()).isEqualTo(1);
    }
}
