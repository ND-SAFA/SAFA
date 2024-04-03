package edu.nd.crc.safa.admin.usagestats;

import edu.nd.crc.safa.admin.usagestats.entities.db.ApplicationUsageStatistics;
import edu.nd.crc.safa.admin.usagestats.repositories.ApplicationUsageStatisticsRepository;
import edu.nd.crc.safa.features.github.entities.events.GithubLinkedEvent;
import edu.nd.crc.safa.features.github.entities.events.GithubProjectImportedEvent;
import edu.nd.crc.safa.features.github.entities.events.ProjectSummarizedEvent;
import edu.nd.crc.safa.features.users.entities.AccountCreatedEvent;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.RequiredArgsConstructor;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ApplicationUsageStatisticsService {

    private final ApplicationUsageStatisticsRepository statsRepo;

    /**
     * Get statistics for a user
     *
     * @param user The user
     * @return The user's usage statistics
     */
    public ApplicationUsageStatistics getByUser(SafaUser user) {
        return statsRepo.findByUser(user).orElseGet(() -> {
            ApplicationUsageStatistics stats = new ApplicationUsageStatistics(user);
            return statsRepo.save(stats);
        });
    }

    /**
     * Handle account created event by setting the account creation time for the user
     *
     * @param event Event with details about the account creation
     */
    @EventListener
    public void handleAccountCreated(AccountCreatedEvent event) {
        ApplicationUsageStatistics stats = getByUser(event.getUser());
        stats.setAccountCreated(event.getCreatedTime());
        statsRepo.save(stats);
    }

    /**
     * Handle github linked event by setting the github link time for the user, if it was not already set
     *
     * @param event Event with details about the github link
     */
    @EventListener
    public void handleGithubLinked(GithubLinkedEvent event) {
        ApplicationUsageStatistics stats = getByUser(event.getUser());

        if (stats.getGithubLinked() == null) {
            stats.setGithubLinked(event.getLinkedTime());
            statsRepo.save(stats);
        }
    }

    /**
     * Handle github project imported event by setting the github project import time for the user,
     * if it was not already set, and incrementing the number of projects imported for the user
     *
     * @param event Event with details about the github project import
     */
    @EventListener
    public void handleGithubProjectImported(GithubProjectImportedEvent event) {
        ApplicationUsageStatistics stats = getByUser(event.getUser());

        if (stats.getProjectImported() == null) {
            stats.setProjectImported(event.getImportedTime());
        }

        stats.setProjectImports(stats.getProjectImports() + 1);
        statsRepo.save(stats);
    }


    /**
     * Handle github project imported event by incrementing the number of projects summarized for the user
     *
     * @param event Event with details about the summarization
     */
    @EventListener
    public void handleProjectSummarized(ProjectSummarizedEvent event) {
        ApplicationUsageStatistics stats = getByUser(event.getUser());
        stats.setProjectSummarizations(stats.getProjectSummarizations() + 1);
        statsRepo.save(stats);
    }
}
