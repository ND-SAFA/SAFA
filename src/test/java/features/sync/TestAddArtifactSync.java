package features.sync;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;

import builders.CommitBuilder;
import common.EntityConstants;

public class TestAddArtifactSync extends AbstractSyncTest {
    private final EntityConstants.ArtifactConstants artifactConstants = new EntityConstants.ArtifactConstants();
    private UUID artifactId;

    @Override
    void performAction() throws Exception {
        ProjectCommit projectCommit = this.commitService.commit(CommitBuilder
            .withVersion(this.projectVersion)
            .withAddedArtifact(artifactConstants.artifact));
        this.artifactId = projectCommit.getArtifact(ModificationType.ADDED, 0).getId();
    }

    @Override
    void verifyActionMessage(EntityChangeMessage message) {
        this.changeMessageVerifies.verifyArtifactMessage(
            message,
            this.artifactId,
            Change.Action.UPDATE);
        this.changeMessageVerifies.verifyWarningMessage(message);
        this.changeMessageVerifies.verifyUpdateLayout(message, true);
    }

    @Override
    void verifyChanges(ProjectAppEntity project) {
        // VP - Verify single artifact was retrieved
        assertThat(project.getArtifacts()).hasSize(1);

        // Step - Retrieve artifact retrieved
        ArtifactAppEntity artifact = project.getArtifacts().get(0);

        // VP - Verify artifact with correct name was retrieved
        assertThat(artifact.getName()).isEqualTo(artifactConstants.name);

        // VP - Verify that
        assertThat(project.getLayout()).isNotEmpty().containsKey(artifact.getId());

        // VP - Verify that layout contains artifact created
        LayoutPosition layoutPosition = project.getLayout().get(artifact.getId());
        assertThat(layoutPosition.getX()).isNotNegative();
        assertThat(layoutPosition.getY()).isNotNegative();

        // VP - Verify that non-included information not retrieved
        assertThat(project.getDocuments()).isEmpty();
        assertThat(project.getTraces()).isEmpty();
        assertThat(project.getName()).isEmpty();
        assertThat(project.getDescription()).isEmpty();
    }
}
