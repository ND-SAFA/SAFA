package edu.nd.crc.safa.features.users.entities.app;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

/**
 * POJO describing data required for a user to change their password while logged in
 */
@Getter
@Setter
public class PasswordChangeRequest {

    @NotNull
    @NotEmpty
    private String oldPassword;

    @NotNull
    @NotEmpty
    private String newPassword;
}
