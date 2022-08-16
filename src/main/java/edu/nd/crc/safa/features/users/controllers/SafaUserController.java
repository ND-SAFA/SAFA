package edu.nd.crc.safa.features.users.controllers;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.app.UserPassword;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller containing endpoints for:
 * 1. Creating a new account
 * 2. Resetting user password (TODO)
 * 3. Confirming user account (TODO)
 * Note, logging into system is handled by spring boot default configuration at /login.
 */
@RestController
public class SafaUserController extends BaseController {

    @Autowired
    public SafaUserController(ResourceBuilder resourceBuilder,
                              ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Creates new account with given email and password.
     * Error is thrown is email is already associated with another account.
     *
     * @param newUser User to create containing email and password.
     * @return Created user entity
     */
    @PostMapping(AppRoutes.Accounts.CREATE_ACCOUNT)
    public UserAppEntity createNewUser(@RequestBody SafaUser newUser) {
        return this.serviceProvider
            .getSafaUserService()
            .createUser(newUser.getEmail(), newUser.getPassword());
    }

    /**
     * Deletes account of authenticated user after confirming that given
     * password matches that of database.
     *
     * @param userPassword Authenticated user's password.
     */
    @PostMapping(AppRoutes.Accounts.DELETE_ACCOUNT)
    public void deleteAccount(@RequestBody UserPassword userPassword) {
        String confirmationPassword = userPassword.getPassword();
        if (confirmationPassword == null) {
            throw new SafaError("Received empty confirmation password.");
        }
        this.serviceProvider
            .getSafaUserService()
            .deleteUser(confirmationPassword);
    }
}
