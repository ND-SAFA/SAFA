package edu.nd.crc.safa.features.users.entities.app;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents a request to resetting a user password.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ResetPasswordRequestDTO {
    /**
     * The token sent to authorized email for resetting account password.
     */
    @NotNull
    @NotEmpty
    private String resetToken;

    /**
     * The new password to set the account to.
     */
    @NotNull
    @NotEmpty
    private String newPassword;
}
