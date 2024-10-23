package edu.nd.crc.safa.test.features.github.imports;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.attributes.ReservedAttributes;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.github.base.AbstractGithubTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

public class TestGithubUpdate extends AbstractGithubTest {

    @Test
    void intoExistingProjectTest() throws Exception {
        String projectName = "githubImport";
        int initialArtifactCount = 5;

        this.createBaseSafaProject(projectName, initialArtifactCount);

        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        Project project = dbEntityBuilder.getProject(projectName);
        ArtifactType type = dbEntityBuilder.newTypeAndReturn(project.getName(), "test type");
        GithubProject githubProject = new GithubProject();

        githubProject.setProject(project);
        githubProject.setRepositoryName(repositoryName);
        githubProject.setBranch("branch");
        githubProject.setLastCommitSha("sha");
        githubProject.setOwner(githubLogin);
        githubProject.setArtifactType(type);
        serviceProvider.getGithubProjectRepository().save(githubProject);

        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Import.UPDATE)
            .withRepositoryName(repositoryName)
            .withOwner(githubLogin)
            .withVersion(projectVersion)
            .putWithJsonObject(new GithubImportDTO(), MockMvcResultMatchers.status().is2xxSuccessful());

        // No other project was created during the import
        Assertions.assertEquals(1, serviceProvider.getProjectRepository().count());

        // We should have one GitHub project created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        int diffArtifactsCount = 3;

        List<ArtifactAppEntity> artifacts = serviceProvider.getArtifactService().getAppEntities(project);

        // We should have the correct number of artifacts and links
        Assertions.assertEquals(initialArtifactCount + diffArtifactsCount, artifacts.size());

        for (ArtifactAppEntity artifact : artifacts) {
            if (artifact.getType().equals(type.getName())) {
                ReservedAttributes.Github.ALL_ATTRIBUTES
                    .forEach(key -> Assertions.assertTrue(artifact.getAttributes().containsKey(key)));
            }
        }

        Assertions.assertEquals(0,
            serviceProvider.getTraceLinkRepository().count());
    }

    @Test
    void intoExistingProjectWithIncludeAndExcludeTest() throws Exception {
        String projectName = "githubImport";
        int initialArtifactCount = 5;

        this.createBaseSafaProject(projectName, initialArtifactCount);

        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        Project project = dbEntityBuilder.getProject(projectName);
        ArtifactType type = dbEntityBuilder.newTypeAndReturn(project.getName(), "test type");
        GithubProject githubProject = new GithubProject();

        githubProject.setProject(project);
        githubProject.setRepositoryName(repositoryName);
        githubProject.setBranch("branch");
        githubProject.setLastCommitSha("sha");
        githubProject.setOwner(githubLogin);
        githubProject.setArtifactType(type);
        githubProject.setInclude("**/*.pl");
        githubProject.setExclude("modules/weather/**");
        serviceProvider.getGithubProjectRepository().save(githubProject);

        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Import.UPDATE)
            .withRepositoryName(repositoryName)
            .withOwner(githubLogin)
            .withVersion(projectVersion)
            .putWithJsonObject(new GithubImportDTO(), MockMvcResultMatchers.status().is2xxSuccessful());

        // No other project was created during the import
        Assertions.assertEquals(1, serviceProvider.getProjectRepository().count());

        // We should have one GitHub project created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        int diffArtifactsCount = 1;

        List<ArtifactAppEntity> artifacts = serviceProvider.getArtifactService().getAppEntities(project);

        // We should have the correct number of artifacts and links
        Assertions.assertEquals(initialArtifactCount + diffArtifactsCount, artifacts.size());

        for (ArtifactAppEntity artifact : artifacts) {
            if (artifact.getType().equals(type.getName())) {
                ReservedAttributes.Github.ALL_ATTRIBUTES
                    .forEach(key -> Assertions.assertTrue(artifact.getAttributes().containsKey(key)));
            }
        }

        Assertions.assertEquals(0,
            serviceProvider.getTraceLinkRepository().count());
    }
}
