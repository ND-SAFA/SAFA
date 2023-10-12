package edu.nd.crc.safa.features.permissions.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public enum ProjectPermission implements Permission {
    DELETE("project.delete"),
    EDIT("project.edit"),
    EDIT_DATA("project.edit_data"),
    EDIT_INTEGRATIONS("project.edit_integrations"),
    EDIT_MEMBERS("project.edit_members"),
    EDIT_VERSIONS("project.edit_versions"),
    GENERATE("project.generate"),
    VIEW("project.view");

    @Getter
    private final String name;
}
