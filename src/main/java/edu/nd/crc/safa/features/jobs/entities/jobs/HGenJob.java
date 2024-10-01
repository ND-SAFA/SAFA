package edu.nd.crc.safa.features.jobs.entities.jobs;

import edu.nd.crc.safa.features.billing.entities.db.Transaction;
import edu.nd.crc.safa.features.billing.services.TransactionService;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.GenerationPerformedEvent;
import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.generation.hgen.HGenService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.StringUtil;

/**
 * Generates trace links between artifacts defined in request.
 */
public class HGenJob extends GenerationJob {
    /**
     * The request to generate trace links.
     */
    private final HGenRequest hGenRequest;
    /**
     * The project version to commit summaries and generated links to.
     */
    private final ProjectVersion projectVersion;

    private Transaction billingTransaction;

    public HGenJob(SafaUser user,
                   JobDbEntity jobDbEntity,
                   ServiceProvider serviceProvider,
                   ProjectCommitDefinition projectCommitDefinition,
                   HGenRequest hGenRequest) {
        super(user, jobDbEntity, serviceProvider, projectCommitDefinition);
        this.hGenRequest = hGenRequest;
        this.projectVersion = projectCommitDefinition.getCommitVersion();
        billingTransaction = null;
    }

    public static String getJobName(HGenRequest request) {
        String result = StringUtil.join(request.getTargetTypes(), ",");
        return String.format("Generating artifacts: %s", result);
    }

    @IJobStep(value = "Generating Artifacts", position = 3)
    public void generatingArtifacts() {
        HGenService hGenService = this.getServiceProvider().getHGenService();
        String summary = this.projectVersion.getProject().getSpecification();
        this.hGenRequest.setSummary(summary);
        ProjectCommitDefinition projectCommitDefinition = hGenService.generateHierarchy(this.projectVersion,
            this.hGenRequest, this.getDbLogger());
        this.setProjectCommitDefinition(projectCommitDefinition);
    }

    @Override
    public void afterJob(boolean success) throws Exception {
        super.afterJob(success);

        if (success) {
            getServiceProvider().getEventPublisher()
                .publishEvent(new GenerationPerformedEvent(this, getUser(), projectVersion, hGenRequest));
        }

        if (billingTransaction != null) {
            TransactionService transactionService = getServiceProvider().getTransactionService();
            if (success) {
                transactionService.markTransactionSuccessful(billingTransaction);
            } else {
                transactionService.markTransactionFailed(billingTransaction);
            }
        }
    }
}
