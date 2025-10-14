package edu.nd.crc.safa.test.features.github.imports;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.IOException;
import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.attributes.ReservedAttributes;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubAccessCredentials;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.github.base.AbstractGithubGraphqlTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.requests.CommonProjectRequests;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestGithubImport extends AbstractGithubGraphqlTest {

    protected String repositoryName = "bend";
    protected String owner = "ND-SAFA";

    @BeforeEach
    public void setup() {
        GithubAccessCredentials credentials = new GithubAccessCredentials();
        credentials.setUser(getCurrentUser());
        String accessToken = "testAccessToken";
        credentials.setAccessToken(accessToken);
        serviceProvider.getGithubAccessCredentialsRepository().save(credentials);
    }

    private void enqueueDefaultResponses() throws IOException {
        enqueueResponse("repository_response.json");
        enqueueResponse("filetree_response.json");
        enqueueResponse("filetree_response_src.json");
        enqueueResponse("filetree_response_include.json");
    }

    @Test
    void intoNewProjectTest() throws Exception {
        enqueueDefaultResponses();

        SafaRequest
            .withRoute(AppRoutes.Github.Import.BY_NAME)
            .withRepositoryName(repositoryName)
            .withOwner(owner)
            .postWithJsonObject(new GithubImportDTO(), status().is2xxSuccessful());

        // We should have one version created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        GithubProject githubProject = serviceProvider.getGithubProjectRepository().findAll().get(0);

        List<ArtifactAppEntity> importedFiles =
            serviceProvider.getArtifactService().getAppEntities(githubProject.getProject());

        // We should have the corespondent project and user set
        Assertions.assertNotNull(githubProject.getProject());
        // We should have as many artifacts as the number of files produced by the mock service
        Assertions.assertEquals(26, importedFiles.size());

        // These assertions are just to contrast the ones in the next test
        Assertions.assertTrue(importedFiles.stream().anyMatch(artifact -> !artifact.getName().endsWith(".cpp")));
        Assertions.assertTrue(importedFiles.stream().anyMatch(artifact -> artifact.getName().startsWith("include/")));
        Assertions.assertTrue(importedFiles.stream().allMatch(artifact ->
            artifact.getType().equals("GitHub File")));

        for (ArtifactAppEntity artifact : importedFiles) {
            if (artifact.getType().equals("GitHub File")) {
                ReservedAttributes.Github.ALL_ATTRIBUTES
                    .forEach(key -> Assertions.assertTrue(artifact.getAttributes().containsKey(key)));
            }
        }
        List<JobAppEntity> jobs = CommonProjectRequests.getProjectJobs(githubProject.getProject());
        Assertions.assertEquals(1, jobs.size());
    }


    @Test
    void intoNewProjectWithImportSettingsTest() throws Exception {
        enqueueDefaultResponses();

        String typeName = "test github artifact type";
        GithubImportDTO importSettings = new GithubImportDTO();
        importSettings.setInclude(List.of("**/*.{cpp,hpp}"));
        importSettings.setExclude(List.of("include/**"));
        importSettings.setArtifactType(typeName);

        SafaRequest
            .withRoute(AppRoutes.Github.Import.BY_NAME)
            .withRepositoryName(repositoryName)
            .withOwner(owner)
            .postWithJsonObject(importSettings, status().is2xxSuccessful());

        // We should have one version created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        GithubProject githubProject = serviceProvider.getGithubProjectRepository().findAll().get(0);

        List<ArtifactAppEntity> importedFiles =
            serviceProvider.getArtifactService().getAppEntities(githubProject.getProject());

        // We should have the corespondent project and user set
        Assertions.assertNotNull(githubProject.getProject());
        Assertions.assertEquals(7, importedFiles.size());

        for (ArtifactAppEntity artifact : importedFiles) {
            Assertions.assertEquals(typeName, artifact.getType());
            Assertions.assertTrue(artifact.getName().endsWith(".cpp"));
            Assertions.assertFalse(artifact.getName().startsWith("include/"));

            ReservedAttributes.Github.ALL_ATTRIBUTES
                .forEach(key -> Assertions.assertTrue(artifact.getAttributes().containsKey(key)));
        }
    }

    @Test
    void intoExistingProjectTest() throws Exception {
        enqueueDefaultResponses();

        String projectName = "githubImport";
        int initialArtifactCount = 5;

        this.createBaseSafaProject(projectName, initialArtifactCount);

        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        Project project = dbEntityBuilder.getProject(projectName);

        SafaRequest
            .withRoute(AppRoutes.Github.Import.IMPORT_INTO_EXISTING)
            .withRepositoryName(repositoryName)
            .withOwner(owner)
            .withVersion(projectVersion)
            .postWithJsonObject(new GithubImportDTO(), status().is2xxSuccessful());

        // No other project was created during the import
        Assertions.assertEquals(1, serviceProvider.getProjectRepository().count());

        // We should have one GitHub project created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        Assertions.assertTrue(serviceProvider.getGithubProjectRepository()
            .findByProjectAndOwnerAndRepositoryName(project, owner, repositoryName).isPresent());

        int importedArtifactsCount = 26;

        // We should have the correct number of artifacts and links
        List<ArtifactAppEntity> artifacts = serviceProvider.getArtifactService().getAppEntities(project);
        Assertions.assertEquals(
            importedArtifactsCount + initialArtifactCount,
            artifacts.size());

        for (ArtifactAppEntity artifact : artifacts) {
            if (artifact.getType().equals("GitHub File")) {
                ReservedAttributes.Github.ALL_ATTRIBUTES
                    .forEach(key -> Assertions.assertTrue(artifact.getAttributes().containsKey(key)));
            }
        }

        Assertions.assertEquals(0,
            serviceProvider.getTraceLinkRepository().count());
    }

    @Test
    void intoExistingProjectWithImportSettingsTest() throws Exception {
        enqueueDefaultResponses();

        String typeName = "test github artifact type";
        GithubImportDTO importSettings = new GithubImportDTO();
        importSettings.setInclude(List.of("**/*.{cpp,hpp}", ".gitignore", "src/filename_with_a_{comma\\,,brace\\{}",
            "**/another_filename_with_a_comma\\,"));
        importSettings.setExclude(List.of("include/**"));
        importSettings.setArtifactType(typeName);

        String projectName = "githubImport";
        int initialArtifactCount = 5;

        this.createBaseSafaProject(projectName, initialArtifactCount);

        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        Project project = dbEntityBuilder.getProject(projectName);

        SafaRequest
            .withRoute(AppRoutes.Github.Import.IMPORT_INTO_EXISTING)
            .withRepositoryName(repositoryName)
            .withOwner(owner)
            .withVersion(projectVersion)
            .postWithJsonObject(importSettings, status().is2xxSuccessful());

        // No other project was created during the import
        Assertions.assertEquals(1, serviceProvider.getProjectRepository().count());

        // We should have one GitHub project created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        Assertions.assertTrue(serviceProvider.getGithubProjectRepository()
            .findByProjectAndOwnerAndRepositoryName(project, owner, repositoryName).isPresent());

        int importedArtifactsCount = 11;

        // We should have the correct number of artifacts and links
        List<ArtifactAppEntity> artifacts = serviceProvider.getArtifactService().getAppEntities(project);
        Assertions.assertEquals(importedArtifactsCount + initialArtifactCount, artifacts.size());

        for (ArtifactAppEntity artifact : artifacts) {
            if (artifact.getType().equals(typeName)) {
                importedArtifactsCount--;
                Assertions.assertTrue(
                    artifact.getName().endsWith(".cpp")
                        || artifact.getName().equals(".gitignore")
                        || artifact.getName().equals("src/filename_with_a_comma,")
                        || artifact.getName().equals("src/filename_with_a_brace{")
                        || artifact.getName().equals("src/another_filename_with_a_comma,"),
                    () -> "Unexpected file:" + artifact.getName()
                );
                Assertions.assertFalse(artifact.getName().startsWith("include/"));

                ReservedAttributes.Github.ALL_ATTRIBUTES
                    .forEach(key -> Assertions.assertTrue(artifact.getAttributes().containsKey(key)));
            }
        }
        Assertions.assertEquals(0, importedArtifactsCount);

        Assertions.assertEquals(0,
            serviceProvider.getTraceLinkRepository().count());
    }

    @Test
    void testNoDefaultBranch() throws Exception {
        enqueueResponse("repository_response_no_default_branch.json");
        enqueueResponse("filetree_response.json");
        enqueueResponse("filetree_response_src.json");
        enqueueResponse("filetree_response_include.json");

        SafaRequest
            .withRoute(AppRoutes.Github.Import.BY_NAME)
            .withRepositoryName(repositoryName)
            .withOwner(owner)
            .postWithJsonObject(new GithubImportDTO(), status().is2xxSuccessful());

        // We should have one version created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        GithubProject githubProject = serviceProvider.getGithubProjectRepository().findAll().get(0);

        List<ArtifactAppEntity> importedFiles =
            serviceProvider.getArtifactService().getAppEntities(githubProject.getProject());

        // We should have the corespondent project and user set
        Assertions.assertNotNull(githubProject.getProject());
        // We should have as many artifacts as the number of files produced by the mock service
        Assertions.assertEquals(26, importedFiles.size());
    }
}
