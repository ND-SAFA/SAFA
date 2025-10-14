package edu.nd.crc.safa.features.users.entities.app;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@Data
public class CreateAccountRequest extends UserAppEntity {
    /**
     * User password to create account with.
     */
    private String password;
}
