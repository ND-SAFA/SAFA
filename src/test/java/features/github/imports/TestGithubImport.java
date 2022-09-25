package features.github.imports;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import features.github.base.AbstractGithubTest;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import org.json.JSONObject;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import requests.SafaRequest;

public class TestGithubImport extends AbstractGithubTest {

    protected String repositoryName = "repository";

    @Test
    void baseTest() throws Exception {
        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Import.BY_NAME)
            .withRepositoryName(repositoryName)
            .postWithoutBody(status().is2xxSuccessful());

        // We should have one version created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        GithubProject githubProject = serviceProvider.getGithubProjectRepository().findAll().get(0);

        // We should have the corespondent project and user set
        Assertions.assertNotNull(githubProject.getProject());
        // We should have as many artifacts as the number of files produced by the mock service
        Assertions.assertEquals(
            serviceMock.getRepositoryFiles(credentials, repositoryName, "sha")
                .filterOutFolders().getTree().size(),
            serviceProvider.getArtifactRepository()
                .findByProject(githubProject.getProject()).size()
        );
    }
}
