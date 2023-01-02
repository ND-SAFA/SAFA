package edu.nd.crc.safa.features.projects.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.installations.app.InstallationDTO;
import edu.nd.crc.safa.features.installations.app.ProjectWithInstallationDTO;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectRepository extends CrudRepository<Project, UUID> {

    Project findByProjectId(UUID projectId);

    @Query(value =
        "SELECT new edu.nd.crc.safa.features.installations.app.InstallationDTO("
            + "  CAST(j.jiraProjectId AS string), "
            + "   j.lastUpdate, "
            + "   'JIRA') "
            + "FROM Project p "
            + "JOIN FETCH JiraProject j "
            + "     ON j.project.id = p.id "
            + "WHERE p.id= :projectId"
    )
    List<InstallationDTO> findJiraInstallationsByProjectId(@Param("projectId") UUID projectId);

    @Query(value =
        "SELECT new edu.nd.crc.safa.features.installations.app.InstallationDTO("
            + "  g.repositoryName, "
            + "   g.lastUpdate, "
            + "   'GITHUB') "
            + "FROM Project p "
            + "JOIN FETCH GithubProject g "
            + "     ON g.project.id = p.id "
            + "WHERE p.id = :projectId"
    )
    List<InstallationDTO> findGithubInstallationsByProjectId(@Param("projectId") UUID projectId);

    default List<InstallationDTO> findInstallationsByProjectId(UUID projectId) {
        // This could be one UNION query, but unfortunately those are not possible in JPQL
        List<InstallationDTO> lo = this.findJiraInstallationsByProjectId(projectId);
        List<InstallationDTO> hi = this.findGithubInstallationsByProjectId(projectId);

        lo.addAll(hi);
        return lo;
    }

    /**
     * Given a list of JIRA project identifiers find all SAFA projects that have imported
     * them
     *
     * @param projects List of JIRA identifiers
     * @return list of projects that imported specified JIRA identifiers
     */
    @Query(value =
        "SELECT new edu.nd.crc.safa.features.installations.app.ProjectWithInstallationDTO("
            + "     p.id, "
            + "     p.name, "
            + "     CAST(j.jiraProjectId as string), "
            + "     j.lastUpdate, "
            + "    'JIRA')"
            + "FROM Project p "
            + "JOIN FETCH JiraProject j "
            + "ON j.project.id = p.id "
            + "WHERE j.jiraProjectId IN :projects"
    )
    List<ProjectWithInstallationDTO> findAllThatImportedGivenJIRAProjects(@Param("projects") List<Long> projects);

    /**
     * Given a list of GitHub repository names find all SAFA projects that have imported
     * them
     *
     * @param projects List of GitHub repository names
     * @return list of projects that imported specified GitHub repository names
     */
    @Query(value = "SELECT new edu.nd.crc.safa.features.installations.app.ProjectWithInstallationDTO("
        + "     p.id, "
        + "     p.name, "
        + "     g.repositoryName, "
        + "     g.lastUpdate, "
        + "    'GITHUB') "
        + "FROM Project p "
        + "JOIN FETCH GithubProject g "
        + "ON g.project.id = p.id "
        + "WHERE g.repositoryName IN :projects"
    )
    List<ProjectWithInstallationDTO> findAllThatImportedGivenGithubProjects(@Param("projects") List<String> projects);
}
