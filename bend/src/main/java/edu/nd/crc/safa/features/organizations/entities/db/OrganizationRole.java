package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.Set;

import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum OrganizationRole implements IRole {
    NONE(Set.of()),
    MEMBER(Set.of(
        OrganizationPermission.VIEW, OrganizationPermission.VIEW_TEAMS
    )),
    BILLING_MANAGER(Set.of(
        OrganizationPermission.VIEW_BILLING, OrganizationPermission.VIEW
    )),
    ADMIN(Set.of(
        OrganizationPermission.VIEW, OrganizationPermission.VIEW_BILLING, OrganizationPermission.EDIT,
        OrganizationPermission.VIEW_TEAMS, OrganizationPermission.CREATE_TEAMS, OrganizationPermission.DELETE_TEAMS,
        TeamPermission.EDIT_MEMBERS, OrganizationPermission.EDIT_MEMBERS
    )),
    GENERATOR(Set.of(
        ProjectPermission.GENERATE, OrganizationPermission.VIEW, OrganizationPermission.VIEW_TEAMS
    ));

    private final Set<Permission> grants;
}
