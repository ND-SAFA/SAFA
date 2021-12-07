package unit.project.artifacts;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.EntityVersionService;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Verifies that:
 * 1. We are able to find the last inputted artifact body.
 */
public class TestArtifactService extends ApplicationBaseTest {


    @Autowired
    EntityVersionService entityVersionService;

    @Test
    public void checkAbleToFindLastArtifactBody() {
        String artifactName = "RE-8";
        String artifactTypeName = "requirements";
        String summary = "this is a summary";
        String body = "this is a body";
        String projectName = "test-project";

        // Step - Create project, with type, artifact, and body.
        Project project = dbEntityBuilder.newProjectWithReturn(projectName);
        dbEntityBuilder
            .newVersion(projectName)
            .newType(projectName, artifactTypeName)
            .newArtifact(projectName, artifactTypeName, artifactName)
            .newArtifactBody(projectName, artifactName, summary, body);
        Artifact artifact = dbEntityBuilder.getArtifact(projectName, artifactName);

        //VP - Able to find first created body
        Optional<ArtifactVersion> artifactBodyQuery = this.artifactVersionRepository.findLastArtifactBody(project, artifact);

        assertThat(artifactBodyQuery.isPresent()).isTrue();
        ArtifactVersion artifactVersionFound = artifactBodyQuery.get();
        assertThat(artifactVersionFound.getModificationType()).isEqualTo(ModificationType.ADDED);
        assertThat(artifactVersionFound.getArtifact().getBaseEntityId()).isEqualTo(artifactName);

        //Step 2 - Simulate new version added but artifact experienced no change
        dbEntityBuilder.newVersion(projectName);

        //Step 3 - Create third version with modified body
        dbEntityBuilder
            .newVersion(projectName)
            .newArtifactBodyWithReturn(projectName,
                2,
                ModificationType.REMOVED,
                artifactName,
                "",
                "");

        //VP 2 - Find new modified body
        artifactBodyQuery = this.artifactVersionRepository.findLastArtifactBody(project, artifact);

        assertThat(artifactBodyQuery.isPresent()).isTrue();
        artifactVersionFound = artifactBodyQuery.get();
        assertThat(artifactVersionFound.getModificationType()).isEqualTo(ModificationType.REMOVED);
        assertThat(artifactVersionFound.getArtifact().getBaseEntityId()).isEqualTo(artifactName);
        assertThat(artifactVersionFound.getContent()).isEqualTo("");
        assertThat(artifactVersionFound.getSummary()).isEqualTo("");
    }

    @Test
    public void testNoBodyFound() {
        String artifactName = "RE-8";
        String artifactTypeName = "requirements";
        String projectName = "test-project";
        dbEntityBuilder
            .newProject(projectName)
            .newType(projectName, artifactTypeName)
            .newArtifact(projectName, artifactTypeName, artifactName);

        Optional<ArtifactVersion> artifactBodyQuery = this.artifactVersionRepository
            .findLastArtifactBody(dbEntityBuilder.getProject(projectName),
                dbEntityBuilder.getArtifact(projectName, artifactName));
        assertThat(artifactBodyQuery.isPresent()).isFalse();
    }

    @Test
    public void testNoChangeDetected() throws SafaError {
        String projectName = "test-project";
        String artifactTypeName = "requirement";
        String artifactName = "RE-8";
        String artifactContent = "this is a body";
        String artifactSummary = "this is a summary";

        // Step - Create project with: v1, type, artifact, body
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, artifactTypeName)
            .newArtifact(projectName, artifactTypeName, artifactName)
            .newArtifactBody(projectName, artifactName, artifactSummary, artifactContent);

        // Step - Create new version + update artifact with same artifact (no change)
        ArtifactVersion artifactVersion = dbEntityBuilder.getArtifactBody(projectName, artifactName, 0);
        ArtifactAppEntity artifactApp = new ArtifactAppEntity(artifactVersion);

        // VP - Verify that no new entry has been created
        ProjectVersion newVersion = dbEntityBuilder.newVersionWithReturn(projectName);
        Artifact artifact = dbEntityBuilder.getArtifact(projectName, artifactName);

        entityVersionService.commitVersionArtifacts(newVersion, Arrays.asList(artifactApp));
        List<ArtifactVersion> artifactBodies = this.artifactVersionRepository.findByArtifact(artifact);
        assertThat(artifactBodies.size()).isEqualTo(1);
    }

    @Test
    public void artifactModificationDetected() throws SafaError {
        String projectName = "test-project";
        String typeName = "requirements";
        String artifactName = "RE-8";
        String artifactSummary = "this is a summary";
        String newContent = "this is a new content text";

        // Step - Create project with: version, type, artifact, body
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, typeName)
            .newArtifact(projectName, typeName, artifactName)
            .newArtifactBody(projectName, artifactName, "", "");

        // Step - Create new version and updated artifact
        ProjectVersion projectVersion = dbEntityBuilder.newVersionWithReturn(projectName);
        Artifact artifact = dbEntityBuilder.getArtifact(projectName, artifactName);
        String artifactId = artifact.getArtifactId().toString();
        ArtifactAppEntity appEntity = new ArtifactAppEntity(
            artifactId,
            typeName,
            artifactName,
            artifactSummary,
            newContent);

        // VP - Verify that artifact body is detected to be modified
        this.entityVersionService.commitVersionArtifacts(projectVersion,
            Arrays.asList(appEntity));
        Optional<ArtifactVersion> updatedBodyQuery =
            this.artifactVersionRepository.findByProjectVersionAndArtifact(projectVersion,
                artifact);
        assertThat(updatedBodyQuery.isPresent()).isTrue();
        ArtifactVersion updatedBody = updatedBodyQuery.get();
        assertThat(updatedBody.getModificationType()).isEqualTo(ModificationType.MODIFIED);
        assertThat(updatedBody.getContent()).isEqualTo(newContent);
    }
}
