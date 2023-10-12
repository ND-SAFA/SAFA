package edu.nd.crc.safa.features.permissions.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public enum TeamPermission implements Permission {
    CREATE_PROJECTS("team.create_projects"),
    DELETE("team.delete"),
    DELETE_PROJECTS("team.delete_projects"),
    EDIT("team.edit"),
    EDIT_MEMBERS("team.edit_members"),
    VIEW("team.view"),
    VIEW_PROJECTS("team.view_projects");

    @Getter
    private final String name;
}
