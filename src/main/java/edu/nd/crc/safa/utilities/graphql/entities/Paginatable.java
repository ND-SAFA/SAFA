package edu.nd.crc.safa.utilities.graphql.entities;

public interface Paginatable {

    /**
     * Get the path to the query file that can be used to get the next page of results.
     *
     * @return The path to the query file.
     */
    String getPaginationQuery();

}
