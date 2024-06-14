package edu.nd.crc.safa.admin.usagestats;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

import edu.nd.crc.safa.admin.usagestats.entities.app.AccountCreationStatistics;
import edu.nd.crc.safa.admin.usagestats.entities.app.GenerationStatistics;
import edu.nd.crc.safa.admin.usagestats.entities.app.GithubIntegrationStatistics;
import edu.nd.crc.safa.admin.usagestats.entities.app.OnboardingProgressSummaryDTO;
import edu.nd.crc.safa.admin.usagestats.entities.app.ProjectImportStatistics;
import edu.nd.crc.safa.admin.usagestats.entities.app.ProjectSummarizationStatistics;
import edu.nd.crc.safa.admin.usagestats.entities.db.ApplicationUsageStatistics;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.NONE)
public class ProgressSummaryCalculator {

    /**
     * Calculate a user progress summary from the collection of user usage statistics objects
     *
     * @param stats All user usage stats
     * @return Calculated progress summary
     */
    public static OnboardingProgressSummaryDTO fromUsageStats(Iterable<ApplicationUsageStatistics> stats) {
        OnboardingProgressSummaryDTO summaryObj = new OnboardingProgressSummaryDTO();

        for (ApplicationUsageStatistics userStats : stats) {
            countUser(summaryObj, userStats);
        }

        calculateAverages(summaryObj);

        return summaryObj;
    }

    private static void countUser(OnboardingProgressSummaryDTO summaryObj, ApplicationUsageStatistics userStats) {
        countAccountCreation(summaryObj.getAccounts(), userStats);
        countGithub(summaryObj.getGithub(), userStats);
        countImports(summaryObj.getImports(), userStats);
        countSummarizations(summaryObj.getSummarizations(), userStats);
        countGenerations(summaryObj.getGenerations(), userStats);
    }

    private static void countAccountCreation(AccountCreationStatistics creationStats,
                                             ApplicationUsageStatistics userStats) {
        creationStats.setCreated(creationStats.getCreated() + 1);

        if (userStats.getUser().isVerified()) {
            creationStats.setVerified(creationStats.getVerified() + 1);
        }

        if (isProperTrackedAccount(userStats)) {
            creationStats.setHaveProperProgressTracking(creationStats.getHaveProperProgressTracking() + 1);
        }
    }

    private static void countGithub(GithubIntegrationStatistics githubStats, ApplicationUsageStatistics userStats) {
        if (!isGithubLinked(userStats)) {
            return;
        }

        GithubIntegrationStatistics.GithubIntegrationStatisticsSingle total = githubStats.getTotal();
        total.setAccounts(total.getAccounts() + 1);

        if (isProperTrackedAccount(userStats)) {
            GithubIntegrationStatistics.GithubIntegrationStatisticsSingle withProperTracking =
                    githubStats.getWithProperTracking();
            withProperTracking.setAccounts(withProperTracking.getAccounts() + 1);
            withProperTracking.setAverageTime(withProperTracking.getAverageTime()
                    + timeBetween(userStats.getAccountCreated(), userStats.getGithubLinked()));
        }
    }

    private static void countImports(ProjectImportStatistics importStats, ApplicationUsageStatistics userStats) {
        if (!isProjectImported(userStats)) {
            return;
        }

        importStats.setTotalPerformed(importStats.getTotalPerformed() + userStats.getProjectImports());

        ProjectImportStatistics.ImportStatisticsSingle total = importStats.getTotal();
        total.setAccounts(total.getAccounts() + 1);

        if (isGithubLinked(userStats)) {
            ProjectImportStatistics.ImportStatisticsSingle fromGithub = importStats.getFromGithub();
            fromGithub.setAccounts(fromGithub.getAccounts() + 1);
            fromGithub.setAverageTime(fromGithub.getAverageTime()
                    + timeBetween(userStats.getGithubLinked(), userStats.getProjectImported()));

            if (isProperTrackedAccount(userStats)) {
                ProjectImportStatistics.ImportStatisticsSingle fromGithubProper = importStats.getFromGithubProper();
                fromGithubProper.setAccounts(fromGithubProper.getAccounts() + 1);
                fromGithubProper.setAverageTime(fromGithubProper.getAverageTime()
                        + timeBetween(userStats.getGithubLinked(), userStats.getProjectImported()));
            }
        }
    }

    private static void countSummarizations(ProjectSummarizationStatistics summaryStats,
                                            ApplicationUsageStatistics userStats) {
        int userSummaries = userStats.getProjectSummarizations();
        summaryStats.setTotalPerformed(summaryStats.getTotalPerformed() + userSummaries);
    }

