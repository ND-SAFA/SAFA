package edu.nd.crc.safa.features.notifications.builders;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class ProjectChangeBuilder extends AbstractEntityChangeBuilder<ProjectChangeBuilder> {

    public ProjectChangeBuilder(SafaUser user, Project project) {
        super(user.getUserId());
        String projectTopic = TopicCreator.getProjectTopic(project.getProjectId());
        this.getEntityChangeMessage().setTopic(projectTopic);
    }

    public ProjectChangeBuilder withArtifactsUpdate(List<UUID> artifactIds) {
        return (ProjectChangeBuilder) withEntityUpdate(NotificationEntity.ARTIFACTS, artifactIds);
    }

    public ProjectChangeBuilder withTraceMatrixUpdate(TraceMatrixAppEntity traceMatrix) {
        return withTraceMatricesUpdate(List.of(traceMatrix));
    }

    public ProjectChangeBuilder withTraceMatricesUpdate(List<TraceMatrixAppEntity> traceMatrices) {
        return (ProjectChangeBuilder) withEntitiesUpdate(NotificationEntity.TRACE_MATRICES, traceMatrices);
    }

    public ProjectChangeBuilder withTraceMatrixDelete(UUID matrixId) {
        return withTraceMatricesDelete(List.of(matrixId));
    }

    public ProjectChangeBuilder withTraceMatricesDelete(List<UUID> matrixIds) {
        return (ProjectChangeBuilder) withEntityDelete(NotificationEntity.TRACE_MATRICES, matrixIds);
    }

    public ProjectChangeBuilder withTypeUpdate(ArtifactType artifactType) {
        return (ProjectChangeBuilder) withEntitiesUpdate(NotificationEntity.TYPES, List.of(artifactType));
    }

    public ProjectChangeBuilder withTypeDelete(UUID artifactTypeId) {
        return (ProjectChangeBuilder) withEntityDelete(NotificationEntity.TYPES, List.of(artifactTypeId));
    }

    public ProjectChangeBuilder withProjectUpdate(UUID projectId) {
        return (ProjectChangeBuilder) withEntityUpdate(NotificationEntity.PROJECT, List.of(projectId));
    }

    public ProjectChangeBuilder withMembersUpdate(UUID membershipId) {
        return (ProjectChangeBuilder) withEntityUpdate(NotificationEntity.MEMBERS, List.of(membershipId));
    }

    public ProjectChangeBuilder withMembersDelete(UUID projectId) {
        return (ProjectChangeBuilder) withEntityDelete(NotificationEntity.MEMBERS, List.of(projectId));
    }

    public ProjectChangeBuilder withDocumentUpdate(List<UUID> documentIds) {
        return (ProjectChangeBuilder) withEntityUpdate(NotificationEntity.DOCUMENT, documentIds);
    }

    public ProjectChangeBuilder withDocumentDelete(UUID documentId) {
        return (ProjectChangeBuilder) withEntityDelete(NotificationEntity.DOCUMENT, List.of(documentId));
    }

    public ProjectChangeBuilder withVersionUpdate(ProjectVersion projectVersion) {
        return (ProjectChangeBuilder) withEntityUpdate(NotificationEntity.VERSION,
            List.of(projectVersion.getVersionId()));
    }

    @Override
    protected ProjectChangeBuilder self() {
        return this;
    }
}
