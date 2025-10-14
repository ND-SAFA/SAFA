package edu.nd.crc.safa.features.memberships.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.entities.db.TeamMembership;
import edu.nd.crc.safa.features.memberships.repositories.TeamMembershipRepository;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class TeamMembershipService implements IMembershipService {

    private final TeamMembershipRepository teamMembershipRepo;

    /**
     * {@inheritDoc}
     */
    @Override
    public TeamMembership addUserRole(SafaUser user, IEntityWithMembership entity, IRole iRole) {
        assert entity instanceof Team;
        assert iRole instanceof TeamRole;
        Team team = (Team) entity;
        TeamRole role = (TeamRole) iRole;

        Optional<TeamMembership> membershipOptional =
            teamMembershipRepo.findByUserAndTeamAndRole(user, team, role);

        return membershipOptional.orElseGet(() -> {
            TeamMembership newMembership = new TeamMembership(user, team, role);
            return teamMembershipRepo.save(newMembership);
        });
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void removeUserRole(SafaUser user, IEntityWithMembership entity, IRole iRole) {
        assert entity instanceof Team;
        assert iRole instanceof TeamRole;
        Team team = (Team) entity;
        TeamRole role = (TeamRole) iRole;

        Optional<TeamMembership> membershipOptional =
            teamMembershipRepo.findByUserAndTeamAndRole(user, team, role);

        membershipOptional.ifPresent(teamMembershipRepo::delete);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public List<IRole> getRolesForUser(SafaUser user, IEntityWithMembership entity) {
        assert entity instanceof Team;
        Team team = (Team) entity;

        return teamMembershipRepo.findByUserAndTeam(user, team).stream()
            .map(TeamMembership::getRole)
            .collect(Collectors.toUnmodifiableList());
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public List<IEntityMembership> getMembershipsForUser(SafaUser user) {
        // Remaking the list forces it to understand that the type is indeed correct
        return new ArrayList<>(teamMembershipRepo.findByUser(user));
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public List<IEntityMembership> getMembershipsForEntity(IEntityWithMembership entity) {
        assert entity instanceof Team;
        Team team = (Team) entity;
        // Remaking the list forces it to understand that the type is indeed correct
        return new ArrayList<>(teamMembershipRepo.findByTeam(team));
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public Optional<IEntityMembership> getMembershipOptionalById(UUID membershipId) {
        // The map call forces it to understand that the type is indeed correct
        return teamMembershipRepo.findById(membershipId).map(m -> m);
    }

    /**
     * Returns the team members of the project.
     *
     * @param project Project whose members are returned.
     * @return List of team members with access to the project.
     */
    public List<MembershipAppEntity> getProjectMemberships(Project project) {
        Team owningTeam = project.getOwningTeam();
        List<IEntityMembership> teamMembers = this.getMembershipsForEntity(owningTeam);
        return teamMembers
            .stream()
            .map(m -> {
                MembershipAppEntity membershipAppEntity = new MembershipAppEntity();
                membershipAppEntity.setEntityType(MembershipType.TEAM);
                membershipAppEntity.setEntityId(owningTeam.getId());
                membershipAppEntity.setEmail(m.getUser().getEmail());
                membershipAppEntity.setRole(m.getRole().name());
                return membershipAppEntity;
            }).collect(Collectors.toList());
    }
}
