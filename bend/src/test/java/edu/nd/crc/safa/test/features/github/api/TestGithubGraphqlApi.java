package edu.nd.crc.safa.test.features.github.api;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.github.entities.app.GithubRepositoryDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.test.features.github.base.AbstractGithubGraphqlTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import okhttp3.mockwebserver.RecordedRequest;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpHeaders;

public class TestGithubGraphqlApi extends AbstractGithubGraphqlTest {

    private final String accessToken = "testAccessToken";

    @BeforeEach
    public void setup() {
        GithubAccessCredentials credentials = new GithubAccessCredentials();
        credentials.setUser(getCurrentUser());
        credentials.setAccessToken(accessToken);
        serviceProvider.getGithubAccessCredentialsRepository().save(credentials);
    }

    @AfterEach
    public void teardown() {
        serviceProvider.getGithubAccessCredentialsRepository().deleteAll();
    }

    @Test
    void testGetRepositories() throws Exception {
        enqueueResponse("repositories_response.json");
        enqueueResponse("repositories_continued.json");
        enqueueResponse("branches_continued.json");

        List<GithubRepositoryDTO> response = SafaRequest
            .withRoute(AppRoutes.Integrations.Github.Repos.ROOT)
            .getAsType(new TypeReference<>() {
            });

        RecordedRequest recordedRequest = getServer().takeRequest();

        assertEquals("POST", recordedRequest.getMethod());
        assertEquals("token " + accessToken, recordedRequest.getHeader(HttpHeaders.AUTHORIZATION));

        assertEquals(2, response.size());

        GithubRepositoryDTO bend = response.get(0);
        assertEquals("ND-SAFA", bend.getOwner());
        assertEquals("bend", bend.getName());
        List<String> bendBranches = bend.getBranches();
        assertEquals(3, bendBranches.size());
        assertEquals("development", bendBranches.get(0));
        assertEquals("production", bendBranches.get(1));
        assertEquals("branch3", bendBranches.get(2));
        assertEquals("development", bend.getDefaultBranch());

        GithubRepositoryDTO fend = response.get(1);
        assertEquals("ND-SAFA", fend.getOwner());
        assertEquals("fend", fend.getName());
        List<String> fendBranches = fend.getBranches();
        assertEquals(3, fendBranches.size());
        assertEquals("FEAT-aws-integration", fendBranches.get(0));
        assertEquals("development", fendBranches.get(1));
        assertEquals("production", fendBranches.get(2));
        assertNull(fend.getDefaultBranch());
    }

    @Test
    void testGetRepository() throws Exception {
        enqueueResponse("repository_response.json");

        GithubRepositoryDTO response = SafaRequest
            .withRoute(AppRoutes.Integrations.Github.Repos.BY_OWNER_AND_NAME)
            .withOwner("owner")
            .withRepositoryName("name")
            .getAsType(new TypeReference<>() {
            });

        RecordedRequest recordedRequest = getServer().takeRequest();

        assertEquals("POST", recordedRequest.getMethod());
        assertEquals("token " + accessToken, recordedRequest.getHeader(HttpHeaders.AUTHORIZATION));

        assertEquals("ND-SAFA", response.getOwner());
        assertEquals("bend", response.getName());
        List<String> bendBranches = response.getBranches();
        assertEquals(6, bendBranches.size());
        assertEquals("FEATURE/aws-integration", bendBranches.get(0));
        assertEquals("FEATURE/github-import-updates", bendBranches.get(1));
        assertEquals("FEATURE-improve-db", bendBranches.get(2));
        assertEquals("REFACTOR/update-tgen", bendBranches.get(3));
        assertEquals("development", bendBranches.get(4));
        assertEquals("production", bendBranches.get(5));
    }
}