    private static void countGenerations(GenerationStatistics generationStats, ApplicationUsageStatistics userStats) {
        if (!isGenerated(userStats)) {
            return;
        }

        int userGenerations = userStats.getProjectGenerations();
        int userLinesGeneratedOn = userStats.getLinesGeneratedOn();
        generationStats.setTotalGenerations(generationStats.getTotalGenerations() + userGenerations);
        generationStats.setLinesGeneratedOn(generationStats.getLinesGeneratedOn() + userLinesGeneratedOn);

        GenerationStatistics.GenerationStatisticsSingle total = generationStats.getTotal();
        total.setAccounts(total.getAccounts() + 1);

        if (isProjectImported(userStats)) {
            GenerationStatistics.GenerationStatisticsSingle fromImport = generationStats.getFromImport();
            fromImport.setAccounts(fromImport.getAccounts() + 1);
            fromImport.setAverageTime(fromImport.getAverageTime()
                    + timeBetween(userStats.getProjectImported(),userStats.getGenerationPerformed()));

            if (isProperTrackedAccount(userStats)) {
                GenerationStatistics.GenerationStatisticsSingle fromImportProper =
                        generationStats.getFromImportProper();
                fromImportProper.setAccounts(fromImportProper.getAccounts() + 1);
                fromImportProper.setAverageTime(fromImportProper.getAverageTime()
                        + timeBetween(userStats.getProjectImported(),userStats.getGenerationPerformed()));
            }
        }
    }

    private static boolean isProperTrackedAccount(ApplicationUsageStatistics userStats) {
        return userStats.getAccountCreated() != null;
    }

    private static boolean isGithubLinked(ApplicationUsageStatistics userStats) {
        return userStats.getGithubLinked() != null;
    }

    private static boolean isProjectImported(ApplicationUsageStatistics userStats) {
        return userStats.getProjectImported() != null;
    }

    private static boolean isGenerated(ApplicationUsageStatistics userStats) {
        return userStats.getGenerationPerformed() != null;
    }

    private static long timeBetween(LocalDateTime ldt1, LocalDateTime ldt2) {
        return ChronoUnit.SECONDS.between(ldt1, ldt2);
    }

    private static void calculateAverages(OnboardingProgressSummaryDTO summaryObj) {
        calculateAveragesGithub(summaryObj);
        calculateAveragesImport(summaryObj);
        calculateAveragesGeneration(summaryObj);
    }

    private static void calculateAveragesGithub(OnboardingProgressSummaryDTO summaryObj) {
        AccountCreationStatistics accounts = summaryObj.getAccounts();
        GithubIntegrationStatistics github = summaryObj.getGithub();

        GithubIntegrationStatistics.GithubIntegrationStatisticsSingle total = github.getTotal();
        GithubIntegrationStatistics.GithubIntegrationStatisticsSingle withTracking = github.getWithProperTracking();

        total.setPercent(safeDivide(total.getAccounts(), accounts.getCreated()));
        total.setAverageTime(-1);
        withTracking.setPercent(safeDivide(withTracking.getAccounts(), accounts.getHaveProperProgressTracking()));
        withTracking.setAverageTime((long) safeDivide(withTracking.getAverageTime(), withTracking.getAccounts()));
    }

    private static void calculateAveragesImport(OnboardingProgressSummaryDTO summaryObj) {
        AccountCreationStatistics accounts = summaryObj.getAccounts();
        GithubIntegrationStatistics github = summaryObj.getGithub();
        ProjectImportStatistics imports = summaryObj.getImports();

        ProjectImportStatistics.ImportStatisticsSingle total = imports.getTotal();
        ProjectImportStatistics.ImportStatisticsSingle fromGithub = imports.getFromGithub();
        ProjectImportStatistics.ImportStatisticsSingle fromGithubProper = imports.getFromGithubProper();

        total.setPercent(safeDivide(total.getAccounts(), accounts.getCreated()));
        total.setAverageTime(-1);
        fromGithub.setPercent(safeDivide(fromGithub.getAccounts(), github.getTotal().getAccounts()));
        fromGithub.setAverageTime((long) safeDivide(fromGithub.getAverageTime(), fromGithub.getAccounts()));
        fromGithubProper.setPercent(
                safeDivide(fromGithubProper.getAccounts(), github.getWithProperTracking().getAccounts()));
        fromGithubProper.setAverageTime(
                (long) safeDivide(fromGithubProper.getAverageTime(), fromGithubProper.getAccounts()));
    }

    private static void calculateAveragesGeneration(OnboardingProgressSummaryDTO summaryObj) {
        AccountCreationStatistics accounts = summaryObj.getAccounts();
        ProjectImportStatistics imports = summaryObj.getImports();
        GenerationStatistics generations = summaryObj.getGenerations();

        GenerationStatistics.GenerationStatisticsSingle total = generations.getTotal();
        GenerationStatistics.GenerationStatisticsSingle fromImport = generations.getFromImport();
        GenerationStatistics.GenerationStatisticsSingle fromImportProper = generations.getFromImportProper();

        total.setPercent(safeDivide(total.getAccounts(), accounts.getCreated()));
        total.setAverageTime(-1);
        fromImport.setPercent(safeDivide(fromImport.getAccounts(), imports.getTotal().getAccounts()));
        fromImport.setAverageTime((long) safeDivide(fromImport.getAverageTime(), fromImport.getAccounts()));
        fromImportProper.setPercent(
                safeDivide(fromImportProper.getAccounts(), imports.getFromGithubProper().getAccounts()));
        fromImportProper.setAverageTime(
                (long) safeDivide(fromImportProper.getAverageTime(), fromImportProper.getAccounts()));
    }

    private static double safeDivide(double a, double b) {
        if (b == 0) {
            return -1;
        } else {
            return a / b;
        }
    }

}
