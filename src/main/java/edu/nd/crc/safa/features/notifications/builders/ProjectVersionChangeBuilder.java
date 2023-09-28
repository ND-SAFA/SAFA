package edu.nd.crc.safa.features.notifications.builders;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class ProjectVersionChangeBuilder extends AbstractEntityChangeBuilder {

    public ProjectVersionChangeBuilder(SafaUser user, ProjectVersion projectVersion) {
        super(user.getUserId());
        String versionTopic = TopicCreator.getVersionTopic(projectVersion.getVersionId());
        this.getEntityChangeMessage().setTopic(versionTopic);
    }

    public ProjectVersionChangeBuilder withVersionDelete(UUID versionId) {
        return (ProjectVersionChangeBuilder) withEntityDelete(Change.Entity.VERSION, List.of(versionId));
    }

    public ProjectVersionChangeBuilder withArtifactsUpdate(List<UUID> artifactIds) {
        return (ProjectVersionChangeBuilder) withEntityUpdate(Change.Entity.ARTIFACTS, artifactIds);
    }

    public ProjectVersionChangeBuilder withArtifactsDelete(List<UUID> artifactIds) {
        return (ProjectVersionChangeBuilder) withEntityDelete(Change.Entity.ARTIFACTS, artifactIds);
    }

    public ProjectVersionChangeBuilder withWarningsUpdate() {
        return (ProjectVersionChangeBuilder) withEntityUpdate(Change.Entity.WARNINGS, new ArrayList<>(), false);
    }

    public ProjectVersionChangeBuilder withTracesUpdate(List<UUID> traceIds) {
        return (ProjectVersionChangeBuilder) withEntityUpdate(Change.Entity.TRACES, traceIds);
    }

    public ProjectVersionChangeBuilder withTracesDelete(List<UUID> traceLinkIds) {
        return (ProjectVersionChangeBuilder) withEntityDelete(Change.Entity.TRACES, traceLinkIds);
    }
}
