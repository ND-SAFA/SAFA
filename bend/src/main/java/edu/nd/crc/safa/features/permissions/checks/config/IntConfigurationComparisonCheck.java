package edu.nd.crc.safa.features.permissions.checks.config;

import java.util.function.Function;

import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;

/**
 * Specialization of {@link ConfigurationComparisonCheck} for integers
 */
public abstract class IntConfigurationComparisonCheck extends ConfigurationComparisonCheck<Integer> {
    public IntConfigurationComparisonCheck(Function<PermissionCheckContext, Integer> valueSupplier, String configKey,
                                           ComparisonType comparisonType) {
        super(valueSupplier, configKey, Integer.class, comparisonType);
    }
}
