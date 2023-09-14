package edu.nd.crc.safa.features.commits.services.pipeline.steps;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.commits.services.pipeline.ICommitStep;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;

import org.javatuples.Pair;

public class CommitTraces implements ICommitStep {
    @Override
    public void performStep(CommitService service, ProjectCommit commit, ProjectCommit after) {
        Pair<ProjectChange<TraceAppEntity>, List<CommitError>> traceResponse = commitTraceChanges(
            service, commit);
        ProjectChange<TraceAppEntity> traceChanges = traceResponse.getValue0();
        after.setTraces(traceChanges);
        after.addErrors(traceResponse.getValue1());
    }

    private Pair<ProjectChange<TraceAppEntity>, List<CommitError>> commitTraceChanges(
        CommitService service,
        ProjectCommit commit) throws SafaError {
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
