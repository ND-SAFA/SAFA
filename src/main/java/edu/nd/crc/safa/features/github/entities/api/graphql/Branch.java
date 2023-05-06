package edu.nd.crc.safa.features.github.entities.api.graphql;

import java.util.List;
import java.util.function.Consumer;

import edu.nd.crc.safa.utilities.graphql.entities.Paginatable;

import lombok.Data;
import org.apache.commons.lang3.NotImplementedException;

@Data
public class Branch implements Paginatable<Branch> {
    private String name;
    private Commit target;

    @Override
    public Consumer<List<Branch>> getPaginationFunction() {
        throw new NotImplementedException("Not implemented yet.");
    }
}
