package edu.nd.crc.safa.test.features.traces.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.AbstractCrudTest;
import edu.nd.crc.safa.test.services.builders.CommitBuilder;
import edu.nd.crc.safa.test.services.builders.ProjectBuilder;

public class TraceCrudTest extends AbstractCrudTest<TraceAppEntity> {
    private final TraceAppEntity trace = new TraceAppEntity(
        null,
        "R0",
        null,
        "D0",
        null,
        ApprovalStatus.UNREVIEWED,
        0.5,
        TraceType.GENERATED,
        true,
        null
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
    protected List<String> getTopic() {
        String topic = TopicCreator.getVersionTopic(this.projectVersion.getVersionId());
        return List.of(topic);
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
    protected void verifyCreationMessages(List<EntityChangeMessage> creationMessages) {
        assertThat(creationMessages).hasSize(1);
        verifyTraceUpdateMessage(creationMessages.get(0));
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
    protected void verifyUpdateMessages(List<EntityChangeMessage> updateMessages) {
        assertThat(updateMessages).hasSize(1);
        verifyTraceUpdateMessage(updateMessages.get(0));
    }

    @Override
    protected void deleteEntity(TraceAppEntity entity) throws Exception {
        commitService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withRemovedTrace(entity));
    }

    @Override
    protected void verifyDeletionMessages(List<EntityChangeMessage> deletionMessages) {
        assertThat(deletionMessages).hasSize(1);
        messageVerificationService.verifyTraceMessage(deletionMessages.get(0), entityId, NotificationAction.DELETE);
    }

    private void verifyTraceUpdateMessage(EntityChangeMessage message) {
        messageVerificationService.verifyTraceMessage(message, entityId, NotificationAction.UPDATE);
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
