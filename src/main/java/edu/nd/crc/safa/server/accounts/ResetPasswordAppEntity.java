package edu.nd.crc.safa.server.accounts;

import lombok.Data;

/**
 * Represents a request to reset a user password
 */
@Data
public class ResetPasswordAppEntity {
    String resetToken;
    String newPassword;
}
