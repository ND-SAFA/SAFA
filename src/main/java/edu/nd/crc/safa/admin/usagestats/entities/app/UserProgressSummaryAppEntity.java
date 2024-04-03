package edu.nd.crc.safa.admin.usagestats.entities.app;

import lombok.Data;

@Data
public class UserProgressSummaryAppEntity {
    private AccountCreationStatistics accounts;
    private GithubIntegrationStatistics github;
    private ProjectImportStatistics imports;
    private ProjectSummarizationStatistics summarizations;
    private GenerationStatistics generations;

    public UserProgressSummaryAppEntity() {
        accounts = new AccountCreationStatistics();
        github = new GithubIntegrationStatistics();
        imports = new ProjectImportStatistics();
        summarizations = new ProjectSummarizationStatistics();
        generations = new GenerationStatistics();
    }
}
