package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.Set;

import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum TeamRole implements IRole {
    NONE(Set.of()),
    VIEWER(Set.of(
        ProjectPermission.VIEW, TeamPermission.VIEW, TeamPermission.VIEW_PROJECTS
    )),
    EDITOR(Set.of(
        ProjectPermission.VIEW, ProjectPermission.EDIT, TeamPermission.VIEW, TeamPermission.VIEW_PROJECTS,
        ProjectPermission.EDIT_DATA, ProjectPermission.EDIT_INTEGRATIONS, ProjectPermission.EDIT_VERSIONS
    )),
    ADMIN(Set.of(
        ProjectPermission.VIEW, ProjectPermission.EDIT, ProjectPermission.EDIT_MEMBERS, ProjectPermission.DELETE,
        TeamPermission.VIEW, TeamPermission.EDIT, TeamPermission.EDIT_MEMBERS, TeamPermission.DELETE,
        TeamPermission.VIEW_PROJECTS, TeamPermission.CREATE_PROJECTS, TeamPermission.DELETE_PROJECTS,
        ProjectPermission.EDIT_DATA, ProjectPermission.EDIT_INTEGRATIONS, ProjectPermission.EDIT_VERSIONS,
        ProjectPermission.GENERATE, ProjectPermission.MOVE
    )),
    GENERATOR(Set.of(
        ProjectPermission.GENERATE, ProjectPermission.VIEW, ProjectPermission.EDIT, ProjectPermission.EDIT_DATA,
        TeamPermission.VIEW, TeamPermission.VIEW_PROJECTS
    ));

    private final Set<Permission> grants;
}
