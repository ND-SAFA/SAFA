package edu.nd.crc.safa.features.permissions.checks.billing;

import java.util.List;
import java.util.function.Function;

import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;
import edu.nd.crc.safa.features.permissions.checks.utility.OrPermissionCheck;

/**
 * A check determining if an organization can afford a particular charge,
 * taking into account that some payment tiers ignore balance
 */
public class CanAffordChargeCheck extends OrPermissionCheck {

    public CanAffordChargeCheck(int chargeAmount) {
        super(
            List.of(
                new HasUnlimitedCreditsCheck(),
                new MinimumBalanceCheck(chargeAmount)
            )
        );
    }

    public CanAffordChargeCheck(Function<PermissionCheckContext, Integer> chargeAmountSupplier) {
        super(
            List.of(
                new HasUnlimitedCreditsCheck(),
                new MinimumBalanceCheck(chargeAmountSupplier)
            )
        );
    }
}
