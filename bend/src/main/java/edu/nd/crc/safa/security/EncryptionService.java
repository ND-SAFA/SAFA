package edu.nd.crc.safa.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.util.Base64;

/**
 * Service for encrypting and decrypting sensitive data using AES-256-GCM.
 * Uses a secret key from environment configuration.
 */
@Service
public class EncryptionService {

    private static final String ALGORITHM = "AES/GCM/NoPadding";
    private static final int GCM_IV_LENGTH = 12;
    private static final int GCM_TAG_LENGTH = 128;

    private final SecretKey secretKey;

    public EncryptionService(@Value("${encryption.key:}") String encryptionKey) {
        // Allow service to be created without key, but will fail at runtime if used
        if (encryptionKey == null || encryptionKey.trim().isEmpty()) {
            this.secretKey = null;
            return;
        }

        byte[] decodedKey = Base64.getDecoder().decode(encryptionKey.trim());
        if (decodedKey.length != 32) {
            throw new IllegalStateException(
                "Invalid encryption key length. Expected 32 bytes (256 bits), got " + decodedKey.length
            );
        }

        this.secretKey = new SecretKeySpec(decodedKey, "AES");
    }

    /**
     * Encrypts plaintext using AES-256-GCM.
     *
     * @param plaintext The text to encrypt
     * @return Base64-encoded encrypted text with IV prepended
     * @throws EncryptionException if encryption fails
     */
    public String encrypt(String plaintext) {
        if (plaintext == null) {
            return null;
        }

        if (secretKey == null) {
            throw new EncryptionException(
                "Encryption key not configured. Please set 'encryption.key' environment variable or application property."
            );
        }

        try {
            Cipher cipher = Cipher.getInstance(ALGORITHM);

            // Generate random IV
            byte[] iv = new byte[GCM_IV_LENGTH];
            SecureRandom.getInstanceStrong().nextBytes(iv);
            GCMParameterSpec parameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);

            cipher.init(Cipher.ENCRYPT_MODE, secretKey, parameterSpec);
            byte[] ciphertext = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));

            // Prepend IV to ciphertext
            byte[] combined = new byte[iv.length + ciphertext.length];
            System.arraycopy(iv, 0, combined, 0, iv.length);
            System.arraycopy(ciphertext, 0, combined, iv.length, ciphertext.length);

            return Base64.getEncoder().encodeToString(combined);
        } catch (Exception e) {
            throw new EncryptionException("Failed to encrypt data", e);
        }
    }

    /**
     * Decrypts encrypted text using AES-256-GCM.
     *
     * @param encryptedText Base64-encoded encrypted text with IV prepended
     * @return Decrypted plaintext
     * @throws EncryptionException if decryption fails
     */
    public String decrypt(String encryptedText) {
        if (encryptedText == null) {
            return null;
        }

        if (secretKey == null) {
            throw new EncryptionException(
                "Encryption key not configured. Please set 'encryption.key' environment variable or application property."
            );
        }

        try {
            byte[] combined = Base64.getDecoder().decode(encryptedText);

            if (combined.length < GCM_IV_LENGTH) {
                throw new EncryptionException("Invalid encrypted data: too short");
            }

            // Extract IV and ciphertext
            byte[] iv = new byte[GCM_IV_LENGTH];
            byte[] ciphertext = new byte[combined.length - GCM_IV_LENGTH];
            System.arraycopy(combined, 0, iv, 0, iv.length);
            System.arraycopy(combined, iv.length, ciphertext, 0, ciphertext.length);

            Cipher cipher = Cipher.getInstance(ALGORITHM);
            GCMParameterSpec parameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
            cipher.init(Cipher.DECRYPT_MODE, secretKey, parameterSpec);

            byte[] plaintext = cipher.doFinal(ciphertext);
            return new String(plaintext, StandardCharsets.UTF_8);
        } catch (Exception e) {
            throw new EncryptionException("Failed to decrypt data", e);
        }
    }

    /**
     * Exception thrown when encryption or decryption fails.
     */
    public static class EncryptionException extends RuntimeException {
        public EncryptionException(String message) {
            super(message);
        }

        public EncryptionException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}
