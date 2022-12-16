package features.github.imports;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import features.github.base.AbstractGithubTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import requests.SafaRequest;

public class TestGithubImport extends AbstractGithubTest {

    protected String repositoryName = "home_assistant_ro";

    @Test
    void intoNewProjectTest() throws Exception {
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
                .filesOnly().getTree().size(),
            serviceProvider.getArtifactRepository()
                .findByProject(githubProject.getProject()).size()
        );
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
            .withVersion(projectVersion)
            .postWithoutBody(status().is2xxSuccessful());

        // No other project was created during the import
        Assertions.assertEquals(1, serviceProvider.getProjectRepository().count());

        // We should have one GitHub project created
        Assertions.assertEquals(1, serviceProvider.getGithubProjectRepository().count());

        Assertions.assertTrue(serviceProvider.getGithubProjectRepository()
            .findByProjectAndRepositoryName(project, repositoryName).isPresent());

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

            if (artifactVersion.isPresent() && artifactVersion.get().getContent().equals(AbstractGithubTest.DECODED_FILE_CONTENT)) {
                correctBodyFound = true;
                Assertions.assertEquals("GitHub File", artifact.getType().getName());
            }
        }
        Assertions.assertTrue(correctBodyFound);

        Assertions.assertEquals(0,
            serviceProvider.getTraceLinkRepository().count());
    }
}
