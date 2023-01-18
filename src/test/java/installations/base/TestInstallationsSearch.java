package installations.base;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.installations.app.InstallationDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraProject;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import common.ApplicationBaseTest;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

/**
 * Given a Safa project test all external installations are correctly retrieved
 */
public class TestInstallationsSearch extends ApplicationBaseTest {

    private static final String PROJECT_NAME = "test-project";

    @Test
    public void allInstallationsForProjectAreLoaded() {
        Project project = dbEntityBuilder.newProject(PROJECT_NAME).getProject(PROJECT_NAME);
        JiraProject jiraProject = this.createJiraProject(UUID.randomUUID(), 10002L, project);
        GithubProject githubProject = this.createGithubProject("repository", "branch", project);
        List<InstallationDTO> installationDTOList = this.serviceProvider
            .getProjectRepository()
            .findInstallationsByProjectId(project.getProjectId());

        Assertions.assertEquals(2, installationDTOList.size());
    }

    private JiraProject createJiraProject(UUID orgId, Long id, Project project) {
        JiraProject jiraProject = new JiraProject();
        jiraProject.setOrgId(orgId);
        jiraProject.setJiraProjectId(id);
        jiraProject.setProject(project);
        return this.serviceProvider.getJiraProjectRepository().save(jiraProject);
    }

    private GithubProject createGithubProject(String repository, String branch, Project project) {
        GithubProject githubProject = new GithubProject();

        githubProject.setRepositoryName(repository);
        githubProject.setProject(project);
        githubProject.setBranch(branch);
        return this.serviceProvider.getGithubProjectRepository().save(githubProject);
    }
}
