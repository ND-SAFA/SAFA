package edu.nd.crc.safa.features.users.controllers;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.admin.auditlog.services.AuditLogService;
import edu.nd.crc.safa.authentication.AuthorizationSetter;
import edu.nd.crc.safa.authentication.TokenService;
import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.email.services.EmailService;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.permissions.entities.SimplePermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.CreateAccountRequest;
import edu.nd.crc.safa.features.users.entities.app.PasswordChangeRequest;
import edu.nd.crc.safa.features.users.entities.app.PasswordForgottenRequest;
import edu.nd.crc.safa.features.users.entities.app.ResetPasswordRequestDTO;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.app.UserPasswordDTO;
import edu.nd.crc.safa.features.users.entities.db.PasswordResetToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.PasswordResetTokenRepository;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.users.services.EmailVerificationService;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.jsonwebtoken.Claims;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

/**
 * Controller containing endpoints for:
 * 1. Creating a new account
 * 2. Resetting user password
 * 3. Confirming user account
 * Note, logging into system is handled by spring boot default configuration at /login.
 */
@RestController
public class SafaUserController extends BaseController {

    private final TokenService tokenService;
    private final PasswordEncoder passwordEncoder;
    private final SafaUserRepository safaUserRepository;
    private final SafaUserService safaUserService;
    private final EmailService emailService;
    private final PermissionService permissionService;
    private final EmailVerificationService emailVerificationService;
    private final PasswordResetTokenRepository passwordResetTokenRepository;
    private final OrganizationService organizationService;
    private final AuditLogService auditLogService;

    @Value("${security.allow_new_accounts}")
    private boolean allowNewAccounts;

    @Autowired
    public SafaUserController(ResourceBuilder resourceBuilder,
                              ServiceProvider serviceProvider,
                              EmailService emailService,
                              PermissionService permissionService,
                              EmailVerificationService emailVerificationService,
                              PasswordResetTokenRepository passwordResetTokenRepository,
                              OrganizationService organizationService,
                              AuditLogService auditLogService) {
        super(resourceBuilder, serviceProvider);
        this.tokenService = serviceProvider.getTokenService();
        this.passwordEncoder = serviceProvider.getPasswordEncoder();
        this.safaUserRepository = serviceProvider.getSafaUserRepository();
        this.safaUserService = serviceProvider.getSafaUserService();
        this.emailService = emailService;
        this.permissionService = permissionService;
        this.emailVerificationService = emailVerificationService;
        this.passwordResetTokenRepository = passwordResetTokenRepository;
        this.organizationService = organizationService;
        this.auditLogService = auditLogService;
    }

    /**
     * Creates new account with given email and password.
     * Error is thrown is email is already associated with another account.
     *
     * @param newUser User to create containing email and password.
     * @return Created user entity
     */
    @PostMapping(AppRoutes.Accounts.CREATE_ACCOUNT)
    public UserAppEntity createNewUser(@RequestBody CreateAccountRequest newUser) {
        if (!allowNewAccounts) {
            throw new SafaError("Sign-ups are disabled. Please contact an admin.");
        }

        // Step - Create user
        SafaUser createdAccount = getServiceProvider()
            .getSafaUserService()
            .createUser(newUser.getEmail(), newUser.getPassword());

        emailVerificationService.sendVerificationEmail(createdAccount);

        return safaUserService.toAppEntity(createdAccount);
    }

    /**
     * <p>Creates new account with given email and password.
     * Error is thrown is email is already associated with another account.</p>
     *
     * <p>The created account will be automatically verified and will not send
     * a verification email.</p>
     *
     * <p>This action can only be done by a superuser</p>
     *
     * @param newUser User to create containing email and password.
     * @return Created user entity
     */
    @PostMapping(AppRoutes.Accounts.CREATE_VERIFIED_ACCOUNT)
    public UserAppEntity createNewVerifiedUser(@RequestBody CreateAccountRequest newUser) {
        SafaUser currentUser = getCurrentUser();
        if (!currentUser.isSuperuser()) {
            throw new MissingPermissionException((SimplePermission) () -> "safa.create_verified_account");
        }

        SafaUser createdAccount = safaUserService.createUser(newUser.getEmail(), newUser.getPassword());
        createdAccount = safaUserService.setAccountVerification(createdAccount, true);
        return safaUserService.toAppEntity(createdAccount);
    }

    /**
     * Verify a user's email from an email verification token
     *
     * @param token The email verification token
     */
    @PostMapping(AppRoutes.Accounts.VERIFY_ACCOUNT)
    public void verifyAccount(@RequestBody AccountVerificationDTO token) {
        emailVerificationService.verifyToken(token.getToken());
    }

