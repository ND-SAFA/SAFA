package edu.nd.crc.safa.test.features.github.imports;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.github.base.AbstractGithubTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class TestGithubImport extends AbstractGithubTest {

    protected String repositoryName = "bend";
    protected String owner = "ND-SAFA";

    @Test
    void intoNewProjectTest() throws Exception {
        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Import.BY_NAME)
            .withRepositoryName(repositoryName)
            .withOwner(owner)
            .postWithJsonObject(new GithubImportDTO(), status().is2xxSuccessful());

        // We should have one version created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        GithubProject githubProject = serviceProvider.getGithubProjectRepository().findAll().get(0);

        List<Artifact> importedFiles = serviceProvider.getArtifactRepository()
            .findByProject(githubProject.getProject());

        // We should have the corespondent project and user set
        Assertions.assertNotNull(githubProject.getProject());
        // We should have as many artifacts as the number of files produced by the mock service
        Assertions.assertEquals(
            serviceMock.getRepositoryFiles(credentials, repositoryName, "sha")
                .filesOnly().getTree().size(),
            importedFiles.size()
        );

        // These assertions are just to contrast the ones in the next test
        Assertions.assertTrue(importedFiles.stream().anyMatch(artifact -> !artifact.getName().endsWith(".pl")));
        Assertions.assertTrue(importedFiles.stream().anyMatch(artifact ->
            artifact.getName().startsWith("modules/weather/")));
        Assertions.assertTrue(importedFiles.stream().allMatch(artifact ->
            artifact.getType().getName().equals("GitHub File")));
    }

    @Test
    void intoNewProjectWithImportSettingsTest() throws Exception {
        String typeName = "test github artifact type";
        GithubImportDTO importSettings = new GithubImportDTO();
        importSettings.setInclude(List.of("**/*.pl"));
        importSettings.setExclude(List.of("modules/weather/**"));
        importSettings.setArtifactType(typeName);

        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Import.BY_NAME)
            .withRepositoryName(repositoryName)
            .withOwner(owner)
            .postWithJsonObject(importSettings, status().is2xxSuccessful());

        // We should have one version created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        GithubProject githubProject = serviceProvider.getGithubProjectRepository().findAll().get(0);

        List<Artifact> importedFiles = serviceProvider.getArtifactRepository()
            .findByProject(githubProject.getProject());

        // We should have the corespondent project and user set
        Assertions.assertNotNull(githubProject.getProject());
        Assertions.assertEquals(7, importedFiles.size());

        for (Artifact artifact : importedFiles) {
            Assertions.assertEquals(typeName, artifact.getType().getName());
            Assertions.assertTrue(artifact.getName().endsWith(".pl"));
            Assertions.assertFalse(artifact.getName().startsWith("modules/weather/"));
        }
    }

    @Test
    void intoExistingProjectTest() throws Exception {
        String projectName = "githubImport";
        int initialArtifactCount = 5;

        this.createBaseSafaProject(projectName, initialArtifactCount);

        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        Project project = dbEntityBuilder.getProject(projectName);

        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Import.IMPORT_INTO_EXISTING)
            .withRepositoryName(repositoryName)
            .withOwner(githubLogin)
            .withVersion(projectVersion)
            .postWithJsonObject(new GithubImportDTO(), status().is2xxSuccessful());

        // No other project was created during the import
        Assertions.assertEquals(1, serviceProvider.getProjectRepository().count());

        // We should have one GitHub project created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        Assertions.assertTrue(serviceProvider.getGithubProjectRepository()
            .findByProjectAndOwnerAndRepositoryName(project, owner, repositoryName).isPresent());

        int importedArtifactsCount = serviceMock.getRepositoryFiles(credentials, repositoryName, "sha")
            .filesOnly().getTree().size();

        // We should have the correct number of artifacts and links
        List<Artifact> artifacts = serviceProvider.getArtifactRepository()
            .findByProject(project);
        Assertions.assertEquals(
            importedArtifactsCount + initialArtifactCount,
            artifacts.size());

        // Since some artifacts existed beforehand, we'll just check that *some* artifact has the right body
        // And while we're at it, we'll check the artifact type
        boolean correctBodyFound = false;
        for (Artifact artifact : artifacts) {
            Optional<ArtifactVersion> artifactVersion
                = serviceProvider.getArtifactVersionRepository().findByProjectVersionAndArtifact(projectVersion, artifact);

            if (artifactVersion.isPresent()
                && artifactVersion.get().getContent().equals(AbstractGithubTest.DECODED_FILE_CONTENT)) {

                correctBodyFound = true;
                Assertions.assertEquals("GitHub File", artifact.getType().getName());
            }
        }
        Assertions.assertTrue(correctBodyFound);

        Assertions.assertEquals(0,
            serviceProvider.getTraceLinkRepository().count());
    }

    @Test
    void intoExistingProjectWithImportSettingsTest() throws Exception {
        String typeName = "test github artifact type";
        GithubImportDTO importSettings = new GithubImportDTO();
        importSettings.setInclude(List.of("**/*.pl"));
        importSettings.setExclude(List.of("modules/weather/**"));
        importSettings.setArtifactType(typeName);

        String projectName = "githubImport";
        int initialArtifactCount = 5;

        this.createBaseSafaProject(projectName, initialArtifactCount);

        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        Project project = dbEntityBuilder.getProject(projectName);

        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Github.Import.IMPORT_INTO_EXISTING)
            .withRepositoryName(repositoryName)
            .withOwner(githubLogin)
            .withVersion(projectVersion)
            .postWithJsonObject(importSettings, status().is2xxSuccessful());

        // No other project was created during the import
        Assertions.assertEquals(1, serviceProvider.getProjectRepository().count());

        // We should have one GitHub project created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        Assertions.assertTrue(serviceProvider.getGithubProjectRepository()
            .findByProjectAndOwnerAndRepositoryName(project, owner, repositoryName).isPresent());

        int importedArtifactsCount = 7;

        // We should have the correct number of artifacts and links
        List<Artifact> artifacts = serviceProvider.getArtifactRepository().findByProject(project);
        Assertions.assertEquals(importedArtifactsCount + initialArtifactCount, artifacts.size());

        // Since some artifacts existed beforehand, we'll just check that *some* artifact has the right body
        // And while we're at it, we'll check the artifact type
        boolean correctBodyFound = false;
        for (Artifact artifact : artifacts) {
            Optional<ArtifactVersion> artifactVersion
                = serviceProvider.getArtifactVersionRepository().findByProjectVersionAndArtifact(projectVersion, artifact);

            if (artifact.getType().getName().equals(typeName)) {
                importedArtifactsCount--;
                Assertions.assertTrue(artifact.getName().endsWith(".pl"));
                Assertions.assertFalse(artifact.getName().startsWith("modules/weather/"));
            }

            if (artifactVersion.isPresent()
                && artifactVersion.get().getContent().equals(AbstractGithubTest.DECODED_FILE_CONTENT)) {

                correctBodyFound = true;
                Assertions.assertEquals(typeName, artifact.getType().getName());
            }
        }
        Assertions.assertTrue(correctBodyFound);
        Assertions.assertEquals(0, importedArtifactsCount);

        Assertions.assertEquals(0,
            serviceProvider.getTraceLinkRepository().count());
    }
}
