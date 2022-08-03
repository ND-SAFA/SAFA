package edu.nd.crc.safa.server.entities.api;

import edu.nd.crc.safa.server.entities.db.CommitError;

import org.javatuples.Pair;

/**
 * Defines a lambda for containing a commit action
 * and returning the version entity if successful
 * or the error otherwise.
 */
public interface CommitAction<A, V> {
    Pair<V, CommitError> commitAction(A a) throws SafaError;
}
