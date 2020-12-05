
#ifndef MONERO_CRYPTO_H

#define MONERO_CRYPTO_H



#include "monero/crypto/amd64-64-24k.h"



#define monero_crypto_ge25519_scalarmult monero_crypto_amd64_64_24k_ge25519_scalarmult

#define monero_crypto_generate_key_derivation monero_crypto_amd64_64_24k_generate_key_derivation

#define monero_crypto_generate_subaddress_public_key monero_crypto_amd64_64_24k_generate_subaddress_public_key



#endif // MONERO_CRYPTO_H

