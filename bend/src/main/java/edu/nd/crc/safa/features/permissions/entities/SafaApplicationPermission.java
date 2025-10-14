package edu.nd.crc.safa.features.permissions.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum SafaApplicationPermission implements SimplePermission {
    SUPERUSER("safa.superuser"),
    SUPERUSER_ACTIVATION("safa.active_superuser");

    private final String name;
}
