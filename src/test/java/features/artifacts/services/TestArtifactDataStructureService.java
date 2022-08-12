package features.artifacts.services;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.Arrays;
import java.util.Hashtable;
import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.flatfiles.entities.common.ProjectEntities;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.ProjectChanger;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.Test;

/**
 * Verifies that:
 * 1. We are able to find the last inputted artifact body.
 */
class TestArtifactDataStructureService extends ApplicationBaseTest {

    @Test
    void checkAbleToFindLastArtifactBody() {
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

        assertThat(artifactBodyQuery).isPresent();
        ArtifactVersion artifactVersionFound = artifactBodyQuery.get();
        assertThat(artifactVersionFound.getModificationType()).isEqualTo(ModificationType.ADDED);
        assertThat(artifactVersionFound.getArtifact().getName()).isEqualTo(artifactName);

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

        assertThat(artifactBodyQuery).isPresent();
        artifactVersionFound = artifactBodyQuery.get();
        assertThat(artifactVersionFound.getModificationType()).isEqualTo(ModificationType.REMOVED);
        assertThat(artifactVersionFound.getArtifact().getName()).isEqualTo(artifactName);
        assertThat(artifactVersionFound.getContent()).isEmpty();
        assertThat(artifactVersionFound.getSummary()).isEmpty();
    }

    @Test
    void testNoBodyFound() {
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
        assertThat(artifactBodyQuery).isEmpty();
    }

    @Test
    void testNoChangeDetected() throws SafaError {
        String projectName = "test-project";
        String artifactTypeName = "requirement";
        String artifactName = "RE-8";
        String artifactContent = "this is a body";
        String artifactSummary = "this is a summary";

        // Step - Create project with: version, type, artifact, body
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, artifactTypeName)
            .newArtifact(projectName, artifactTypeName, artifactName)
            .newArtifactBody(projectName, artifactName, artifactSummary, artifactContent);

        // Step - Create new version
        ProjectVersion newVersion = dbEntityBuilder.newVersionWithReturn(projectName);
        Artifact artifact = dbEntityBuilder.getArtifact(projectName, artifactName);

        ArtifactVersion artifactVersion = dbEntityBuilder.getArtifactBody(projectName, artifactName, 0);
        ArtifactAppEntity artifactApp = this.artifactVersionRepository
            .retrieveAppEntityFromVersionEntity(artifactVersion);

        setAuthorization(); // Required because getting currentDocument requires a user be logged in
        ProjectEntities projectEntities = new ProjectEntities(Arrays.asList(artifactApp));
        ProjectChanger projectChanger = new ProjectChanger(newVersion, serviceProvider);
        projectChanger.setEntitiesAsCompleteSet(projectEntities);
        
        List<ArtifactVersion> artifactBodies = this.artifactVersionRepository.findByArtifact(artifact);
        assertThat(artifactBodies).hasSize(1);
    }

    @Test
    void artifactModificationDetected() throws SafaError {
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
            newContent,
            DocumentType.ARTIFACT_TREE,
            new Hashtable<>());

        // VP - Verify that artifact body is detected to be modified
        setAuthorization(); // Required because getting currentDocument requires a user be logged in
        ProjectEntities projectEntities = new ProjectEntities(List.of(appEntity));
        ProjectChanger projectChanger = new ProjectChanger(projectVersion, serviceProvider);
        projectChanger.setEntitiesAsCompleteSet(projectEntities);

        Optional<ArtifactVersion> updatedBodyQuery =
            this.artifactVersionRepository.findByProjectVersionAndArtifact(projectVersion,
                artifact);
        assertThat(updatedBodyQuery).isPresent();
        ArtifactVersion updatedBody = updatedBodyQuery.get();
        assertThat(updatedBody.getModificationType()).isEqualTo(ModificationType.MODIFIED);
        assertThat(updatedBody.getContent()).isEqualTo(newContent);
    }
}
