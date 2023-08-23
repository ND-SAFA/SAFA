package edu.nd.crc.safa.features.memberships.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.TeamMembership;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;

public interface TeamMembershipRepository extends CrudRepository<TeamMembership, UUID> {
    List<TeamMembership> findByUserAndTeam(SafaUser user, Team team);

    Optional<TeamMembership> findByUserAndTeamAndRole(SafaUser user, Team team, TeamRole role);

    List<TeamMembership> findByUser(SafaUser user);

    List<TeamMembership> findByTeam(Team team);
}
