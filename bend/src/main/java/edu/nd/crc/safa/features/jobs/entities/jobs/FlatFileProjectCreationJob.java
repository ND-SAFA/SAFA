package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.io.IOException;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.email.services.EmailService;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.flatfiles.builder.steps.GenerateTraceLinksStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.ParseArtifactStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.ParseProjectSummaryStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.ParseTraces;
import edu.nd.crc.safa.features.flatfiles.builder.steps.ParsingSetupStep;
import edu.nd.crc.safa.features.flatfiles.builder.steps.SummarizeArtifactsStep;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.CommitJobUtility;
import edu.nd.crc.safa.utilities.FileUtilities;

/**
 * Responsible for providing step implementations for parsing flat files
 * to use the project creation worker.
 */
public class FlatFileProjectCreationJob extends CommitJob {
    /**
     * Whether job is updating project.
     */
    private final boolean isNewProject;
    /**
     * The store used to configure that flat file builder.
     */
    private final FlatFileBuilderStore store;

    public FlatFileProjectCreationJob(SafaUser user,
                                      JobDbEntity jobDbEntity,
                                      ServiceProvider serviceProvider,
                                      FlatFileBuilderStore store,
                                      boolean isNewProject) {
        super(user, jobDbEntity, serviceProvider, store.getProjectCommitDefinition(), isNewProject);
        this.store = store;
        this.isNewProject = isNewProject;
        setAsCompleteSet(store.isAsCompleteSet());
    }

    @IJobStep(value = "Parsing Files", position = 1)
    public void parsingFiles(JobLogger logger) throws Exception {
        this.store.setJobLogger(logger);
        ParsingSetupStep parsingStep = new ParsingSetupStep();
        parsingStep.perform(this.store, getServiceProvider());

        ParseProjectSummaryStep projectSummaryStep = new ParseProjectSummaryStep();
        projectSummaryStep.perform(this.store, getServiceProvider());

        ParseArtifactStep parseArtifactStep = new ParseArtifactStep();
        parseArtifactStep.perform(this.store, getServiceProvider());

        ParseTraces parseTraces = new ParseTraces();
        parseTraces.perform(this.store, getServiceProvider());
    }

    @IJobStep(value = "Summarizing Code Artifacts", position = 2)
    public void summarizeCodeArtifacts() throws Exception {
        SummarizeArtifactsStep summarizeArtifactsStep = new SummarizeArtifactsStep();
        summarizeArtifactsStep.perform(this.store, getServiceProvider());
    }

    @IJobStep(value = "Generating Trace Links", position = 3)
    public void generatingTraces(JobLogger logger) throws Exception {
        GenerateTraceLinksStep generateTraceLinksStep = new GenerateTraceLinksStep();
        generateTraceLinksStep.perform(this.store, getServiceProvider());
    }

    @Override
    protected void jobFailed(Exception error) throws RuntimeException, IOException {
        if (this.isNewProject) {
            CommitJobUtility.deleteCommitProject(this);
        }
    }

    @Override
    protected void afterJob(boolean success) throws Exception {
        Project project = this.store.getProjectVersion().getProject();
        String projectPath = ProjectPaths.Storage.projectPath(project, true);
        FileUtilities.deletePath(projectPath);

        if (this.store.isSummarizeArtifacts() || this.store.getFlatFileParser().getTGenRequestAppEntity().size() > 0) {
            EmailService emailService = getServiceProvider().getEmailService();
            emailService.sendGenerationFinished(getUser().getEmail(), getProjectVersion(), getJobDbEntity(), success);
        }
    }
}
