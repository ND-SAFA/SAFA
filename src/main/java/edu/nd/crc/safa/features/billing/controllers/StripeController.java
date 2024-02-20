package edu.nd.crc.safa.features.billing.controllers;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.billing.services.StripeService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StripeController extends BaseController {
    private final StripeService stripeService;

    public StripeController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                            StripeService stripeService) {
        super(resourceBuilder, serviceProvider);
        this.stripeService = stripeService;
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
}
