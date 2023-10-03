package edu.nd.crc.safa.test.services;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.entities.db.UserProjectMembership;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.builders.AndBuilder;
import edu.nd.crc.safa.test.services.builders.BuilderState;

import jakarta.servlet.http.Cookie;
import lombok.AllArgsConstructor;
import org.springframework.test.web.servlet.ResultMatcher;

@AllArgsConstructor
public class AuthorizationTestService {

    ServiceProvider serviceProvider;
    BuilderState state;

    public String createDefaultAccount() {
        String defaultUser = ApplicationBaseTest.currentUserName;
        String defaultUserPassword = ApplicationBaseTest.defaultUserPassword;
        createUser(defaultUser, defaultUserPassword);
        ApplicationBaseTest.currentUser = serviceProvider
            .getAccountLookupService()
            .getUserFromUsername(defaultUser);
        return loginDefaultUser();
    }

    public String loginDefaultUser() {
        String authorizationCode = loginUser(
            ApplicationBaseTest.currentUserName,
            ApplicationBaseTest.defaultUserPassword).get();
        ApplicationBaseTest.currentUser = serviceProvider
            .getAccountLookupService()
            .getUserFromUsername(ApplicationBaseTest.currentUserName);
        return authorizationCode;
    }

    public AndBuilder<AuthorizationTestService, UserAppEntity> createUser(String email, String password) {
        SafaUser user = new SafaUser(email, password);
        UserAppEntity result = SafaRequest
            .withRoute(AppRoutes.Accounts.CREATE_ACCOUNT)
            .postWithJsonObject(user, UserAppEntity.class);
        return new AndBuilder<>(this, result, this.state);
    }

    public void createUser(String email, String password, ResultMatcher test) throws Exception {
        SafaUser user = new SafaUser(email, password);
        SafaRequest
            .withRoute(AppRoutes.Accounts.CREATE_ACCOUNT)
            .postWithJsonObject(user, test);
    }

    public AndBuilder<AuthorizationTestService, String> loginUser(String email, String password) {
        String result = this.loginUser(email, password, true);
        return new AndBuilder<>(this, result, this.state);
    }

    public String loginUser(String email, String password, boolean setToken) {
        return loginUser(email, password, status().is2xxSuccessful(), setToken);
    }

    public void loginUser(String email, String password, ResultMatcher test) throws Exception {
        this.loginUser(email, password, test, true);
    }

    /**
     * Sends request to login endpoint with given account credentials. Result matches
     * used to verify request response. If setToken is true, then token is set to global
     * SafaRequest variable.
     *
     * @param email         Account email.
     * @param password      Account password.
     * @param resultMatcher Expected HTTP response assertions.
     * @param setToken      Whether to set authorization token.
     */
    public String loginUser(String email,
                            String password,
                            ResultMatcher resultMatcher,
                            boolean setToken) {
        // Step - Clear token if setting new one
        if (setToken) {
            SafaRequest.clearAuthorizationToken();
        }

        Optional<Cookie> token = SafaRequest
            .withRoute(AppRoutes.Accounts.LOGIN)
            .sendPostRequestAndRetrieveCookie(new SafaUser(email, password),
                resultMatcher, SecurityConstants.JWT_COOKIE_NAME);

        if (setToken && token.isPresent()) {
            Cookie authorizationCookie = token.get();
            SafaRequest.setAuthorizationToken(authorizationCookie);
            String authorizationCode = authorizationCookie.getValue();
            return authorizationCode;
        } else {
            return null;
        }
    }

    public AuthorizationTestService removeMemberFromProject(Project project, String username) {
        removeMemberFromProject(project, username, status().is2xxSuccessful());
        return this;
    }

    public void removeMemberFromProject(Project project, String username, ResultMatcher resultMatcher) {

        Optional<SafaUser> safaUserOptional = this.serviceProvider
            .getSafaUserRepository()
            .findByEmail(username);
        if (safaUserOptional.isEmpty()) {
            throw new SafaError("Could not find user with name: %s", username);
        }
        Optional<UserProjectMembership> projectMembershipOptional =
            this.serviceProvider.getUserProjectMembershipRepository().findByProjectAndMember(
                project,
                safaUserOptional.get());
        if (projectMembershipOptional.isEmpty()) {
            throw new SafaError("Could not find membership between {%s} and {%s}.",
                username,
                project.getName());

        }
        SafaRequest
            .withRoute(AppRoutes.Projects.Membership.DELETE_PROJECT_MEMBERSHIP)
            .withProjectMembership(projectMembershipOptional.get())
            .deleteWithJsonObject(resultMatcher);
    }
}
