package edu.nd.crc.safa.features.commits.pipeline.steps;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.commits.pipeline.ICommitStep;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;

import org.javatuples.Pair;

public class CommitTraces implements ICommitStep {
    /**
     * Commits trace changes to project version.
     *
     * @param service          The commit service to access database and other services.
     * @param commitDefinition The commit being performed.
     * @param result           The commit final state.
     */
    @Override
    public void performStep(CommitService service, ProjectCommitDefinition commitDefinition,
                            ProjectCommitAppEntity result) {
        Pair<ProjectChange<TraceAppEntity>, List<CommitError>> traceResponse = commitTraceChanges(
            service, commitDefinition);
        ProjectChange<TraceAppEntity> traceChanges = traceResponse.getValue0();
        result.setTraces(traceChanges);
        result.addErrors(traceResponse.getValue1());
    }

    private Pair<ProjectChange<TraceAppEntity>, List<CommitError>> commitTraceChanges(
        CommitService service,
        ProjectCommitDefinition commit) throws SafaError {
        TraceLinkVersionRepository traceLinkRepository = service.getTraceLinkVersionRepository();
        return service.commitEntityChanges(
            commit.getCommitVersion(),
            commit.getTraces(),
            traceLinkRepository,
            traceLinkRepository::retrieveAppEntityFromVersionEntity,
            commit.isFailOnError(),
            commit.getUser());
    }
}
