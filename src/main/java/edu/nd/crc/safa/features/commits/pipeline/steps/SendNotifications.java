package edu.nd.crc.safa.features.commits.pipeline.steps;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.commits.pipeline.ICommitStep;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.builders.ProjectVersionChangeBuilder;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class SendNotifications implements ICommitStep {
    /**
     * Sends notification for all the entities changed.
     *
     * @param service          The commit service to access database and other services.
     * @param commitDefinition The commit being performed.
     * @param result           The commit final state.
     */
    @Override
    public void performStep(CommitService service, ProjectCommitDefinition commitDefinition,
                            ProjectCommitAppEntity result) {
        // Step - Broadcast change
        ProjectVersion projectVersion = commitDefinition.getCommitVersion();
        ProjectChange<ArtifactAppEntity> artifactChanges = result.getArtifacts();
        ProjectChange<TraceAppEntity> traceChanges = result.getTraces();
        SafaUser user = commitDefinition.getUser();

        ProjectVersionChangeBuilder builder = EntityChangeBuilder
            .create(user, projectVersion)
            .withArtifactsUpdate(artifactChanges.getUpdatedIds())
            .withArtifactsDelete(artifactChanges.getDeletedIds())
            .withTracesUpdate(traceChanges.getUpdatedIds())
            .withTracesDelete(traceChanges.getDeletedIds())
            .withWarningsUpdate();

        if (commitDefinition.shouldUpdateDefaultLayout()) {
            builder.withUpdateLayout();
        }

        service.getNotificationService().broadcastChange(builder);
    }
}
