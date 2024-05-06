package edu.nd.crc.safa.features.health.entities.gen;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
@Data
public class GenContradiction {
    /**
     * List of IDs conflicting with artifact being checked.
     */
    private List<String> conflictingIds = new ArrayList<>();
    /**
     * Explanation of conflict.
     */
    private String explanation;
}
