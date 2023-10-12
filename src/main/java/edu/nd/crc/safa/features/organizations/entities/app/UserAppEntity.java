package edu.nd.crc.safa.features.organizations.entities.app;

import java.util.UUID;

import lombok.Data;

@Data
public class UserAppEntity {
    private UUID id;
    private String email;
    private UUID personalOrgId;
    private UUID defaultOrgId;
    private boolean superuser;
}
