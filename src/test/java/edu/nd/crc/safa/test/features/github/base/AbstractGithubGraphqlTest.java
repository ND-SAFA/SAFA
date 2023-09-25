package edu.nd.crc.safa.test.features.github.base;

import java.io.IOException;
import java.util.stream.IntStream;

import edu.nd.crc.safa.features.github.services.GithubGraphQlService;
import edu.nd.crc.safa.test.common.AbstractRemoteApiTest;
import edu.nd.crc.safa.test.server.SafaMockServer;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.test.util.ReflectionTestUtils;

public abstract class AbstractGithubGraphqlTest extends AbstractRemoteApiTest<SafaMockServer> {
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

    protected void createBaseSafaProject(String projectName, int initialArtifactCount) {
        String artifactTypeName = "requirement";

        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, artifactTypeName);

        IntStream.range(0, initialArtifactCount).mapToObj(String::valueOf).forEach(name ->
            dbEntityBuilder.newArtifactAndBody(projectName, artifactTypeName, name, "", ""));
    }

    protected void enqueueResponse(String name) throws IOException {
        getServer().setStringResponse(loadGithubResponseFile(name));
    }
}
