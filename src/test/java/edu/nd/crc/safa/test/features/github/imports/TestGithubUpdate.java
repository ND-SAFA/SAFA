package edu.nd.crc.safa.test.features.github.imports;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.projects.entities.db.Project;
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
        GithubProject githubProject = new GithubProject();

        githubProject.setProject(project);
        githubProject.setRepositoryName(repositoryName);
        githubProject.setBranch("branch");
        githubProject.setLastCommitSha("sha");
        serviceProvider.getGithubProjectRepository().save(githubProject);

        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Import.UPDATE)
            .withRepositoryName(repositoryName)
            .withVersion(projectVersion)
            .putWithoutBody(MockMvcResultMatchers.status().is2xxSuccessful());

        // No other project was created during the import
        Assertions.assertEquals(1, serviceProvider.getProjectRepository().count());

        // We should have one GitHub project created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        int diffArtifactsCount = serviceMock.getDiffBetweenOldCommitAndHead(credentials,
            repositoryName, "sha").getFiles().size();

        // We should have the correct number of artifacts and links
        Assertions.assertEquals(
            initialArtifactCount + diffArtifactsCount,
            serviceProvider.getArtifactRepository().findByProject(project).size());

        Assertions.assertEquals(0,
            serviceProvider.getTraceLinkRepository().count());
    }
}
