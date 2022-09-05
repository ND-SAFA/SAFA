package edu.nd.crc.safa.features.users.entities.app;

import lombok.Data;

/**
 * Represents a request to resetting a user password.
 */
@Data
public class ResetPasswordRequestDTO {
    /**
     * The token sent to authorized email for resetting account password.
     */
    String resetToken;
    /**
     * The new password to set the account to.
     */
    String newPassword;
}