    /**
     * Deletes account of authenticated user after confirming that given
     * password matches that of database.
     *
     * @param userPasswordDTO Authenticated user's password.
     */
    @PostMapping(AppRoutes.Accounts.DELETE_ACCOUNT)
    public void deleteAccount(@RequestBody UserPasswordDTO userPasswordDTO) {
        String confirmationPassword = userPasswordDTO.getPassword();
        if (confirmationPassword == null) {
            throw new SafaError("Received empty confirmation password.");
        }
        getServiceProvider()
            .getSafaUserService()
            .deleteUser(confirmationPassword);
    }

    /**
     * Sends email to authorized user email enabling them to create a new password.
     *
     * @param user The user to send the reset password email to.
     */
    @Transactional
    @PutMapping(AppRoutes.Accounts.FORGOT_PASSWORD)
    public void forgotPassword(@Valid @RequestBody PasswordForgottenRequest user) {
        forgotPassword(user.getEmail(), user.getEmail());
    }

    /**
     * Reset a password
     *
     * @param resetEmail The email of the account to reset
     * @param tokenEmail The email to send the token to (usually the same as the one being
     *                   reset unless an admin is doing it)
     */
    private void forgotPassword(String resetEmail, String tokenEmail) {
        SafaUser retrievedUser = safaUserRepository.findByEmail(resetEmail)
            .orElseThrow(() -> new UsernameNotFoundException("Username does not exist: " + resetEmail));
        Date expirationDate = new Date(System.currentTimeMillis() + SecurityConstants.FORGOT_PASSWORD_EXPIRATION_TIME);
        String token = tokenService.createTokenForUsername(resetEmail, expirationDate);
        PasswordResetToken passwordResetToken = new PasswordResetToken(retrievedUser, token, expirationDate);

        emailService.sendPasswordReset(tokenEmail, resetEmail, token);

        // Just in case the user had a previous forget token they never clicked on
        this.passwordResetTokenRepository.deleteByUser(retrievedUser);
        this.passwordResetTokenRepository.flush();

        this.passwordResetTokenRepository.save(passwordResetToken);
    }

    /**
     * Sends email to authorized user email enabling them to create a new password.
     * This variant can only be used by admins, and it allows for sending the email
     * to an address other than the one owning the account
     *
     * @param user The user to send the reset password email to.
     */
    @Transactional
    @PutMapping(AppRoutes.Accounts.FORGOT_PASSWORD_NO_EMAIL)
    public void forgotPasswordNoEmail(@Valid @RequestBody PasswordForgottenRequest user) {
        SafaUser currentUser = getCurrentUser();
        permissionService.requireActiveSuperuser(currentUser);
        forgotPassword(user.getEmail(), currentUser.getEmail());
    }

    /**
     * Under construction. Sends email to reset password for
     *
     * @param passwordResetRequest Request containing token signed by user and their new password
     * @return {@link UserAppEntity} The user identifier whose password was changed.
     */
    @PutMapping(AppRoutes.Accounts.RESET_PASSWORD)
    public UserAppEntity resetPassword(@Valid @RequestBody ResetPasswordRequestDTO passwordResetRequest) {
        // Step - Extract required information
        String resetToken = passwordResetRequest.getResetToken();
        String newPassword = passwordResetRequest.getNewPassword();

        // Step - check the reset token was issued by us
        PasswordResetToken passwordResetToken = passwordResetTokenRepository.findByToken(resetToken)
            .orElseThrow(() -> new SafaError("Illegal expiration token"));

        resetToken = passwordResetToken.getToken();

        // Step - Decode token and extract user
        Claims userClaims = this.tokenService.getTokenClaims(resetToken);
        String username = userClaims.getSubject();
        SafaUser retrievedUser = this.safaUserRepository.findByEmail(username)
            .orElseThrow(() -> new UsernameNotFoundException("Username does not exist:" + username));

        // Step - Check the token has no expired
        if (userClaims.getExpiration().before(new Date())) {
            throw new SafaError("Reset password token has expired.");
        }

        retrievedUser.setPassword(passwordEncoder.encode(newPassword));
        retrievedUser = this.safaUserRepository.save(retrievedUser);
        this.passwordResetTokenRepository.delete(passwordResetToken);
        return safaUserService.toAppEntity(retrievedUser);
    }

