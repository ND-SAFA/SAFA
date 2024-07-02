package edu.nd.crc.safa.test.admin.usagestats;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.admin.usagestats.entities.app.AccountCreationStatistics;
import edu.nd.crc.safa.admin.usagestats.entities.app.GenerationStatistics;
import edu.nd.crc.safa.admin.usagestats.entities.app.GithubIntegrationStatistics;
import edu.nd.crc.safa.admin.usagestats.entities.app.OnboardingProgressSummaryDTO;
import edu.nd.crc.safa.admin.usagestats.entities.app.ProjectImportStatistics;
import edu.nd.crc.safa.admin.usagestats.entities.app.ProjectSummarizationStatistics;
import edu.nd.crc.safa.admin.usagestats.entities.app.UserStatisticsDTO;
import edu.nd.crc.safa.admin.usagestats.entities.db.ApplicationUsageStatistics;
import edu.nd.crc.safa.admin.usagestats.repositories.ApplicationUsageStatisticsRepository;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.generation.hgen.HGenResponse;
import edu.nd.crc.safa.features.generation.summary.SummaryResponse;
import edu.nd.crc.safa.features.github.entities.app.GithubAccessCredentialsDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubSelfResponseDTO;
import edu.nd.crc.safa.features.github.repositories.GithubAccessCredentialsRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.controllers.SafaUserController;
import edu.nd.crc.safa.features.users.entities.db.EmailVerificationToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.EmailVerificationTokenRepository;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.test.features.github.base.AbstractGithubGraphqlTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.assertj.core.data.Offset;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.ThrowingConsumer;
import org.mockito.Mockito;
import org.mockito.invocation.InvocationOnMock;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestOnboardingStats extends AbstractGithubGraphqlTest {

    private final List<UserDef> users = createUsers();
    private final Map<String, UUID> userProjects = new HashMap<>();
    @Autowired
    private SafaUserService userService;
    @Autowired
    private EmailVerificationTokenRepository verificationTokenRepository;
    @Autowired
    private ApplicationUsageStatisticsRepository usageStatsRepo;
    @Autowired
    private GithubAccessCredentialsRepository githubCredentialsRepo;
    @Autowired
    private OrganizationService organizationService;
    @Autowired
    private ProjectVersionRepository projectVersionRepository;
    @Autowired
    private ProjectService projectService;
    @Autowired
    private ArtifactVersionRepository artifactVersionRepository;
    @MockBean
    private GithubConnectionService githubConnectionService;
    @MockBean
    private GenApi genApi;

    private List<UserDef> createUsers() {
        List<UserDef> users = new ArrayList<>(15);
        for (int i = 0; i < 15; ++i) {
            users.add(new UserDef("user" + i, "password" + i));
        }
        users.add(new UserDef(currentUserName, defaultUserPassword));
        return users;
    }

    @BeforeEach
    public void setup() {
        userService.addSuperUser(getCurrentUser());
        makeUnlimited(getCurrentUser());

        for (UserDef user : users) {
            if (!user.getUsername().equals(currentUserName)) {
                rootBuilder.authorize(a -> a.createUser(user.getUsername(), user.getPassword()));
            }

            SafaUser safaUser = userService.getUserByEmail(user.getUsername());
            makeUnlimited(safaUser);
        }

        Mockito.doReturn(new GithubAccessCredentialsDTO())
            .when(githubConnectionService).useAccessCode(Mockito.anyString());
        Mockito.doReturn(new GithubSelfResponseDTO())
            .when(githubConnectionService).getSelf(Mockito.any());
        Mockito.doAnswer(call -> githubCredentialsRepo.findByUser(call.getArgument(0)))
            .when(githubConnectionService).getGithubCredentials(Mockito.any());
        Mockito.doAnswer(this::getProjectSummary)
            .when(genApi).generateProjectSummary(Mockito.any(), Mockito.any());
        Mockito.doAnswer(this::getHierarchy)
            .when(genApi).generateHierarchy(Mockito.any(), Mockito.any());
    }

    private void makeUnlimited(SafaUser user) {
        Organization userOrg = organizationService.getPersonalOrganization(user);
        userOrg.setPaymentTier(PaymentTier.UNLIMITED);
        organizationService.updateOrganization(userOrg);
    }

    private HGenResponse getHierarchy(InvocationOnMock invocationOnMock) {
        HGenResponse response = new HGenResponse();
        response.setSummary("");
        response.setArtifacts(List.of());
        return response;
    }

    private SummaryResponse getProjectSummary(InvocationOnMock invocationOnMock) {
        List<GenerationArtifact> artifacts = List.of();
        SummaryResponse response = new SummaryResponse();
        response.setSummary("");
        response.setArtifacts(artifacts);
        return response;
    }

    @Test
    public void testOnboardingStats() throws Exception {
        applyToUsers(this::verifyAccount, range(0, 16, 14));
        applyToUsers(this::removeProperTracking, range(0, 16, 8));
        applyToUsers(this::connectGithub, range(0, 16, 4));
        applyToUsers(this::importProject, range(0, 3, 3));
        applyToUsers(this::importProject, range(8, 11, 3));
        applyToUsers(this::doGeneration, range(0, 2, 2));
        applyToUsers(this::doGeneration, range(8, 10, 2));

        rootBuilder.authorize(a -> a.loginDefaultUser(this));
        OnboardingProgressSummaryDTO onboardingState = getOnboardingStats();

        AccountCreationStatistics accountStats = onboardingState.getAccounts();
        assertThat(accountStats.getCreated()).isEqualTo(16);
        assertThat(accountStats.getVerified()).isEqualTo(14);
        assertThat(accountStats.getHaveProperProgressTracking()).isEqualTo(8);

        GithubIntegrationStatistics githubStats = onboardingState.getGithub();
        assertThat(githubStats.getTotal().getAccounts()).isEqualTo(8);
        assertThat(githubStats.getTotal().getPercent()).isEqualTo(0.5);
        assertThat(githubStats.getWithProperTracking().getAccounts()).isEqualTo(4);
        assertThat(githubStats.getWithProperTracking().getPercent()).isEqualTo(0.5);

        ProjectImportStatistics importStats = onboardingState.getImports();
        assertThat(importStats.getTotal().getAccounts()).isEqualTo(6);
        assertThat(importStats.getTotal().getPercent()).isEqualTo(0.375);
        assertThat(importStats.getFromGithub().getAccounts()).isEqualTo(6);
        assertThat(importStats.getFromGithub().getPercent()).isEqualTo(0.75);
        assertThat(importStats.getFromGithubProper().getAccounts()).isEqualTo(3);
        assertThat(importStats.getFromGithubProper().getPercent()).isEqualTo(0.75);
        assertThat(importStats.getTotalPerformed()).isEqualTo(6);

        ProjectSummarizationStatistics summarizationStats = onboardingState.getSummarizations();
        assertThat(summarizationStats.getTotalPerformed()).isEqualTo(0); // TODO

        GenerationStatistics genStats = onboardingState.getGenerations();
        assertThat(genStats.getTotal().getAccounts()).isEqualTo(4);
        assertThat(genStats.getTotal().getPercent()).isEqualTo(0.25);
        assertThat(genStats.getFromImport().getAccounts()).isEqualTo(4);
        assertThat(genStats.getFromImport().getPercent()).isEqualTo(0.6666, Offset.offset(0.0001));
        assertThat(genStats.getFromImportProper().getAccounts()).isEqualTo(2);
        assertThat(genStats.getFromImportProper().getPercent()).isEqualTo(0.6666, Offset.offset(0.0001));
        assertThat(genStats.getTotalGenerations()).isEqualTo(4);
        assertThat(genStats.getLinesGeneratedOn()).isEqualTo(8096);

        UUID firstUserId = safaUserService.getUserByEmail(users.get(0).getUsername()).getUserId();
        UserStatisticsDTO firstUserStats = SafaRequest.withRoute(AppRoutes.Statistics.ONBOARDING_BY_USER)
                .withPathVariable("userId", firstUserId.toString())
                .getAsType(new TypeReference<>(){});
        assertThat(firstUserStats.getImportsPerformed()).isEqualTo(1);
        assertThat(firstUserStats.getSummarizationsPerformed()).isEqualTo(0);
        assertThat(firstUserStats.getGenerationsPerformed()).isEqualTo(1);
        assertThat(firstUserStats.getLinesGeneratedOn()).isEqualTo(2024);
        assertThat(firstUserStats.getAccountCreatedTime()).isNull();
        assertThat(firstUserStats.getGithubLinkedTime()).isNotNull();
        assertThat(firstUserStats.getFirstProjectImportedTime()).isNotNull();
        assertThat(firstUserStats.getFirstGenerationPerformedTime()).isNotNull();
    }

    private OnboardingProgressSummaryDTO getOnboardingStats() throws Exception {
        rootBuilder.authorize(a -> a.loginDefaultUser(this));
        return SafaRequest.withRoute(AppRoutes.Statistics.ONBOARDING_ROOT)
            .getAsType(new TypeReference<>() {
            });
    }

    private void verifyAccount(int index) {
        System.out.println("Verify " + index);
        SafaUser user = getUserAtIndex(index);
        EmailVerificationToken token = verificationTokenRepository.findByUserUserId(user.getUserId());

        SafaRequest.withRoute(AppRoutes.Accounts.VERIFY_ACCOUNT)
            .postWithJsonObject(new SafaUserController.AccountVerificationDTO(token.getToken()));
    }

    private void removeProperTracking(int index) {
        System.out.println("Remove tracking " + index);
        SafaUser user = getUserAtIndex(index);
        ApplicationUsageStatistics stats = usageStatsRepo.findByUser(user).orElseThrow();
        stats.setAccountCreated(null);
        usageStatsRepo.save(stats);
    }

    private void connectGithub(int index) throws Exception {
        System.out.println("Connect github " + index);
        becomeUser(index);
        SafaRequest.withRoute(AppRoutes.Github.Credentials.REGISTER)
            .withPathVariable("accessCode", "token")
            .postWithoutBody(status().is2xxSuccessful());
    }

    private void importProject(int index) throws IOException {
        System.out.println("Import project " + index);
        becomeUser(index);

        enqueueResponse("repository_response.json");
        enqueueResponse("filetree_response.json");
        enqueueResponse("filetree_response_src.json");
        enqueueResponse("filetree_response_include.json");

        GithubImportDTO importDTO = new GithubImportDTO();
        JobAppEntity job = SafaRequest.withRoute(AppRoutes.Github.Import.BY_NAME)
            .withPathVariable("repositoryName", "repo")
            .withPathVariable("owner", "owner")
            .postWithJsonObject(importDTO, JobAppEntity.class);

        userProjects.put(users.get(index).getUsername(), job.getProjectId());
    }

    private void doGeneration(int index) {
        System.out.println("Generate " + index);

        becomeUser(index);
        Organization org = organizationService.getPersonalOrganization(getUserAtIndex(index));
        org.setPaymentTier(PaymentTier.UNLIMITED);
        organizationService.updateOrganization(org);

        UUID projectId = userProjects.get(users.get(index).getUsername());
        Project project = projectService.getProjectById(projectId);
        ProjectVersion projectVersion = projectVersionRepository.findByProject(project).get(0);

        List<ArtifactVersion> artifactVersions = artifactVersionRepository.findByProjectVersion(projectVersion);
        List<UUID> artifactIds = artifactVersions.stream()
            .map(a -> a.getArtifact().getArtifactId())
            .toList();

        HGenRequest hGenRequest = new HGenRequest();
        hGenRequest.setArtifacts(artifactIds);
        hGenRequest.setTargetTypes(List.of("type1", "type2"));

        SafaRequest.withRoute(AppRoutes.HGen.GENERATE)
            .withVersion(projectVersion)
            .postWithJsonObject(hGenRequest);

    }

    private void becomeUser(int index) {
        UserDef user = users.get(index);
        rootBuilder.authorize(a -> a.loginUser(user.getUsername(), user.getPassword(), this));
    }

    private SafaUser getUserAtIndex(int index) {
        UserDef userDef = users.get(index);
        return safaUserService.getUserByEmail(userDef.getUsername());
    }

    private void applyToUsers(ThrowingConsumer<Integer> func, Iterable<Integer> indexes) {
        for (Integer i : indexes) {
            try {
                func.accept(i);
            } catch (Throwable e) {
                throw new RuntimeException(e);
            }
        }
    }

    private Iterable<Integer> range(int start, int end, int groupSize) {
        List<Integer> range = new ArrayList<>();

        for (int i = start; i < end; ++i) {
            if (((i - start) / groupSize) % 2 == 0) {
                range.add(i);
            }
        }

        return range;
    }

    @Data
    @AllArgsConstructor
    private static class UserDef {
        private String username;
        private String password;
    }
}
