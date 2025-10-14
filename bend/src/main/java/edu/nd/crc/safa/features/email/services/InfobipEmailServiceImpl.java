package edu.nd.crc.safa.features.email.services;

import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.FendPathConfig;
import edu.nd.crc.safa.features.email.entities.InfobipProperties;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.memberships.entities.db.MembershipInviteToken;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.infobip.ApiClient;
import com.infobip.ApiException;
import com.infobip.ApiKey;
import com.infobip.BaseUrl;
import com.infobip.api.EmailApi;
import com.infobip.model.EmailSendResponse;
import lombok.RequiredArgsConstructor;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

/**
 * {@link EmailService} implementation using Infobip's email API.
 */
@Service
@ConditionalOnProperty(
    value = "email.provider",
    havingValue = "infobip",
    matchIfMissing = true
)
@RequiredArgsConstructor(onConstructor = @__({@Autowired}))
public class InfobipEmailServiceImpl implements EmailService {

    private static final Logger log = LoggerFactory.getLogger(InfobipEmailServiceImpl.class.getName());

    private final InfobipProperties infobipProperties;
    private final FendPathConfig fendPathConfig;

    @Value("${bend.base}")
    private String bendBase;

    private EmailApi emailApi;

    @PostConstruct
    public void init() {
        ApiClient client = ApiClient.forApiKey(ApiKey.from(infobipProperties.getApiKey()))
            .withBaseUrl(BaseUrl.from(infobipProperties.getEndpoint()))
            .build();

        this.emailApi = new EmailApi(client);
    }

    @Override
    public void sendPasswordReset(String recipient, String resetAccount, String token) {
        String body = "Here is the requested link to reset the password for the account belonging to " + resetAccount
            + "\n\n" + String.format(fendPathConfig.getResetPasswordUrl(), token);
        sendSimpleEmail(recipient, "Requested password reset token", body);
    }

    @Override
    public void sendEmailVerification(String recipient, String token) {
        String url = String.format(fendPathConfig.getVerifyEmailUrl(), token);
        sendTemplatedEmail(List.of(recipient), InfobipProperties.EmailType.VERIFY_EMAIL_ADDRESS,
            Map.of(
                "accountlink", url
            )
        );
    }

    @Override
    public void sendGenerationCompleted(String recipient, ProjectVersion projectVersion, JobDbEntity jobEntity) {
        sendTemplatedEmail(List.of(recipient), InfobipProperties.EmailType.GENERATION_COMPLETED,
            Map.of(
                "jobName", projectVersion.getProject().getName(),
                "projectLink", makeProjectVersionLink(projectVersion)
            )
        );
    }

    @Override
    public void sendGenerationFailed(String recipient, ProjectVersion projectVersion, JobDbEntity jobEntity) {
        sendTemplatedEmail(List.of(recipient), InfobipProperties.EmailType.GENERATION_FAILED,
            Map.of(
                "jobName", projectVersion.getProject().getName()
            )
        );
        sendSimpleEmail("generate@safa.ai", "Customer generation failed",
            makeFailedGenerationText(projectVersion, jobEntity));
    }

    @Override
    public void sendMembershipInvite(String recipient, IEntityWithMembership entity, MembershipInviteToken token) {
        // TODO update with templated email
        sendSimpleEmail(recipient, "New Invitation",
            String.format(
                "You have been invited to join the %s %s. Please use the link below to accept the invitation\n%s",
                getEntityType(entity), getEntityName(entity),
                String.format(fendPathConfig.getAcceptInviteUrl(), token.getId())
            )
        );
    }

    private String getEntityName(IEntityWithMembership entity) {
        if (entity instanceof Organization) {
            return ((Organization) entity).getName();
        } else if (entity instanceof Team) {
            return ((Team) entity).getName();
        } else if (entity instanceof Project) {
            return ((Project) entity).getName();
        } else {
            throw new IllegalArgumentException("Unknown type " + entity.getClass());
        }
    }

    private String getEntityType(IEntityWithMembership entity) {
        if (entity instanceof Organization) {
            return "Organization";
        } else if (entity instanceof Team) {
            return "Team";
        } else if (entity instanceof Project) {
            return "Project";
        } else {
            throw new IllegalArgumentException("Unknown type " + entity.getClass());
        }
    }

    private void sendSimpleEmail(String recipient, String subject, String text) {
        EmailSendResponse response = wrapSendEmail(() ->
            sendConfiguredEmail(
                emailApi
                    .sendEmail(List.of(recipient))
                    .from(infobipProperties.getSenderAddress())
                    .subject(subject)
                    .text(text)
            )
        );

        log.info("Email sent to " + recipient + " - subject \"" + subject + "\": " + response);
    }

    private void sendTemplatedEmail(List<String> recipients, InfobipProperties.EmailType emailType,
                                    Map<String, String> replacements) {
        EmailSendResponse response = wrapSendEmail(() -> {

            JSONObject placeholdersObject = new JSONObject(replacements);
            Long templateId = infobipProperties.getEmails().get(emailType).templateId();

            return sendConfiguredEmail(
                emailApi
                    .sendEmail(recipients)
                    .from(infobipProperties.getSenderAddress())
                    .templateId(templateId)
                    .defaultPlaceholders(placeholdersObject.toString())
            );
        });

        log.info(emailType + " email sent to " + recipients + ": " + response);
    }

    /**
     * Sends an email that we have finished generating if sending emails is enabled in the config
     *
     * @param emailRequest The email request to send
     * @return The response from sending the email, or null if email sending is disabled
     */
    private EmailSendResponse sendConfiguredEmail(EmailApi.SendEmailRequest emailRequest) throws ApiException {
        if (!infobipProperties.isFakeEmails()) {
            return emailRequest.execute();
        } else {
            return null;
        }
    }

    /**
     * Wrap an email send call in a try catch for consistent error handling.
     *
     * @param emailSendFunction The function to send the email
     * @param <T> The type of the parameter returned by the email send function
     * @return Whatever the email send function returns
     */
    private <T> T wrapSendEmail(Callable<T> emailSendFunction) {
        try {
            return emailSendFunction.call();
        } catch (Exception e) {
            throw new SafaError("Failed to send email", e);
        }
    }

    private String makeProjectVersionLink(ProjectVersion projectVersion) {
        return fendPathConfig.getBase() + "/project?version=" + projectVersion.getId();
    }

    private String makeFailedGenerationText(ProjectVersion projectVersion, JobDbEntity jobEntity) {
        Team team = projectVersion.getProject().getOwningTeam();
        Organization organization = team.getOrganization();
        Project project = projectVersion.getProject();

        return "Generation job failed\n"
            + "Organization: name=" + organization.getName() + ", id=" + organization.getId()
                + ", paymentTier=" + organization.getPaymentTier() + "\n"
            + "Team: name=" + team.getName() + ", id=" + team.getId() + "\n"
            + "Project: name=" + project.getName() + ", id=" + project.getId() + "\n"
            + "Project version: number=" + projectVersion + ", id=" + projectVersion.getId() + "\n"
            + "Job Log Link: " + makeJobLogLink(jobEntity);
    }

    private String makeJobLogLink(JobDbEntity jobEntity) {
        if (jobEntity == null) {
            return "None (no job run)";
        }

        return bendBase + AppRoutes.Jobs.Logs.BY_JOB_ID.replace("{jobId}", jobEntity.getId().toString());
    }
}
