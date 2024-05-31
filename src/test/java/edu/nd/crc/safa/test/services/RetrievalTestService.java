package edu.nd.crc.safa.test.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.authentication.AuthorizationSetter;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.DbEntityBuilder;

import lombok.AllArgsConstructor;
import org.json.JSONArray;

@AllArgsConstructor
public class RetrievalTestService {
    ServiceProvider serviceProvider;
    DbEntityBuilder dbEntityBuilder;

    public ProjectAppEntity getProjectAtVersion(ProjectVersion projectVersion) {
        AuthorizationSetter.setSessionAuthorization(ApplicationBaseTest.currentUserName, this.serviceProvider);
        return this.serviceProvider.getProjectRetrievalService().getProjectAppEntity(projectVersion);
    }

    public String getId(String projectName, String artifactName) {
        Project project = this.dbEntityBuilder.getProject(projectName);
        Optional<Artifact> artifactOptional = this.serviceProvider
            .getArtifactRepository()
            .findByProjectIdAndName(project.getId(),
                artifactName);
        if (artifactOptional.isPresent()) {
            return artifactOptional.get().getArtifactId().toString();
        }
        throw new RuntimeException("Could not find artifact with name:" + artifactName);
    }

    public JSONArray getProjectMembers(Project project) {
        return SafaRequest
            .withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
            .withEntityId(project.getProjectId())
            .getWithJsonArray();
    }

    public UUID getArtifactId(List<ArtifactAppEntity> artifacts, String artifactName) {
        ArtifactAppEntity artifact =
            artifacts
                .stream()
                .filter(a -> a.getName().equals(artifactName))
                .toList()
                .get(0);
        return artifact.getId();
    }
}
