package edu.nd.crc.safa.features.users.entities.app;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Responsible for storing user password (encoded or decoded).
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserPasswordDTO {
    private String password;
}
