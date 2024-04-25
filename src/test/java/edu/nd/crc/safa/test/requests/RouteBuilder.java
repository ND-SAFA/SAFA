package edu.nd.crc.safa.test.requests;

import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.flatfiles.services.DataFileBuilder;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Given a route template, allows the users to specify the needed parameters and validates the final path.
 */
public class RouteBuilder<T extends RouteBuilder<T>> {
    protected String path;

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
        this.path = this.path.replace("{typeId}", artifactType.getId().toString());
        return (T) this;
    }

    public T withType(TypeAppEntity type) {
        this.path = this.path.replace("{typeId}", type.getTypeId().toString());
        return (T) this;
    }

    public T withDocument(Document document) {
        this.path = this.path.replace("{documentId}", document.getDocumentId().toString());
        return (T) this;
    }

    public T withDocument(DocumentAppEntity document) {
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

    public T withArtifactType(String artifactType) {
        this.path = this.path.replace("{artifactType}", artifactType);
        return (T) this;
    }

    public T withArtifactId(Artifact artifact) {
        return this.withArtifactId(artifact.getArtifactId());
    }

    public T withArtifactId(UUID artifactId) {
        this.path = this.path.replace("{artifactId}", artifactId.toString());
        return (T) this;
    }

    public T withProjectMembership(ProjectMembership projectMembership) {
        this.path = this.path.replace("{projectMembershipId}", projectMembership.getMembershipId().toString());
        return (T) this;
    }

    public T withSourceArtifactTypeName(String sourceArtifactTypeName) {
        this.path = this.path.replace("{sourceArtifactTypeName}", sourceArtifactTypeName);
        return (T) this;
    }

    public T withTargetArtifactTypeName(String targetArtifactTypeName) {
        this.path = this.path.replace("{targetArtifactTypeName}", targetArtifactTypeName);
        return (T) this;
    }

    public T withJob(JobDbEntity job) {
        this.path = this.path.replace("{jobId}", job.getId().toString());
        return (T) this;
    }

    public T withJob(JobAppEntity job) {
        this.path = this.path.replace("{jobId}", job.getId().toString());
        return (T) this;
    }

    public T withStepNum(int stepNum) {
        this.path = this.path.replace("{stepNum}", Integer.toString(stepNum));
        return (T) this;
    }

    public T withFileType(DataFileBuilder.AcceptedFileTypes fileType) {
        this.path = this.path.replace("{fileType}", fileType.toString());
        return (T) this;
    }

    public T withModelId(UUID modelId) {
        this.path = this.path.replace("{modelId}", modelId.toString());
        return (T) this;
    }

    public T withRepositoryName(String repositoryName) {
        this.path = this.path.replace("{repositoryName}", repositoryName);
        return (T) this;
    }

    public T withOwner(String owner) {
        this.path = this.path.replace("{owner}", owner);
        return (T) this;
    }

    public T withId(UUID id) {
        this.path = this.path.replace("{id}", id.toString());
        return (T) this;
    }

    public T withKey(String key) {
        this.path = this.path.replace("{key}", key);
        return (T) this;
    }

    public T withOrgId(UUID orgId) {
        this.path = this.path.replace("{orgId}", orgId.toString());
        return (T) this;
    }

    public T withTeamId(UUID teamId) {
        this.path = this.path.replace("{teamId}", teamId.toString());
        return (T) this;
    }

    public T withEntityId(UUID entityId) {
        this.path = this.path.replace("{entityId}", entityId.toString());
        return (T) this;
    }

    public T withMembershipId(UUID membershipId) {
        this.path = this.path.replace("{membershipId}", membershipId.toString());
        return (T) this;
    }

    public T withCustomReplacement(String paramName, Object paramValue) {
        String targetQuery = String.format("{%s}", paramName);
        this.path = this.path.replace(targetQuery, paramValue.toString());
        return (T) this;
    }

    public T withPathVariable(String name, String value) {
        this.path = this.path.replace(String.format("{%s}", name), value);
        return (T) this;
    }

    public String buildEndpoint() {
        if (this.path.contains("{")) {
            throw new SafaError("Path is not fully configured: %s", this.path);
        }
        return this.path;
    }

}
