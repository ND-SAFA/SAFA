package edu.nd.crc.safa.builders;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceLink;

/**
 * Given a route template, allows the users to specify the needed parameters and validates the final path.
 */
public class RouteBuilder {
    String path;

    public RouteBuilder(String path) {
        this.path = path;
    }

    public static RouteBuilder withRoute(String routeTemplate) {
        return new RouteBuilder(routeTemplate);
    }

    public RouteBuilder withVersion(ProjectVersion version) {
        this.path = this.path.replace("{versionId}", version.getVersionId().toString());
        return this;
    }

    public RouteBuilder withProject(Project project) {
        this.path = this.path.replace("{projectId}", project.getProjectId().toString());
        return this;
    }

    public RouteBuilder withType(ArtifactType artifactType) {
        this.path = this.path.replace("{typeId}", artifactType.getTypeId().toString());
        return this;
    }

    public RouteBuilder withDocument(Document document) {
        this.path = this.path.replace("{documentId}", document.getDocumentId().toString());
        return this;
    }

    public RouteBuilder withBaselineVersion(ProjectVersion baselineVersion) {
        this.path = this.path.replace("{baselineVersionId}", baselineVersion.getVersionId().toString());
        return this;
    }

    public RouteBuilder withTargetVersion(ProjectVersion targetVersion) {
        this.path = this.path.replace("{targetVersionId}", targetVersion.getVersionId().toString());
        return this;
    }

    public RouteBuilder withArtifactType(String artifactType) {
        this.path = this.path.replace("{artifactType}", artifactType);
        return this;
    }

    public RouteBuilder withTraceLink(TraceLink traceLink) {
        this.path = this.path.replace("{traceLinkId}", traceLink.getTraceLinkId().toString());
        return this;
    }

    public RouteBuilder withSourceName(String sourceId) {
        this.path = this.path.replace("{sourceId}", sourceId);
        return this;
    }

    public RouteBuilder withTargetName(String sourceId) {
        this.path = this.path.replace("{targetId}", sourceId);
        return this;
    }

    public RouteBuilder withArtifactId(Artifact artifact) {
        this.path = this.path.replace("{artifactId}", artifact.getArtifactId().toString());
        return this;
    }

    public RouteBuilder withArtifactName(String artifactName) {
        this.path = this.path.replace("{artifactName}", artifactName);
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

    public RouteBuilder withTraceMatrixId(String traceMatrixId) {
        this.path = this.path.replace("{traceMatrixId}", traceMatrixId);
        return this;
    }

    public String get() {
        if (this.path.contains("{")) {
            throw new RuntimeException("Path is not fully configured:" + this.path);
        }
        return this.path;
    }
}
