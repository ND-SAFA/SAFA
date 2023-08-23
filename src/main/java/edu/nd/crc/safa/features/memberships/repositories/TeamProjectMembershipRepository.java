package edu.nd.crc.safa.features.memberships.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.TeamProjectMembership;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TeamProjectMembershipRepository extends CrudRepository<TeamProjectMembership, UUID> {
    Optional<TeamProjectMembership> findByTeamAndProject(Team team, Project project);
}
