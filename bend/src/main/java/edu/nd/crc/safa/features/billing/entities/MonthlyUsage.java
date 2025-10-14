package edu.nd.crc.safa.features.billing.entities;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class MonthlyUsage {
    private int usedCredits;
    private int successfulCredits;
}
