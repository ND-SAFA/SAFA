package edu.nd.crc.safa.features.commits.entities.app;

import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import org.javatuples.Pair;

/**
 * Defines a lambda for containing a commit action
 * and returning the version entity if successful
 * or the error otherwise.
 */
public interface CommitAction<A, V> {
    Pair<V, CommitError> commitAction(A a) throws SafaError;
}
