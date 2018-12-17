/*
 * Amazon FreeRTOS V1.4.1
 * Copyright (C) 2017 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * http://aws.amazon.com/freertos
 * http://www.FreeRTOS.org
 */

#ifndef AWS_CLIENT_CREDENTIAL_KEYS_H
#define AWS_CLIENT_CREDENTIAL_KEYS_H

#include <stdint.h>

/*
 * PEM-encoded client certificate
 *
 * Must include the PEM header and footer:
 * "-----BEGIN CERTIFICATE-----\n"\
 * "...base64 data...\n"\
 * "-----END CERTIFICATE-----\n"
 */
#define keyCLIENT_CERTIFICATE_PEM \
"-----BEGIN CERTIFICATE-----\n"\
"MIIDWjCCAkKgAwIBAgIVAMVeyRxrZcRf7bqtbw4o4QxKPBOJMA0GCSqGSIb3DQEB\n"\
"CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t\n"\
"IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0xODEyMTMxMzM5\n"\
"MDlaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh\n"\
"dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC9n5nX+LDL3IhrZv//\n"\
"KC3JsrYymS6zM0awK+Irr715QZeQ7de3ZQondWuDol/FKJ8wfPz/40pJRflm19p8\n"\
"dsawOs2K2V4GU/IL86h2vqR2EGLvukS/D0kvW+aiucoT6BVUudfTeJycYs0QJ0vX\n"\
"H3iF7HZIgZLD/+g6HFtTAbxihbTOIwifHrJFl6TieJFatJO7hAFnZgwBC0cZqXTK\n"\
"Fh8FEVb4sD6oK0HPjyLGlh2j/RLznwI0CM/TosWe1xoRZQNWHQIYCkEGIybdLuE+\n"\
"st2VUQCp2w4vbiFgVz68EZy4WQHa615C4h74pFFjp8D+dtTiB3Drsw2cYgGQ+BYU\n"\
"VvOlAgMBAAGjYDBeMB8GA1UdIwQYMBaAFB+TWvldXr+QBQpNgbkM8+oIY2RaMB0G\n"\
"A1UdDgQWBBQ0jy3TV7HQicjLvSNSAWR4+6NEOTAMBgNVHRMBAf8EAjAAMA4GA1Ud\n"\
"DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEAraI0moliqtwxNaf8RLRMLZlv\n"\
"C8V9FfYSV+3thMdNzuf6CedFws8VhOM77YaD5b9257yEqoCa/nOjo3XxJ1ebiWL+\n"\
"aKffVrwRxQsYqvelPxTazp9GBDEo2nz50La8QNDZ59Kno+FYdJaV1iMe4EmKLhg8\n"\
"rUnme5SlwATwoKtvzpX5w5Pi9XTWED2dp9sY0Q3bLFO8roHJXi+bpXvU9UbE919T\n"\
"6YZGl/942rgtgBnld/FOiG+xocxY7EHKdsrzRqVluOA1dAth1SqujsQbu0SYDjNy\n"\
"A90Klx3kmYnWd2dGHKJkZt6YlLjjK7I5JGDp6Li8mxIV/i0Ms7fK1DkB1Wr7yQ==\n"\
"-----END CERTIFICATE-----\n"

/*
 * PEM-encoded issuer certificate for AWS IoT Just In Time Registration (JITR).
 * This is required if you're using JITR, since the issuer (Certificate 
 * Authority) of the client certificate is used by the server for routing the 
 * device's initial request. (The device client certificate must always be 
 * sent as well.) For more information about JITR, see:
 *  https://docs.aws.amazon.com/iot/latest/developerguide/jit-provisioning.html, 
 *  https://aws.amazon.com/blogs/iot/just-in-time-registration-of-device-certificates-on-aws-iot/.
 *
 * If you're not using JITR, set below to NULL.
 * 
 * Must include the PEM header and footer:
 * "-----BEGIN CERTIFICATE-----\n"\
 * "...base64 data...\n"\
 * "-----END CERTIFICATE-----\n"
 */
#define keyJITR_DEVICE_CERTIFICATE_AUTHORITY_PEM  NULL

/*
 * PEM-encoded client private key.
 *
 * Must include the PEM header and footer:
 * "-----BEGIN RSA PRIVATE KEY-----\n"\
 * "...base64 data...\n"\
 * "-----END RSA PRIVATE KEY-----\n"
 */
