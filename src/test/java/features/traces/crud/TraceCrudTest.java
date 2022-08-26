package features.traces.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import builders.CommitBuilder;
import builders.ProjectBuilder;
import common.AbstractCrudTest;

public class TraceCrudTest extends AbstractCrudTest<TraceAppEntity> {
    private final TraceAppEntity trace = new TraceAppEntity(
        null,
        "R0",
        null,
        "D0",
        null,
        ApprovalStatus.UNREVIEWED,
        0.5,
        TraceType.GENERATED
    );

    @Override
    public ProjectVersion setupProject() throws Exception {
        return ProjectBuilder.withProject(projectName)
            .withArtifact("Requirement")
            .withArtifact("Design")
            .getCurrentVersion()
            .getProjectVersion();
    }

    @Override
    protected UUID getTopicId() {
        return this.projectVersion.getVersionId();
    }

    @Override
    protected IAppEntityService<TraceAppEntity> getAppService() {
        return this.serviceProvider.getTraceService();
    }

    @Override
    protected UUID createEntity() throws Exception {
        TraceAppEntity traceAdded = commitTrace();

        // Step - Setting missing properties
        trace.setSourceId(traceAdded.getSourceId());
        trace.setTargetId(traceAdded.getTargetId());
        trace.setTraceLinkId(traceAdded.getTraceLinkId());

        return traceAdded.getTraceLinkId();
    }

    @Override
    protected void verifyCreatedEntity(TraceAppEntity retrievedEntity) {
        assertionService.assertMatch(trace, retrievedEntity);
    }

    @Override
    protected void verifyCreationMessage(EntityChangeMessage creationMessage) {
        verifyTraceUpdateMessage(creationMessage);
    }

    @Override
    protected void updateEntity() throws Exception {
        trace.setScore(1);
        commitTrace();
    }

    @Override
    protected void verifyUpdatedEntity(TraceAppEntity retrievedEntity) {
        assertionService.assertMatch(trace, retrievedEntity);
        assertThat(retrievedEntity.getScore()).isEqualTo(1);
    }

    @Override
    protected void verifyUpdateMessage(EntityChangeMessage updateMessage) {
        verifyTraceUpdateMessage(updateMessage);
    }

    @Override
    protected void deleteEntity(TraceAppEntity entity) throws Exception {
        commitService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withRemovedTrace(entity));
    }

    @Override
    protected void verifyDeletionMessage(EntityChangeMessage deletionMessage) {
        changeMessageVerifies.verifyTraceMessage(deletionMessage, entityId, Change.Action.DELETE);
    }

    private void verifyTraceUpdateMessage(EntityChangeMessage message) {
        changeMessageVerifies.verifyTraceMessage(message, entityId, Change.Action.UPDATE);
    }

    private TraceAppEntity commitTrace() throws Exception {
        return this.commitService
            .commit(
                CommitBuilder
                    .withVersion(projectVersion)
                    .withAddedTrace(trace))
            .getTraces()
            .getAdded()
            .get(0);
    }
}
