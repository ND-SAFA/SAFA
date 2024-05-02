package edu.nd.crc.safa.features.health;

import lombok.Data;

@Data
public class ConceptMatchDTO {
    /**
     * ID of concept artifact matched.
     */
    private String id;
    /**
     * Index in artifact context where match occurs.
     */
    private int loc;
}
