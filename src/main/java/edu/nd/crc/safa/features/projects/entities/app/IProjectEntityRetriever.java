package edu.nd.crc.safa.features.projects.entities.app;

import java.util.List;

import edu.nd.crc.safa.features.projects.entities.db.Project;

/**
 * Represents the commonality between all the repositories used for retrieving artifacts.
 *
 * @param <T> The type of artifact returned by repository.
 */
public interface IProjectEntityRetriever<T> {

    List<T> getByProject(Project project);
}
