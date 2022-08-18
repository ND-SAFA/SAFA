package features.traces.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.builders.entities.ProjectBuilder;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import common.AbstractCrudTest;
import org.json.JSONObject;

public class TraceCrudTest extends AbstractCrudTest<TraceAppEntity> {
    private final TraceAppEntity trace = new TraceAppEntity(
        "",
        "R0",
        "",
        "D0",
        "",
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
        JSONObject traceJson = commitTrace();
        String id = traceJson.getString("traceLinkId");

        // Step - Setting missing properties
        trace.setSourceId(traceJson.getString("sourceId"));
        trace.setTargetId(traceJson.getString("targetId"));
        trace.setTraceLinkId(id);

        return UUID.fromString(id);
    }

    @Override
    protected void verifyCreatedEntity(TraceAppEntity retrievedEntity) {
        assertionTestService.assertMatch(trace, retrievedEntity);
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
        assertionTestService.assertMatch(trace, retrievedEntity);
        assertThat(retrievedEntity.getScore()).isEqualTo(1);
    }

    @Override
    protected void verifyUpdateMessage(EntityChangeMessage updateMessage) {
        verifyTraceUpdateMessage(updateMessage);
    }

    @Override
    protected void deleteEntity(TraceAppEntity entity) throws Exception {
        commitTestService
            .commit(CommitBuilder
                .withVersion(projectVersion)
                .withRemovedTrace(entity));
    }

    @Override
    protected void verifyDeletionMessage(EntityChangeMessage deletionMessage) {
        messageVerificationTestService.verifyTraceMessage(deletionMessage, entityId, Change.Action.DELETE);
    }

    private void verifyTraceUpdateMessage(EntityChangeMessage message) {
        messageVerificationTestService.verifyTraceMessage(message, entityId, Change.Action.UPDATE);
    }

    private JSONObject commitTrace() throws Exception {
        return this.commitTestService
            .commit(
                CommitBuilder
                    .withVersion(projectVersion)
                    .withAddedTrace(trace))
            .getJSONObject("traces")
            .getJSONArray("added")
            .getJSONObject(0);
    }
}
