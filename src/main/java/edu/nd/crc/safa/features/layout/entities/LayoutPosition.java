package edu.nd.crc.safa.features.layout.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Responsible for defining a position in a graph from the top left corner
 * of the container.
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class LayoutPosition {
    /**
     * # of pixels right from the top left corner.
     */
    double x;
    /**
     * # of pixels down from the top left corner.
     */
    double y;
}
