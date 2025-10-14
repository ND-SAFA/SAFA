package edu.nd.crc.safa.features.permissions.checks.billing;

import java.util.Set;

import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;

import lombok.AllArgsConstructor;

/**
 * An additional permission check that makes sure the
 * organization in the context has a payment tier that
 * includes whatever feature is represented by the permission.
 */
@AllArgsConstructor
public class PaymentTierCheck implements AdditionalPermissionCheck {

    private Set<PaymentTier> supportedTiers;

    public PaymentTierCheck(PaymentTier tier) {
        this(Set.of(tier));
    }

    @Override
    public boolean doCheck(PermissionCheckContext context) {
        Organization org = context.getOrganization();

        if (org == null) {
            return false;
        }

        return supportedTiers.contains(org.getPaymentTier());
    }

    @Override
    public String getMessage() {
        return "Payment tier must be among the following: " + supportedTiers;
    }

    @Override
    public boolean superuserCanOverride() {
        return true;
    }
}
