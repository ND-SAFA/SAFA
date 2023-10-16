package edu.nd.crc.safa.test.services;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
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

    public String loginDefaultUser(ApplicationBaseTest test) {
        String token = loginUser(
            ApplicationBaseTest.currentUserName,
            ApplicationBaseTest.defaultUserPassword,
            test).get();
        SafaUser currentUser = serviceProvider
            .getAccountLookupService()
            .getUserFromUsername(ApplicationBaseTest.currentUserName);
        test.setCurrentUser(currentUser, token);
        return token;
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

    public AndBuilder<AuthorizationTestService, String> loginUser(String email, String password,
                                                                  ApplicationBaseTest test) {
        return this.loginUser(email, password, true, test);
    }

    public AndBuilder<AuthorizationTestService, String> loginUser(String email, String password, boolean setToken,
                                                                  ApplicationBaseTest test) {
        String token = this.loginUser(email, password, status().is2xxSuccessful(), setToken, test);
        return new AndBuilder<>(this, token, this.state);
    }

    public String loginUser(String email, String password, ResultMatcher resultMatcher, ApplicationBaseTest test) throws Exception {
        return this.loginUser(email, password, resultMatcher, true, test);
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
                            boolean setToken,
                            ApplicationBaseTest test) {
        // Step - Clear token if setting new one
        if (setToken) {
            SafaRequest.clearAuthorizationToken();
        }

        Optional<Cookie> token = SafaRequest
            .withRoute(AppRoutes.Accounts.LOGIN)
            .sendPostRequestAndRetrieveCookie(new SafaUser(email, password),
                resultMatcher, SecurityConstants.JWT_COOKIE_NAME);


        if (token.isPresent()) { // Result matcher may have failing reques
            Cookie authorizationCookie = token.orElseThrow();
            String userToken = authorizationCookie.getValue();
            if (setToken) {
                SafaRequest.setAuthorizationToken(authorizationCookie);
                test.setCurrentUser(serviceProvider.getAccountLookupService().getUserFromUsername(email), userToken);
            }
            return userToken;
        }
        return null;
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
        List<ProjectMembership> projectMemberships =
            this.serviceProvider.getUserProjectMembershipRepository().findByProjectAndMember(
                project,
                safaUserOptional.get());
        if (projectMemberships.isEmpty()) {
            throw new SafaError("Could not find membership between {%s} and {%s}.",
                username,
                project.getName());

        }

        for (ProjectMembership membership : projectMemberships) {
            SafaRequest
                .withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
                .withEntityId(project.getProjectId())
                .withMembershipId(membership.getMembershipId())
                .deleteWithJsonObject(resultMatcher);
        }
    }

    public SafaUser getAccount(String email) {
        return this.serviceProvider.getAccountLookupService().getUserFromUsername(email);
    }
}
