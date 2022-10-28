package edu.nd.crc.safa.features.users.entities.app;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class PasswordForgottenRequest {

    /**
     * User's email
     */
    @NotNull
    @NotEmpty
    String email;
}
