package edu.nd.crc.safa.features.projects.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.installations.InstallationDTO;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface ProjectRepository extends CrudRepository<Project, UUID> {

    Project findByProjectId(UUID projectId);

    List<Project> findByOwningTeam(Team owningTeam);

    @Query(value =
        "SELECT new edu.nd.crc.safa.features.installations.InstallationDTO("
            + "  CAST(j.jiraProjectId AS string), "
            + "   j.orgId, "
            + "   j.lastUpdate, "
            + "   'JIRA') "
            + "FROM Project p "
            + "JOIN FETCH JiraProject j "
            + "     ON j.project.id = p.id "
            + "WHERE p.id= :projectId"
    )
    List<InstallationDTO> findJiraInstallationsByProjectId(@Param("projectId") UUID projectId);

    @Query(value =
        "SELECT new edu.nd.crc.safa.features.installations.InstallationDTO("
            + "  g.repositoryName, "
            + "   g.owner,"
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
}
