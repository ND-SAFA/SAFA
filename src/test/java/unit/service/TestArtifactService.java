package unit.service;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.Optional;

import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.ModificationType;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.server.services.ArtifactService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;

/**
 * Verifies that:
 * 1. We are able to find the last inputted artifact body.
 */
public class TestArtifactService extends EntityBaseTest {


    @Autowired
    ArtifactService artifactService;

    @Test
    public void checkAbleToFindLastArtifactBody() {
        String artifactName = "RE-8";
        String artifactTypeName = "requirements";
        String summary = "this is a summary";
        String body = "this is a body";
        String projectName = "test-project";

        // Step - Create project, with type, artifact, and body.
        Project project = entityBuilder.newProjectWithReturn(projectName);
        entityBuilder
            .newVersion(projectName)
            .newType(projectName, artifactTypeName)
            .newArtifact(projectName, artifactTypeName, artifactName)
            .newArtifactBody(projectName, artifactName, summary, body);
        Artifact artifact = entityBuilder.getArtifact(projectName, artifactName);

        //VP - Able to find first created body
        Optional<ArtifactBody> artifactBodyQuery = this.artifactBodyRepository.findLastArtifactBody(project, artifact);

        assertThat(artifactBodyQuery.isPresent()).isTrue();
        ArtifactBody artifactBodyFound = artifactBodyQuery.get();
        assertThat(artifactBodyFound.getModificationType()).isEqualTo(ModificationType.ADDED);
        assertThat(artifactBodyFound.getArtifact().getName()).isEqualTo(artifactName);

        //Step 2 - Simulate new version added but artifact experienced no change
        entityBuilder.newVersion(projectName);

        //Step 3 - Create third version with modified body
        entityBuilder
            .newVersion(projectName)
            .newArtifactBodyWithReturn(projectName,
                2,
                ModificationType.REMOVED,
                artifactName,
                null,
                null);

        //VP 2 - Find new modified body
        artifactBodyQuery = this.artifactBodyRepository.findLastArtifactBody(project, artifact);

        assertThat(artifactBodyQuery.isPresent()).isTrue();
        artifactBodyFound = artifactBodyQuery.get();
        assertThat(artifactBodyFound.getModificationType()).isEqualTo(ModificationType.REMOVED);
        assertThat(artifactBodyFound.getArtifact().getName()).isEqualTo(artifactName);
        assertThat(artifactBodyFound.getContent()).isNull();
        assertThat(artifactBodyFound.getSummary()).isNull();
    }

    @Test
    public void testNoBodyFound() {
        String artifactName = "RE-8";
        String artifactTypeName = "requirements";
        String projectName = "test-project";
        entityBuilder
            .newProject(projectName)
            .newType(projectName, artifactTypeName)
            .newArtifact(projectName, artifactTypeName, artifactName);

        Optional<ArtifactBody> artifactBodyQuery = this.artifactBodyRepository
            .findLastArtifactBody(entityBuilder.getProject(projectName),
                entityBuilder.getArtifact(projectName, artifactName));
        assertThat(artifactBodyQuery.isPresent()).isFalse();
    }
}
