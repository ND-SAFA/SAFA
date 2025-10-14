package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.Set;

import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum ProjectRole implements IRole {
    NONE(Set.of()),
    VIEWER(Set.of(
        ProjectPermission.VIEW
    )),
    EDITOR(Set.of(
        ProjectPermission.VIEW, ProjectPermission.EDIT, ProjectPermission.EDIT_DATA
    )),
    ADMIN(Set.of(
        ProjectPermission.VIEW, ProjectPermission.EDIT, ProjectPermission.EDIT_MEMBERS, ProjectPermission.EDIT_DATA,
        ProjectPermission.EDIT_INTEGRATIONS, ProjectPermission.EDIT_VERSIONS, ProjectPermission.GENERATE,
        ProjectPermission.MOVE
    )),
    OWNER(Set.of(
        ProjectPermission.VIEW, ProjectPermission.EDIT, ProjectPermission.EDIT_MEMBERS, ProjectPermission.EDIT_DATA,
        ProjectPermission.EDIT_INTEGRATIONS, ProjectPermission.EDIT_VERSIONS, ProjectPermission.GENERATE,
        ProjectPermission.DELETE, ProjectPermission.MOVE
    )),
    GENERATOR(Set.of(
        ProjectPermission.VIEW, ProjectPermission.EDIT, ProjectPermission.EDIT_DATA, ProjectPermission.GENERATE
    ));

    private final Set<Permission> grants;
}
