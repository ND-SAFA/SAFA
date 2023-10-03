package edu.nd.crc.safa.features.notifications.builders;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.CustomAttributeAppEntity;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

public class ProjectChangeBuilder extends AbstractEntityChangeBuilder<ProjectChangeBuilder> {

    public ProjectChangeBuilder(SafaUser user, Project project) {
        super(user.getUserId());
        String projectTopic = TopicCreator.getProjectTopic(project.getProjectId());
        this.getEntityChangeMessage().setTopic(projectTopic);
    }

    public ProjectChangeBuilder withArtifactsUpdate(List<UUID> artifactIds) {
        return withEntityUpdate(NotificationEntity.ARTIFACTS, artifactIds);
    }

    public ProjectChangeBuilder withTraceMatrixUpdate(TraceMatrixAppEntity traceMatrix) {
        return withTraceMatricesUpdate(List.of(traceMatrix));
    }

    public ProjectChangeBuilder withTraceMatricesUpdate(List<TraceMatrixAppEntity> traceMatrices) {
        return withEntitiesUpdate(NotificationEntity.TRACE_MATRICES, traceMatrices);
    }

    public ProjectChangeBuilder withTraceMatrixDelete(UUID matrixId) {
        return withTraceMatricesDelete(List.of(matrixId));
    }

    public ProjectChangeBuilder withTraceMatricesDelete(List<UUID> matrixIds) {
        return withEntityDelete(NotificationEntity.TRACE_MATRICES, matrixIds);
    }

    public ProjectChangeBuilder withTypeUpdate(ArtifactType artifactType) {
        return withEntitiesUpdate(NotificationEntity.TYPES, List.of(artifactType));
    }

    public ProjectChangeBuilder withTypeDelete(UUID artifactTypeId) {
        return withEntityDelete(NotificationEntity.TYPES, List.of(artifactTypeId));
    }

    public ProjectChangeBuilder withProjectUpdate(UUID projectId) {
        return withEntityUpdate(NotificationEntity.PROJECT, List.of(projectId));
    }

    public ProjectChangeBuilder withMembersUpdate(UUID membershipId) {
        return withEntityUpdate(NotificationEntity.MEMBERS, List.of(membershipId));
    }

    public ProjectChangeBuilder withMembersDelete(UUID projectId) {
        return withEntityDelete(NotificationEntity.MEMBERS, List.of(projectId));
    }

    public ProjectChangeBuilder withDocumentUpdate(List<UUID> documentIds) {
        return withEntityUpdate(NotificationEntity.DOCUMENT, documentIds);
    }

    public ProjectChangeBuilder withDocumentDelete(UUID documentId) {
        return withEntityDelete(NotificationEntity.DOCUMENT, List.of(documentId));
    }

    public ProjectChangeBuilder withAttributeUpdate(CustomAttributeAppEntity customAttribute) {
        return withEntitiesUpdate(NotificationEntity.ATTRIBUTES, List.of(customAttribute));
    }

    public ProjectChangeBuilder withAttributeDelete(UUID attributeId) {
        return withEntityDelete(NotificationEntity.ATTRIBUTES, List.of(attributeId));
    }

    @Override
    protected ProjectChangeBuilder self() {
        return this;
    }
}
