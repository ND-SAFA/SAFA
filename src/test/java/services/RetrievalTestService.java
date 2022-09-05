package services;

import static features.base.ApplicationBaseTest.defaultUser;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.AuthorizationSetter;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import builders.DbEntityBuilder;
import lombok.AllArgsConstructor;
import org.json.JSONArray;
import requests.SafaRequest;

@AllArgsConstructor
public class RetrievalTestService {
    ServiceProvider serviceProvider;
    DbEntityBuilder dbEntityBuilder;


    public ProjectAppEntity getProjectAtVersion(ProjectVersion projectVersion) {
        AuthorizationSetter.setSessionAuthorization(defaultUser, this.serviceProvider);
        return this.serviceProvider.getProjectRetrievalService().getProjectAppEntity(projectVersion);
    }


    public String getId(String projectName, String artifactName) {
        Project project = this.dbEntityBuilder.getProject(projectName);
        Optional<Artifact> artifactOptional = this.serviceProvider
            .getArtifactRepository()
            .findByProjectAndName(project,
                artifactName);
        if (artifactOptional.isPresent()) {
            return artifactOptional.get().getArtifactId().toString();
        }
        throw new RuntimeException("Could not find artifact with name:" + artifactName);
    }

    public JSONArray getProjectMembers(Project project) throws Exception {
        return SafaRequest
            .withRoute(AppRoutes.Projects.Membership.GET_PROJECT_MEMBERS)
            .withProject(project)
            .getWithJsonArray();
    }

    public UUID getArtifactId(List<ArtifactAppEntity> artifacts, String artifactName) {
        ArtifactAppEntity artifact =
            artifacts
                .stream()
                .filter(a -> a.getName().equals(artifactName))
                .collect(Collectors.toList())
                .get(0);
        return artifact.getId();
    }
}
