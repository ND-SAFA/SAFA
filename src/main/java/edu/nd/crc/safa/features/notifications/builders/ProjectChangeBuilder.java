package edu.nd.crc.safa.features.notifications.builders;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class ProjectChangeBuilder extends AbstractEntityChangeBuilder {

    public ProjectChangeBuilder(SafaUser user, Project project) {
        super(user.getUserId());
        String projectTopic = TopicCreator.getProjectTopic(project.getProjectId());
        this.getEntityChangeMessage().setTopic(projectTopic);
    }

    public ProjectChangeBuilder withArtifactsUpdate(List<UUID> artifactIds) {
        return (ProjectChangeBuilder) withEntityUpdate(Change.Entity.ARTIFACTS, artifactIds);
    }

    public ProjectChangeBuilder withTraceMatrixUpdate(UUID matrixId) {
        return withTraceMatricesUpdate(List.of(matrixId));
    }

    public ProjectChangeBuilder withTraceMatricesUpdate(List<UUID> matrixIds) {
        return (ProjectChangeBuilder) withEntityUpdate(Change.Entity.TRACE_MATRICES, matrixIds);
    }

    public ProjectChangeBuilder withTraceMatrixDelete(UUID matrixId) {
        return withTraceMatricesDelete(List.of(matrixId));
    }

    public ProjectChangeBuilder withTraceMatricesDelete(List<UUID> matrixIds) {
        return (ProjectChangeBuilder) withEntityDelete(Change.Entity.TRACE_MATRICES, matrixIds);
    }

    public ProjectChangeBuilder withTypeUpdate(UUID typeId) {
        return (ProjectChangeBuilder) withEntityUpdate(Change.Entity.TYPES, List.of(typeId));
    }

    public ProjectChangeBuilder withTypeDelete(UUID artifactTypeId) {
        return (ProjectChangeBuilder) withEntityDelete(Change.Entity.TYPES, List.of(artifactTypeId));
    }

    public ProjectChangeBuilder withProjectUpdate(UUID projectId) {
        return (ProjectChangeBuilder) withEntityUpdate(Change.Entity.PROJECT, List.of(projectId));
    }

    public ProjectChangeBuilder withMembersUpdate(UUID membershipId) {
        return (ProjectChangeBuilder) withEntityUpdate(Change.Entity.MEMBERS, List.of(membershipId));
    }

    public ProjectChangeBuilder withMembersDelete(UUID projectId) {
        return (ProjectChangeBuilder) withEntityDelete(Change.Entity.MEMBERS, List.of(projectId));
    }

    public ProjectChangeBuilder withDocumentUpdate(List<UUID> documentIds) {
        return (ProjectChangeBuilder) withEntityUpdate(Change.Entity.DOCUMENT, documentIds);
    }

    public ProjectChangeBuilder withDocumentDelete(UUID documentId) {
        return (ProjectChangeBuilder) withEntityDelete(Change.Entity.DOCUMENT, List.of(documentId));
    }

    public ProjectChangeBuilder withVersionUpdate(ProjectVersion projectVersion) {
        return (ProjectChangeBuilder) withEntityUpdate(Change.Entity.VERSION,
            List.of(projectVersion.getVersionId()));
    }
}
