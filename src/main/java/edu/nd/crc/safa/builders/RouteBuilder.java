package edu.nd.crc.safa.builders;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

/**
 * Given a route template, allows the users to specify the needed parameters and validates the final path.
 */
public class RouteBuilder<T extends RouteBuilder<T>> {
    String path;

    public RouteBuilder(String path) {
        this.path = path;
    }

    public static RouteBuilder withRoute(String routeTemplate) {
        return new RouteBuilder(routeTemplate);
    }

    public T withVersion(ProjectVersion version) {
        this.path = this.path.replace("{versionId}", version.getVersionId().toString());
        return (T) this;
    }

    public T withProject(Project project) {
        this.path = this.path.replace("{projectId}", project.getProjectId().toString());
        return (T) this;
    }

    public T withType(ArtifactType artifactType) {
        this.path = this.path.replace("{typeId}", artifactType.getTypeId().toString());
        return (T) this;
    }

    public T withDocument(Document document) {
        this.path = this.path.replace("{documentId}", document.getDocumentId().toString());
        return (T) this;
    }

    public T withBaselineVersion(ProjectVersion baselineVersion) {
        this.path = this.path.replace("{baselineVersionId}", baselineVersion.getVersionId().toString());
        return (T) this;
    }

    public T withTargetVersion(ProjectVersion targetVersion) {
        this.path = this.path.replace("{targetVersionId}", targetVersion.getVersionId().toString());
        return (T) this;
    }

    public RouteBuilder withArtifactType(String artifactType) {
        this.path = this.path.replace("{artifactType}", artifactType);
        return this;
    }

    public RouteBuilder withArtifactId(Artifact artifact) {
        this.path = this.path.replace("{artifactId}", artifact.getArtifactId().toString());
        return this;
    }

    public RouteBuilder withProjectMembership(ProjectMembership projectMembership) {
        this.path = this.path.replace("{projectMembershipId}", projectMembership.getMembershipId().toString());
        return this;
    }

    public RouteBuilder withSourceArtifactTypeName(String sourceArtifactTypeName) {
        this.path = this.path.replace("{sourceArtifactTypeName}", sourceArtifactTypeName);
        return this;
    }

    public RouteBuilder withTargetArtifactTypeName(String targetArtifactTypeName) {
        this.path = this.path.replace("{targetArtifactTypeName}", targetArtifactTypeName);
        return this;
    }

    public RouteBuilder withJob(JobDbEntity job) {
        this.path = this.path.replace("{jobId}", job.getId().toString());
        return this;
    }

    public String buildEndpoint() {
        if (this.path.contains("{")) {
            throw new RuntimeException("Path is not fully configured:" + this.path);
        }
        return this.path;
    }
}
