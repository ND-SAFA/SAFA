package edu.nd.crc.safa.features.notifications.builders;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import lombok.NoArgsConstructor;

/**
 * Used to build multiple changes into an entity change.
 */
@NoArgsConstructor
public class EntityChangeBuilder {
    /**
     * The change being built.
     */
    private EntityChangeMessage entityChangeMessage;
    /**
     * Project defining what topic to send message to.
     */
    private UUID topicId;

    public EntityChangeBuilder(UUID topicId) {
        this.topicId = topicId;
        this.entityChangeMessage = new EntityChangeMessage();
    }

    public static EntityChangeBuilder create(ProjectVersion projectVersion) {
        return create(projectVersion.getVersionId());
    }

    public static EntityChangeBuilder create(Project project) {
        return create(project.getProjectId());
    }

    public static EntityChangeBuilder create(UUID topicId) {
        return new EntityChangeBuilder(topicId);
    }

    public static EntityChangeBuilder createJobUpdate(JobDbEntity jobDbEntity) {
        UUID jobId = jobDbEntity.getId();
        return create(jobId).withJobUpdate(jobId);
    }

    public EntityChangeMessage get(String email) {
        entityChangeMessage.setUser(email);
        return entityChangeMessage;
    }

    public String getTopic() {
        return NotificationService.getTopic(this.topicId);
    }

    public EntityChangeBuilder withProjectUpdate(UUID projectId) {
        return withEntityUpdate(Change.Entity.PROJECT, List.of(projectId));
    }

    public EntityChangeBuilder withMembersUpdate(UUID membershipId) {
        return withEntityUpdate(Change.Entity.MEMBERS, List.of(membershipId));
    }

    public EntityChangeBuilder withMembersDelete(UUID projectId) {
        return withEntityDelete(Change.Entity.MEMBERS, List.of(projectId));
    }

    public EntityChangeBuilder withTypeUpdate(UUID typeId) {
        return withEntityUpdate(Change.Entity.TYPES, List.of(typeId));
    }

    public EntityChangeBuilder withTypeDelete(UUID artifactTypeId) {
        return withEntityDelete(Change.Entity.TYPES, List.of(artifactTypeId));
    }

    public EntityChangeBuilder withVersionUpdate(UUID versionId) {
        return withEntityUpdate(Change.Entity.VERSION, List.of(versionId));
    }

    public EntityChangeBuilder withVersionDelete(UUID versionId) {
        return withEntityDelete(Change.Entity.VERSION, List.of(versionId));
    }

    public EntityChangeBuilder withDocumentUpdate(List<UUID> documentIds) {
        return withEntityUpdate(Change.Entity.DOCUMENT, documentIds);
    }

    public EntityChangeBuilder withDocumentDelete(UUID documentId) {
        return withEntityDelete(Change.Entity.DOCUMENT, List.of(documentId));
    }

    public EntityChangeBuilder withArtifactsUpdate(List<UUID> artifactIds) {
        return withEntityUpdate(Change.Entity.ARTIFACTS, artifactIds);
    }

    public EntityChangeBuilder withArtifactsDelete(List<UUID> artifactIds) {
        return withEntityDelete(Change.Entity.ARTIFACTS, artifactIds);
    }

    public EntityChangeBuilder withWarningsUpdate() {
        return withEntityUpdate(Change.Entity.WARNINGS, new ArrayList<>(), false);
    }

    public EntityChangeBuilder withTracesUpdate(List<UUID> traceIds) {
        return withEntityUpdate(Change.Entity.TRACES, traceIds);
    }

    public EntityChangeBuilder withTracesDelete(List<UUID> traceLinkIds) {
        return withEntityDelete(Change.Entity.TRACES, traceLinkIds);
    }

    public EntityChangeBuilder withJobUpdate(UUID jobId) {
        return withEntityUpdate(Change.Entity.JOBS, List.of(jobId));
    }

    public EntityChangeBuilder withJobDelete(UUID jobId) {
        return withEntityDelete(Change.Entity.JOBS, List.of(jobId));
    }

    private EntityChangeBuilder withEntityUpdate(Change.Entity entity, List<UUID> entityIds) {
        return withEntityUpdate(entity, entityIds, true);
    }

    private EntityChangeBuilder withEntityUpdate(Change.Entity entity,
                                                 List<UUID> entityIds,
                                                 boolean checkIfEmpty) {
        Change change = new Change(entity, Change.Action.UPDATE, entityIds);
        return addChange(change, checkIfEmpty);
    }

    private EntityChangeBuilder withEntityDelete(Change.Entity entity, List<UUID> entityIds) {
        return withEntityDelete(entity, entityIds, true);
    }

    private EntityChangeBuilder withEntityDelete(Change.Entity entity,
                                                 List<UUID> entityIds,
                                                 boolean checkIfEmpty) {
        Change change = new Change(entity, Change.Action.DELETE, entityIds);
        return addChange(change, checkIfEmpty);
    }

    private EntityChangeBuilder addChange(Change change, boolean checkIfEmpty) {
        if (checkIfEmpty) {
            if (!change.getEntityIds().isEmpty()) {
                this.entityChangeMessage.getChanges().add(change);
            }
        } else {
            this.entityChangeMessage.getChanges().add(change);
        }
        return this;
    }
}
