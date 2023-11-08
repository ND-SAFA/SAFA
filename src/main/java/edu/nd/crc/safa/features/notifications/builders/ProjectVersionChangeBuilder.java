package edu.nd.crc.safa.features.notifications.builders;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class ProjectVersionChangeBuilder extends AbstractEntityChangeBuilder<ProjectVersionChangeBuilder> {

    public ProjectVersionChangeBuilder(IUser user, ProjectVersion projectVersion) {
        super(user.getUserId());
        String versionTopic = TopicCreator.getVersionTopic(projectVersion.getVersionId());
        this.getEntityChangeMessage().setTopic(versionTopic);
    }

    public ProjectVersionChangeBuilder withDocumentUpdate(List<DocumentAppEntity> documents) {
        return withEntitiesUpdate(NotificationEntity.DOCUMENT, documents);
    }

    public ProjectVersionChangeBuilder withVersionDelete(UUID versionId) {
        return withEntityDelete(NotificationEntity.VERSION, List.of(versionId));
    }

    public ProjectVersionChangeBuilder withArtifactsUpdate(List<ArtifactAppEntity> artifacts) {
        return withEntitiesUpdate(NotificationEntity.ARTIFACTS, artifacts);
    }

    public ProjectVersionChangeBuilder withArtifactsDelete(List<UUID> artifactIds) {
        return withEntityDelete(NotificationEntity.ARTIFACTS, artifactIds);
    }

    public ProjectVersionChangeBuilder withWarningsUpdate() {
        return withEntityUpdate(NotificationEntity.WARNINGS, new ArrayList<>(), false);
    }

    public ProjectVersionChangeBuilder withTracesUpdate(List<TraceAppEntity> traces) {
        return withEntitiesUpdate(NotificationEntity.TRACES, traces);
    }

    public ProjectVersionChangeBuilder withTracesDelete(List<UUID> traceLinkIds) {
        return withEntityDelete(NotificationEntity.TRACES, traceLinkIds);
    }

    public ProjectVersionChangeBuilder withTypeUpdate(TypeAppEntity typeAppEntity) {
        return withEntitiesUpdate(NotificationEntity.TYPES, List.of(typeAppEntity));
    }

    @Override
    protected ProjectVersionChangeBuilder self() {
        return this;
    }
}
