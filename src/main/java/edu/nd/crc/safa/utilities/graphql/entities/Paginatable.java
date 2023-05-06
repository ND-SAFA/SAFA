package edu.nd.crc.safa.utilities.graphql.entities;

import java.util.List;
import java.util.function.Consumer;

public interface Paginatable<T> {

    /**
     * Get the function that will be used to paginate the query. The function will take in a list of
     * objects to be paginated and will add objects from the addition pages to that list.
     *
     * @return The pagination function.
     */
    Consumer<List<T>> getPaginationFunction();

}
