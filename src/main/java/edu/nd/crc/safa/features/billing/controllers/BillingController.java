package edu.nd.crc.safa.features.billing.controllers;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.billing.entities.app.TransactionAppEntity;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.billing.services.StripeService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;

@Controller
public class BillingController extends BaseController {

    private final BillingService billingService;
    private final StripeService stripeService;

    public BillingController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                             BillingService billingService, StripeService stripeService) {
        super(resourceBuilder, serviceProvider);
        this.billingService = billingService;
        this.stripeService = stripeService;
    }

    @PostMapping(AppRoutes.Stripe.CHECKOUT)
    public TransactionAppEntity purchaseCredits(@RequestBody PurchaseDetailsDTO purchaseDetails) {
        Organization organization = getResourceBuilder().fetchOrganization(purchaseDetails.getOrganizationId())
            .withPermission(OrganizationPermission.VIEW_BILLING, getCurrentUser())
            .get();
        return billingService.startTransaction(organization, purchaseDetails.getAmount(),
            purchaseDetails.getDescription());
    }

    @PostMapping(AppRoutes.Stripe.CANCEL)
    public void cancelSession(@PathVariable String sessionId) {
        stripeService.cancelSession(sessionId);
    }

    @PostMapping(AppRoutes.Stripe.WEBHOOK)
    public void processStripeEvent(@RequestBody String body,
                                   @RequestHeader("Stripe-Signature") String stripeSignature) {
        stripeService.processWebhookEvent(body, stripeSignature);
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PurchaseDetailsDTO {
        private UUID organizationId;
        private int amount;
        private String description;
    }

}
