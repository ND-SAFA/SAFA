package edu.nd.crc.safa.features.users.entities.app;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import lombok.Getter;
import lombok.Setter;

/**
 * POJO describing data required for a user to change their password while logged in
 */
@Getter
@Setter
public class PasswordChangeDTO {

    @NotNull
    @NotEmpty
    private String oldPassword;

    @NotNull
    @NotEmpty
    private String newPassword;
}
