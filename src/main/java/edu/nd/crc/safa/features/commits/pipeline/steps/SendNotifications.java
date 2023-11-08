package edu.nd.crc.safa.features.commits.pipeline.steps;

import java.util.List;

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

        List<TraceAppEntity> updatedTraces = traceChanges.getModified();
        updatedTraces.addAll(traceChanges.getAdded());

        List<ArtifactAppEntity> updatedArtifacts = artifactChanges.getModified();
        updatedArtifacts.addAll(artifactChanges.getAdded());

        ProjectVersionChangeBuilder builder = EntityChangeBuilder
            .create(user, projectVersion)
            .withArtifactsUpdate(updatedArtifacts)
            .withArtifactsDelete(artifactChanges.getDeletedIds())
            .withTracesUpdate(updatedTraces)
            .withTracesDelete(traceChanges.getDeletedIds())
            .withWarningsUpdate();

        if (commitDefinition.shouldUpdateDefaultLayout()) {
            builder.withUpdateLayout();
        }

        service.getNotificationService().broadcastChange(builder);
    }
}
