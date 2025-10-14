package edu.nd.crc.safa.test.admin;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.forwardedUrl;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.admin.auditlog.entities.db.AuditLogEntry;
import edu.nd.crc.safa.admin.auditlog.repositories.AuditLogRepository;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

public class TestExecuteRequestAsUser extends ApplicationBaseTest {

    @Autowired
    private AuditLogRepository auditLogRepo;

    private UserAppEntity otherUser;

    @BeforeEach
    public void setup() {
        this.rootBuilder.getCommonRequestService()
                .user()
                .makeUserSuperuser(getCurrentUser())
                .activateSuperuser();

        this.otherUser = this.rootBuilder
                .authorize((s, a) -> a
                        .createUser("otherUser@gmail.com", "password")
                        .save("sharee-user").get()).get();
    }

    @Test
    public void test() throws Exception {
        // MockMvc is super stripped down, so it cannot resolve the forwarding. All we can do is check
        // that the forwarding is happening and to the right url
        SafaRequest.getMockMvc().perform(
                MockMvcRequestBuilders
                        .get(AppRoutes.Accounts.IMPERSONATE + AppRoutes.Accounts.SELF, otherUser.getEmail())
                        .cookie(SafaRequest.getAuthorizationToken())
                )
                .andExpect(forwardedUrl(AppRoutes.Accounts.SELF));

        // List<AuditLogEntryDTO> auditLogs =
        //         SafaRequest.withRoute(AppRoutes.Audit.LOGS)
        //                 .getAsType(new TypeReference<>(){});
        // Can't do this ^^ because the Between part of the repo works different in test mode so the list is always empty :eyeroll:

        List<AuditLogEntry> auditLogs = new ArrayList<>();
        auditLogRepo.findAll().forEach(auditLogs::add);
        assertThat(auditLogs.size()).isEqualTo(1);

        AuditLogEntry entry = auditLogs.get(0);
        assertThat(entry.getEntry())
                .contains(otherUser.getEmail())
                .contains("GET " + AppRoutes.Accounts.SELF);
        assertThat(entry.getUserEmail()).isEqualTo(currentUserName);
    }
}
