package installations.base;

import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.LongStream;

import common.ApplicationBaseTest;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.installations.app.InstallationDTO;
import edu.nd.crc.safa.features.installations.app.InstallationTypeEnum;
import edu.nd.crc.safa.features.installations.app.ProjectWithInstallationDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraProject;
import edu.nd.crc.safa.features.projects.entities.db.Project;
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
        JiraProject jiraProject = this.createJiraProject(10002L, project);
        GithubProject githubProject = this.createGithubProject("repository", "branch", project);
        List<InstallationDTO> installationDTOList = this.serviceProvider
            .getProjectRepository()
            .findInstallationsByProjectId(project.getProjectId());

        Assertions.assertEquals(2, installationDTOList.size());
    }

    @Test
    public void allProjectsThatImportedGivenInstallationsAreRetrieved() {
        Project project = dbEntityBuilder.newProject(PROJECT_NAME).getProject(PROJECT_NAME);
        List<Long> jiraIds = LongStream.range(10000L, 10005L).boxed().collect(Collectors.toList());
        List<String> repos = List.of("MetaHeuristics", "Home-Assistant", "Term-Rewriting");

        jiraIds.subList(1, 5).forEach(id -> createJiraProject(id, project));
        repos.subList(0, 2).forEach(name -> createGithubProject(name, "branch", project));

        List<ProjectWithInstallationDTO> jiraProjects = this.serviceProvider
            .getProjectRepository()
            .findAllThatImportedGivenJIRAProjects(jiraIds);
        List<ProjectWithInstallationDTO> githubProjects = this.serviceProvider
            .getProjectRepository()
            .findAllThatImportedGivenGithubProjects(repos);

        Assertions.assertTrue(jiraProjects
            .stream()
            .map(ProjectWithInstallationDTO::getType)
            .allMatch(InstallationTypeEnum.JIRA::equals));

        Assertions.assertTrue(githubProjects
            .stream()
            .map(ProjectWithInstallationDTO::getType)
            .allMatch(InstallationTypeEnum.GITHUB::equals));

        Assertions.assertEquals(4, jiraProjects.size());
        Assertions.assertEquals(2, githubProjects.size());
    }

    private JiraProject createJiraProject(Long id, Project project) {
        JiraProject jiraProject = new JiraProject();

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
