package edu.nd.crc.safa.features.users.entities.app;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents a request to resetting a user password.
 */
@Data
@NoArgsConstructor
public class ResetPasswordRequestDTO {
    /**
     * The token sent to authorized email for resetting account password.
     */
    @NotNull
    @NotEmpty
    String resetToken;

    /**
     * The new password to set the account to.
     */
    @NotNull
    @NotEmpty
    String newPassword;
}
