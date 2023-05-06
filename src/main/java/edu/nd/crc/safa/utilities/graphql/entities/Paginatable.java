package edu.nd.crc.safa.utilities.graphql.entities;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

public interface Paginatable {

    /**
     * Perform any pagination that is necessary within this type.
     *
     * @param user The user making the request.
     */
    void paginate(SafaUser user);

}
