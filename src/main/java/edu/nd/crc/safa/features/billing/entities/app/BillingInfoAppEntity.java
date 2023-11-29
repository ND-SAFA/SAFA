package edu.nd.crc.safa.features.organizations.entities.app;

import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class BillingInfoAppEntity {
    private PaymentTier paymentTier;
    private int monthlyRemainingCredits;
    private int monthlyUsedCredits;
    private int monthlySuccessfulCredits;
    private int totalUsedCredits;
    private int totalSuccessfulCredits;

    public BillingInfoAppEntity(Organization organization, BillingInfo billingInfo) {
        this.paymentTier = organization.getPaymentTier();
        this.totalUsedCredits = billingInfo.getTotalUsed();
        this.totalSuccessfulCredits = billingInfo.getTotalSuccessful();
    }
}
