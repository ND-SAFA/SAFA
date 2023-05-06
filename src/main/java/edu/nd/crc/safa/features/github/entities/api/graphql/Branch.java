package edu.nd.crc.safa.features.github.entities.api.graphql;

import edu.nd.crc.safa.utilities.graphql.entities.Paginatable;

import lombok.Data;
import org.apache.commons.lang3.NotImplementedException;

@Data
public class Branch implements Paginatable {
    private String name;
    private Commit target;

    @Override
    public String getPaginationQuery() {
        throw new NotImplementedException("Not implemented yet.");
    }
}
