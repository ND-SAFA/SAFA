package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.Set;

import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public enum TeamRole {
    NONE(Set.of()),
    VIEWER(Set.of(ProjectPermission.VIEW,
                  TeamPermission.VIEW, TeamPermission.VIEW_PROJECTS)),
    EDITOR(Set.of(ProjectPermission.VIEW, ProjectPermission.EDIT,
                  TeamPermission.VIEW, TeamPermission.VIEW_PROJECTS)),
    ADMIN(Set.of(ProjectPermission.VIEW, ProjectPermission.EDIT, ProjectPermission.SHARE, ProjectPermission.DELETE,
                 TeamPermission.VIEW, TeamPermission.EDIT, TeamPermission.EDIT_MEMBERS, TeamPermission.DELETE,
                 TeamPermission.VIEW_PROJECTS, TeamPermission.CREATE_PROJECTS, TeamPermission.DELETE_PROJECTS)),

    GENERATOR(Set.of(ProjectPermission.GENERATE));

    @Getter
    private final Set<Permission> grants;
}
