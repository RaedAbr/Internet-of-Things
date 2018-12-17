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
"MIIDWjCCAkKgAwIBAgIVAOyUuS4fmoX12jjPc/52QR+HOsBNMA0GCSqGSIb3DQEB\n"\
"CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t\n"\
"IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0xODEyMTcxNTM2\n"\
"NDBaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh\n"\
"dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC48krqzyQz68dq2qKn\n"\
"3ibTuDONE0WTN/ppoxXawy+3l0DpJoGT7GUzeICKxKLp/ELdtc1zjJuauUkb6dX1\n"\
"ayXqJg1iV/uITwFV5RFrMNMuP9lGpJkFvqLGCsA38vw8xiJAl50o8Chp1uZsUBPE\n"\
"8fQeWqsJQrSZ0CyYWeqmoPSzQLZmYomQke7jeePQfoN3qCxWmzx66V1eRtfwo1b+\n"\
"im/8ZfAVHNSc1ThArRywyFPyaWzKx5mG5a1+mr2FE7Pn4l9u/tBc/KgUFKqpKD8C\n"\
"MQ9L28cUSmRudB9nDbAaJQXwb3i3C+2ycmSR8HvBB9oNs/QcQLWJEpL2J22OtcN0\n"\
"vElvAgMBAAGjYDBeMB8GA1UdIwQYMBaAFDMVd3UjTl4adom+Icdpmrpm/EiKMB0G\n"\
"A1UdDgQWBBSE+3DSNjh9yn+fw6LSCjAKipEY3jAMBgNVHRMBAf8EAjAAMA4GA1Ud\n"\
"DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEAPlNh1ufVgvUAdlyaMm2rQxwn\n"\
"39AV7pKtUWwDSZPZipa0zp/Rfs9ssK+GHNbqbzR3IRelGJJaW1FN2VJNGUmEQKS8\n"\
"0yAOKtbbYeN8Z/RL2hTtjYGFPgxaN++7E9Z6N/j14s5k68WN7RetM7bS1TP+xtrW\n"\
"tKgHi88z3TGOR2WPYf3/uf4uH2fhfsN3BHAEU5Vsit2JUyc4i1Mp59/p40CeCk+J\n"\
"uHeElRjGwz6+H7/jadGSpgJXzlpEdOvEzQ8e5qR8kPPc1kmFr1FjRbvOrYiSFS82\n"\
"oDSNQV7i97j5L5+15MndKOTSljTZbFZ3GTSKTfZqIXAPiDqBPELfum0ZSWPHrQ==\n"\
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
"MIIEpAIBAAKCAQEAuPJK6s8kM+vHatqip94m07gzjRNFkzf6aaMV2sMvt5dA6SaB\n"\
"k+xlM3iAisSi6fxC3bXNc4ybmrlJG+nV9Wsl6iYNYlf7iE8BVeURazDTLj/ZRqSZ\n"\
"Bb6ixgrAN/L8PMYiQJedKPAoadbmbFATxPH0HlqrCUK0mdAsmFnqpqD0s0C2ZmKJ\n"\
"kJHu43nj0H6Dd6gsVps8euldXkbX8KNW/opv/GXwFRzUnNU4QK0csMhT8mlsyseZ\n"\
"huWtfpq9hROz5+Jfbv7QXPyoFBSqqSg/AjEPS9vHFEpkbnQfZw2wGiUF8G94twvt\n"\
"snJkkfB7wQfaDbP0HEC1iRKS9idtjrXDdLxJbwIDAQABAoIBAFrOjD4yKoJbt/Qd\n"\
"GVP23XWCsb0Iw1Z/W7JWYrqgr2MjHrnbMDAjF6Vn+yUnWx4rv+EADLo5RYV4iA7u\n"\
"hyES1PDcciHhNR0+PVehOyY4ONgyfUoUMxYA/gbi7HIMGhD074hraLza/dzJqSVx\n"\
"Q+OlMMlely/a0rXa4qqDK5VY3gzMWZDFxcDTs6G0PlZhODKDG/6BowIoBTYdddeb\n"\
"iH1nH+vt3xgV/FpjNC4NcpvLlazjtxPKJ1Bq1LKNval6NQf0fYKNX6XCNuz3SPu/\n"\
"xAAPwP43q6/IXZyaNbzcOG6OjV1kqXZPT4rm03xPxvLW9Qsq9Rbba1jxjKoTY18v\n"\
"vR0KGBECgYEA3JVIUAroG2dRTojDMsVOeARQ0VAQxz/KbcKbbXDKll1+216QelUj\n"\
"/bP1DdB09Xlb+rtP1BIlB7VGIJxNt0+gPSH6ki8NU3A2db7z3SpE+qcyNQU/qukU\n"\
"8FS6cxPqMp/TKvxbYw9f1Rq1i0OtHBiLJiszse18QInI287zKiIMcYMCgYEA1qQ4\n"\
"rNPzx3HZT85AQEtIAbvh3jmajXI9HoMdWCWkwhhbUndGi6JwZpk+iWqsrzhML1DO\n"\
"euwORVoO1t16LihjcOUz9bmz2RgJP2iBC7dGFWQq9qvln7iDRLf20GwWW1/elYez\n"\
"+seN+5dYcfj0p6IBhFYl/laSaS4DCO/+tcxiYKUCgYEAi2TPIL3ztbWRvQZSDFiB\n"\
"YPihNdTZ9YALZVdQr1VSwLjuvKRCuvvo1Z+OYZ90+dcqWAVcyhB5VCiq21rLBeeM\n"\
"xHUfipevXSYRVFFKfF4E3z0fTkA13sSSldmFRcm0+y7i3ExDWBNUJTBOv2YSFCoy\n"\
"bPlqHquMFKC9zKI4Kkz//g8CgYEAgcsAcpIgogRYUof4FmjvfAzvAoB20v23s9G5\n"\
"Vuo8fRpZbr6trBZoPcKBLHuTPMmgWCRXF8HSx2E0A/4dufe2WjhfeUH4XVjJjsxU\n"\
"7I7BFIJj8JH14uWii1VrLJGP22VXpbhPv2AYnYDhfNn8p7mxjSLDCs+y7WNjdm4Z\n"\
"6jlTa/kCgYB8KASgWEGsRJC4HW3Heyyq8cPV33wzj07ZpeK7T/8gAT7dgigkNTAS\n"\
"MaPSdLxbWPvFuw4ORbojlMZl72Rss9pNoHsps+nY+PrzszWzNj3Pofqqq3usPwjq\n"\
"cNwvWrUrgNKVYg/myfeGLAvdgk3EmOTmVZn7qC/yNr21VPofMQbyfg==\n"\
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