    /**
     * Updates the user's password to new one if their current password is validated.
     *
     * @param passwordChangeRequest Password change request containing current and new password.
     * @return {@link UserAppEntity} The user entity whose password was set.
     */
    @PutMapping(AppRoutes.Accounts.CHANGE_PASSWORD)
    public UserAppEntity changePassword(@Valid @RequestBody PasswordChangeRequest passwordChangeRequest) {
        SafaUser principal = safaUserService.getCurrentUser();

        if (passwordChangeRequest.getNewPassword().equals(passwordChangeRequest.getOldPassword())) {
            throw new SafaError("New password cannot be the same with the old one.");
        }

        if (!this.passwordEncoder.matches(passwordChangeRequest.getOldPassword(), principal.getPassword())) {
            throw new SafaError("Invalid old password");
        }

        principal.setPassword(passwordEncoder.encode(passwordChangeRequest.getNewPassword()));
        principal = this.safaUserRepository.save(principal);
        return safaUserService.toAppEntity(principal);
    }

    @GetMapping(AppRoutes.Accounts.SELF)
    public UserAppEntity retrieveCurrentUser() {
        return safaUserService.toAppEntity(safaUserService.getCurrentUser());
    }

    @GetMapping(AppRoutes.Accounts.ROOT)
    public List<UserAppEntity> retrieveAllUsers() {
        permissionService.requireSuperuser(getCurrentUser());
        List<UserAppEntity> users = new ArrayList<>();
        safaUserRepository.findAll().forEach(user -> users.add(safaUserService.toAppEntity(user)));
        return users;
    }

    @PutMapping(AppRoutes.Accounts.DEFAULT_ORG)
    public void updateDefaultOrg(@RequestBody DefaultOrgDTO newOrgDto) {
        SafaUser currentUser = getCurrentUser();
        safaUserService.updateDefaultOrg(currentUser, newOrgDto.defaultOrgId);
    }

    /**
     * Set the user with the given email to be a superuser
     *
     * @param body The request body containing the user's email
     */
    @PutMapping(AppRoutes.Accounts.SuperUser.ROOT)
    public void addSuperUser(@RequestBody CreateSuperUserDTO body) {
        SafaUser currentUser = getCurrentUser();
        permissionService.requireActiveSuperuser(currentUser);

        SafaUser updatedUser = safaUserService.getUserByEmail(body.getEmail());
        safaUserService.addSuperUser(updatedUser);

        Organization personalOrg = organizationService.getPersonalOrganization(updatedUser);
        personalOrg.setPaymentTier(PaymentTier.UNLIMITED);
        organizationService.updateOrganization(personalOrg);
    }

    /**
     * <p>Activate a user's superuser powers.</p>
     *
     * <p>A user's superuser powers are inactive by default to
     * help prevent accidental misuse. By activating superuser
     * powers, the user will be able to actually perform superuser
     * actions.</p>
     */
    @PutMapping(AppRoutes.Accounts.SuperUser.ACTIVATE)
    public void activateSuperuser() {
        SafaUser currentUser = getCurrentUser();
        permissionService.requireSuperuser(currentUser);
        permissionService.setActiveSuperuser(currentUser, true);
    }

    /**
     * <p>Deactivate a user's superuser powers.</p>
     *
     * <p>A user's superuser powers are inactive by default to
     * help prevent accidental misuse. Deactivating superuser
     * powers on a user whose powers are active will return them
     * to functioning like a normal user.</p>
     */
    @PutMapping(AppRoutes.Accounts.SuperUser.DEACTIVATE)
    public void deactivateSuperuser() {
        SafaUser currentUser = getCurrentUser();
        permissionService.setActiveSuperuser(currentUser, false);
    }

    /**
     * Execute a request as another user. Requires active superuser
     *
     * @param request The request details (autowired by Spring)
     * @param user The user to execute the request as
     * @return Whatever the underlying request returns, unless there is an error becoming the other user
     */
    @RequestMapping(AppRoutes.Accounts.IMPERSONATE + "/**")
    public ModelAndView executeAsUser(HttpServletRequest request, @PathVariable String user) {
        SafaUser currentUser = getCurrentUser();

        permissionService.requireActiveSuperuser(getCurrentUser());
        AuthorizationSetter.setSessionAuthorization(user, getServiceProvider());
        String path = request.getRequestURI().replace(AppRoutes.Accounts.IMPERSONATE.replace("{user}", user), "");

        String message = String.format(
                "Execute request as another user:%n\tRequest: %s %s%n\tAs-user: %s%n\tParams: %s",
                request.getMethod(), path, user, mapToString(request.getParameterMap()));
        auditLogService.createEntry(currentUser, message);

        return new ModelAndView("forward:" + path);
    }

    private String mapToString(Map<String, String[]> map) {
        try {
            return new ObjectMapper().writeValueAsString(map);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    @Data
    public static class DefaultOrgDTO {
        private UUID defaultOrgId;
    }

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public static class AccountVerificationDTO {
        private String token;
    }

    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    public static class CreateSuperUserDTO {
        private String email;
    }
}
