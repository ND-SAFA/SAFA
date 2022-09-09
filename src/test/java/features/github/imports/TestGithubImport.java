package features.github.imports;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.github.entities.app.GithubResponseDTO;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import features.github.base.AbstractGithubTest;

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
        // We should have one GitHub project created
        Assertions.assertEquals(1, serviceProvider.getProjectVersionRepository().count());
        // We should have as many artifacts as the number of files produces by the mock service
        Assertions.assertEquals(
            serviceMock.getRepositoryFiles(credentials, repositoryName, "sha")
                .getTree().size(),
            serviceProvider.getArtifactRepository().count()
        );
    }
}
