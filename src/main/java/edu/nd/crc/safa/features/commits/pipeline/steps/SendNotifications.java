package edu.nd.crc.safa.features.commits.pipeline.steps;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.pipeline.ICommitStep;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class SendNotifications implements ICommitStep {
    @Override
    public void performStep(CommitService service, ProjectCommit commit, ProjectCommit after) {
        // Step - Broadcast change
        ProjectVersion projectVersion = commit.getCommitVersion();
        ProjectChange<ArtifactAppEntity> artifactChanges = after.getArtifacts();
        ProjectChange<TraceAppEntity> traceChanges = after.getTraces();

        EntityChangeBuilder builder = new EntityChangeBuilder(projectVersion.getVersionId());
        builder
            .withArtifactsUpdate(artifactChanges.getUpdatedIds())
            .withArtifactsDelete(artifactChanges.getDeletedIds())
            .withTracesUpdate(traceChanges.getUpdatedIds())
            .withTracesDelete(traceChanges.getDeletedIds())
            .withWarningsUpdate();

        if (commit.shouldUpdateDefaultLayout()) {
            builder.withUpdateLayout();
        }

        service.getNotificationService().broadcastChangeToUser(builder, commit.getUser());
    }
}