#define keyCLIENT_PRIVATE_KEY_PEM \
"-----BEGIN RSA PRIVATE KEY-----\n"\
"MIIEowIBAAKCAQEAvZ+Z1/iwy9yIa2b//ygtybK2MpkuszNGsCviK6+9eUGXkO3X\n"\
"t2UKJ3Vrg6JfxSifMHz8/+NKSUX5ZtfafHbGsDrNitleBlPyC/Oodr6kdhBi77pE\n"\
"vw9JL1vmornKE+gVVLnX03icnGLNECdL1x94hex2SIGSw//oOhxbUwG8YoW0ziMI\n"\
"nx6yRZek4niRWrSTu4QBZ2YMAQtHGal0yhYfBRFW+LA+qCtBz48ixpYdo/0S858C\n"\
"NAjP06LFntcaEWUDVh0CGApBBiMm3S7hPrLdlVEAqdsOL24hYFc+vBGcuFkB2ute\n"\
"QuIe+KRRY6fA/nbU4gdw67MNnGIBkPgWFFbzpQIDAQABAoIBABu3NzpM/DJf4oSo\n"\
"QmSeD8s6Vs0gfKXuqbdYQq+V+UC+6JNjYDNLDmfkDrnnws3DeTkSG7yfER2Sn7h7\n"\
"dlDY34OkpKRVzxtnq6o5i/cHOGyVSpC1jhTK/Cxy50wDkdjFBFEk9LnRGDr3afeh\n"\
"dsFTtT8F5+gDIFuLjPrpaCPCzjEsD1YWqpz0enPEuoBEEi7lSfJdPVG5916SmA3b\n"\
"xpQew4lGOyOMjRmKPxaSg22xSZzhi3JAlVelFlnvkHzj6S3jXZXilhXPHqo0bfn0\n"\
"L/Y3ymSpHn4fvii8IE6/JuBlDp2+lWn3pfj9F1mtscJElNISAPAmO2vlPGQi1bYC\n"\
"gEcSHSUCgYEA6Qb81OVKT0xuU/SUttdgVKHMzHbFd4IiVZW4BH1Tn4YM6C4Rrgel\n"\
"apq0T4mDR0GPEwUwgaauQVFePN3Igeh8DHc7uW3Ij1ifAuNVpuMQ2lJ2AuC8g4F3\n"\
"iJEhovioVvPyYKXLFwrp3dR1s4HLyJsQ2JDmt2N4njHTwy89QI3QIYMCgYEA0FE2\n"\
"Dtr3Yrnl71RJE4uZ7FC2AztsW0og+CGSjYNgc+V82FyS142XmJgmN3qhD3cA+qwE\n"\
"14J3Eo6d8fV0TvA2IkP6AWDq2fh6RiyD1+sgbtguh65H7m6Cm9Uu/Z27Bj8ykJ+L\n"\
"O9fq/V9ghw9c8YCj7yn/aPPVMVm9T4sfEoYP1bcCgYEAkuJisFevlXiZ+rWqn+32\n"\
"vKIYk7EyG3id59Ct47aT5XP74sZXQplzPVUy3wfRBjNe2iBlSPQl1upROpCZ+Ljw\n"\
"qHLn5KQ8zY6Q/KMLtFxgnR1pYbsDWOlczWqeBzox8k1mtGENOQMaE0f+wR3JtDN6\n"\
"VOhRZbt/pkfGMbwvIefCD70CgYBbqXBU5wp1mYDQZ1DkVcf70KPWFj6eiKarJ/KZ\n"\
"bBZzyKW/ejRuvnHXBhPC06Ws7Vsz8Z8LyO9l7fUXsz5jQZVATJLkKmYMVSZQXGQD\n"\
"DQWvYFZRA2HJSz0THqHXnKDfpc01D86vHVnb9Sy/IQZviYAYy20EHE5Rsb/4ESox\n"\
"92VeTwKBgAwJ5e+0Q2Aw3SKCJYGFtcQpsSQ9//Nm8eNwTkxB1lPdXLate3Ibp4tb\n"\
"5Hg06bgOcr3tI4w2dGZVwOUzPbu6Sdc9/ZoIanJ0BrEEaWLgUsA2d/bmUa4qfvF3\n"\
"52F8Bi5Vve/zFMrRzH3ngupqz9XcOsjkxfDALvJsY48H5KhxweAs\n"\
"-----END RSA PRIVATE KEY-----\n"

/* The constants above are set to const char * pointers defined in aws_demo_runner.c,
 * and externed here for use in C files.  NOTE!  THIS IS DONE FOR CONVENIENCE
 * DURING AN EVALUATION PHASE AND IS NOT GOOD PRACTICE FOR PRODUCTION SYSTEMS 
 * WHICH MUST STORE KEYS SECURELY. */
extern const char clientcredentialCLIENT_CERTIFICATE_PEM[];
extern const char* clientcredentialJITR_DEVICE_CERTIFICATE_AUTHORITY_PEM;
extern const char clientcredentialCLIENT_PRIVATE_KEY_PEM[];
extern const uint32_t clientcredentialCLIENT_CERTIFICATE_LENGTH;
extern const uint32_t clientcredentialCLIENT_PRIVATE_KEY_LENGTH;

#endif /* AWS_CLIENT_CREDENTIAL_KEYS_H */
