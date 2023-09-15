package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.Set;

import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public enum ProjectRole {
    NONE(Set.of()),
    VIEWER(Set.of(ProjectPermission.VIEW)),
    EDITOR(Set.of(ProjectPermission.VIEW, ProjectPermission.EDIT)),
    ADMIN(Set.of(ProjectPermission.VIEW, ProjectPermission.EDIT, ProjectPermission.SHARE)),
    OWNER(Set.of(ProjectPermission.VIEW, ProjectPermission.EDIT, ProjectPermission.SHARE, ProjectPermission.DELETE)),
    GENERATOR(Set.of(ProjectPermission.GENERATE));

    @Getter
    private final Set<Permission> grants;
}
