package edu.nd.crc.safa.admin.usagestats.entities.app;

import java.time.LocalDateTime;

import edu.nd.crc.safa.admin.usagestats.entities.db.ApplicationUsageStatistics;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class UserStatisticsDTO {

    private int importsPerformed;
    private int summarizationsPerformed;
    private int generationsPerformed;
    private int linesGeneratedOn;

    private LocalDateTime accountCreatedTime;
    private LocalDateTime githubLinkedTime;
    private LocalDateTime firstProjectImportedTime;
    private LocalDateTime firstGenerationPerformedTime;

    public UserStatisticsDTO(ApplicationUsageStatistics stats) {
        this.importsPerformed = stats.getProjectImports();
        this.summarizationsPerformed = stats.getProjectSummarizations();
        this.generationsPerformed = stats.getProjectGenerations();
        this.linesGeneratedOn = stats.getLinesGeneratedOn();
        this.accountCreatedTime = stats.getAccountCreated();
        this.githubLinkedTime = stats.getGithubLinked();
        this.firstProjectImportedTime = stats.getProjectImported();
        this.firstGenerationPerformedTime = stats.getGenerationPerformed();
    }
}
