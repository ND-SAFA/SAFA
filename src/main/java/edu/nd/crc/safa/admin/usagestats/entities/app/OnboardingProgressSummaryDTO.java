package edu.nd.crc.safa.admin.usagestats.entities.app;

import lombok.Data;

@Data
public class OnboardingProgressSummaryDTO {
    private AccountCreationStatistics accounts;
    private GithubIntegrationStatistics github;
    private ProjectImportStatistics imports;
    private ProjectSummarizationStatistics summarizations;
    private GenerationStatistics generations;

    public OnboardingProgressSummaryDTO() {
        accounts = new AccountCreationStatistics();
        github = new GithubIntegrationStatistics();
        imports = new ProjectImportStatistics();
        summarizations = new ProjectSummarizationStatistics();
        generations = new GenerationStatistics();
    }
}
