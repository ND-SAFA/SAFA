package edu.nd.crc.safa.features.users.entities.app;

import lombok.Data;

/**
 * Represents a request to reset a user password
 */
@Data
public class ResetPasswordAppEntity {
    String resetToken;
    String newPassword;
}
