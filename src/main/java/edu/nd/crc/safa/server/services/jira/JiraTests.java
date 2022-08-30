package edu.nd.crc.safa.server.services.jira;

import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Date;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.features.jira.entities.app.JiraIssuesResponseDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jira.repositories.JiraAccessCredentialsRepository;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class JiraTests {
    private final Logger log = LoggerFactory.getLogger(JiraTests.class);

    private final JiraConnectionService jiraConnectionService;
    private final JiraAccessCredentialsRepository jiraAccessCredentialsRepository;
    private final SafaUserRepository safaUserRepository;

    @PostConstruct
    private void init() {
        log.info("Initialising");
        //do_it();
    }

    private void do_it() {
        SafaUser user = safaUserRepository.findByEmail("marcuspopb@gmail.com")
            .orElseThrow(() -> new RuntimeException("User"));

        JiraAccessCredentials credentials = jiraAccessCredentialsRepository
            .findByUserAndCloudId(user, "aad1005f-a2ca-406a-982d-609589f8ac50")
            .orElseThrow(() -> new RuntimeException("Credentials"));

        LocalDate localDate = LocalDate.now().minusDays(10L);
        Date date = Date.from(
            localDate.atStartOfDay()
                .atZone(ZoneId.systemDefault())
                .toInstant()
        );
        Long jiraProjectId = 10004L;

        JiraIssuesResponseDTO jiraIssuesResponseDTO =
            jiraConnectionService.retrieveUpdatedJIRAIssues(credentials, jiraProjectId, date);

        jiraIssuesResponseDTO.getIssues().forEach(i -> {
            log.info(i.toString());
        });
    }
}
