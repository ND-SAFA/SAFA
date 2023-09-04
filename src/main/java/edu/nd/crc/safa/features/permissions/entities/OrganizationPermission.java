package edu.nd.crc.safa.features.permissions.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public enum OrganizationPermission implements Permission {
    VIEW("org.view"),
    VIEW_BILLING("org.view_billing"),
    EDIT("org.edit"),
    DELETE("org.delete"),
    VIEW_TEAMS("org.view_teams"),
    CREATE_TEAMS("org.create_teams"),
    DELETE_TEAMS("org.delete_teams");

    @Getter
    private final String name;
}
