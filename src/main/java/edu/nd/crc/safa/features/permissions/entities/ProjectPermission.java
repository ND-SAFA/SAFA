package edu.nd.crc.safa.features.permissions.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum ProjectPermission implements SimplePermission {
    DELETE("project.delete"),
    EDIT("project.edit"),
    EDIT_DATA("project.edit_data"),
    EDIT_INTEGRATIONS("project.edit_integrations"),
    EDIT_MEMBERS("project.edit_members"),
    EDIT_VERSIONS("project.edit_versions"),
    GENERATE("project.generate"),
    MOVE("project.move"),
    VIEW("project.view");

    private final String name;
}
