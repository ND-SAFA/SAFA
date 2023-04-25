package edu.nd.crc.safa.test.features.github.base;

import java.io.IOException;

import edu.nd.crc.safa.features.github.services.GithubGraphQlService;
import edu.nd.crc.safa.test.common.AbstractRemoteApiTest;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.test.util.ReflectionTestUtils;

public abstract class AbstractGithubGraphqlTest extends AbstractRemoteApiTest {
    private String githubUrlSave;

    @BeforeEach
    public void setupGithubGraphQlService() {
        GithubGraphQlService githubGraphQlService = serviceProvider.getGithubGraphQlService();
        githubUrlSave = (String) ReflectionTestUtils.getField(githubGraphQlService, "githubGraphqlUrl");
        ReflectionTestUtils.setField(githubGraphQlService, "githubGraphqlUrl", getRemoteApiUrl());
    }

    @AfterEach
    public void teardownGithubGraphQlService() {
        GithubGraphQlService githubGraphQlService = serviceProvider.getGithubGraphQlService();
        ReflectionTestUtils.setField(githubGraphQlService, "githubGraphqlUrl", githubUrlSave);
    }

    public String loadGithubResponseFile(String filename) throws IOException {
        return FileUtilities.readClasspathFile("mock/github/" + filename);
    }
}
