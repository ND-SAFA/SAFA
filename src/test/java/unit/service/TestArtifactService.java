package unit.service;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.server.db.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.server.db.entities.sql.ModificationType;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.messages.ServerError;
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

    @Test
    public void testNoChangeDetected() throws ServerError {
        String projectName = "test-project";
        String artifactTypeName = "requirement";
        String artifactName = "RE-8";
        String artifactContent = "this is a body";
        String artifactSummary = "this is a summary";

        // Step - Create project with: v1, type, artifact, body
        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, artifactTypeName)
            .newArtifact(projectName, artifactTypeName, artifactName)
            .newArtifactBody(projectName, artifactName, artifactSummary, artifactContent);

        // Step - Create new version + update artifact with same artifact (no change)
        ArtifactBody artifactBody = entityBuilder.getArtifactBody(projectName, artifactName, 0);
        ArtifactAppEntity artifactApp = new ArtifactAppEntity(artifactBody);

        // VP - Verify that no new entry has been created
        ProjectVersion newVersion = entityBuilder.newVersionWithReturn(projectName);
        Artifact artifact = entityBuilder.getArtifact(projectName, artifactName);

        artifactService.createOrUpdateArtifacts(newVersion, Arrays.asList(artifactApp));
        List<ArtifactBody> artifactBodies = this.artifactBodyRepository.findByArtifact(artifact);
        assertThat(artifactBodies.size()).isEqualTo(1);
    }

    @Test
    public void artifactModificationDetected() throws ServerError {
        String projectName = "test-project";
        String typeName = "requirements";
        String artifactName = "RE-8";
        String newContent = "this is a new content text";

        // Step - Create project with: version, type, artifact, body
        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, typeName)
            .newArtifact(projectName, typeName, artifactName)
            .newArtifactBody(projectName, artifactName, "", "");

        // Step - Create new version and updated artifact
        ProjectVersion projectVersion = entityBuilder.newVersionWithReturn(projectName);
        Artifact artifact = entityBuilder.getArtifact(projectName, artifactName);
        ArtifactAppEntity appEntity = new ArtifactAppEntity(typeName, artifactName, "", newContent);

        // VP - Verify that artifact body is detected to be modified
        this.artifactService.createOrUpdateArtifacts(projectVersion,
            Arrays.asList(appEntity));
        Optional<ArtifactBody> updatedBodyQuery =
            this.artifactBodyRepository.findByProjectVersionAndArtifact(projectVersion,
                artifact);
        assertThat(updatedBodyQuery.isPresent()).isTrue();
        ArtifactBody updatedBody = updatedBodyQuery.get();
        assertThat(updatedBody.getModificationType()).isEqualTo(ModificationType.MODIFIED);
        assertThat(updatedBody.getContent()).isEqualTo(newContent);
    }
}
