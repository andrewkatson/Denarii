
#ifndef sodium_H
#define sodium_H

#include "src/device_trezor/trezor/include/version.h"

#include "src/device_trezor/trezor/include/core.h"
#include "src/device_trezor/trezor/include/crypto_aead_aes256gcm.h"
#include "src/device_trezor/trezor/include/crypto_aead_chacha20poly1305.h"
#include "src/device_trezor/trezor/include/crypto_aead_xchacha20poly1305.h"
#include "src/device_trezor/trezor/include/crypto_auth.h"
#include "src/device_trezor/trezor/include/crypto_auth_hmacsha256.h"
#include "src/device_trezor/trezor/include/crypto_auth_hmacsha512.h"
#include "src/device_trezor/trezor/include/crypto_auth_hmacsha512256.h"
#include "src/device_trezor/trezor/include/crypto_box.h"
#include "src/device_trezor/trezor/include/crypto_box_curve25519xsalsa20poly1305.h"
#include "src/device_trezor/trezor/include/crypto_core_hsalsa20.h"
#include "src/device_trezor/trezor/include/crypto_core_hchacha20.h"
#include "src/device_trezor/trezor/include/crypto_core_salsa20.h"
#include "src/device_trezor/trezor/include/crypto_core_salsa2012.h"
#include "src/device_trezor/trezor/include/crypto_core_salsa208.h"
#include "src/device_trezor/trezor/include/crypto_generichash.h"
#include "src/device_trezor/trezor/include/crypto_generichash_blake2b.h"
#include "src/device_trezor/trezor/include/crypto_hash.h"
#include "src/device_trezor/trezor/include/crypto_hash_sha256.h"
#include "src/device_trezor/trezor/include/crypto_hash_sha512.h"
#include "src/device_trezor/trezor/include/crypto_kdf.h"
#include "src/device_trezor/trezor/include/crypto_kdf_blake2b.h"
#include "src/device_trezor/trezor/include/crypto_kx.h"
#include "src/device_trezor/trezor/include/crypto_onetimeauth.h"
#include "src/device_trezor/trezor/include/crypto_onetimeauth_poly1305.h"
#include "src/device_trezor/trezor/include/crypto_pwhash.h"
#include "src/device_trezor/trezor/include/crypto_pwhash_argon2i.h"
#include "src/device_trezor/trezor/include/crypto_scalarmult.h"
#include "src/device_trezor/trezor/include/crypto_scalarmult_curve25519.h"
#include "src/device_trezor/trezor/include/crypto_secretbox.h"
#include "src/device_trezor/trezor/include/crypto_secretbox_xsalsa20poly1305.h"
#include "src/device_trezor/trezor/include/crypto_secretstream_xchacha20poly1305.h"
#include "src/device_trezor/trezor/include/crypto_shorthash.h"
#include "src/device_trezor/trezor/include/crypto_shorthash_siphash24.h"
#include "src/device_trezor/trezor/include/crypto_sign.h"
#include "src/device_trezor/trezor/include/crypto_sign_ed25519.h"
#include "src/device_trezor/trezor/include/crypto_stream.h"
#include "src/device_trezor/trezor/include/crypto_stream_chacha20.h"
#include "src/device_trezor/trezor/include/crypto_stream_salsa20.h"
#include "src/device_trezor/trezor/include/crypto_stream_xsalsa20.h"
#include "src/device_trezor/trezor/include/crypto_verify_16.h"
#include "src/device_trezor/trezor/include/crypto_verify_32.h"
#include "src/device_trezor/trezor/include/crypto_verify_64.h"
#include "src/device_trezor/trezor/include/randombytes.h"
#include "src/device_trezor/trezor/include/randombytes_internal_random.h"
#include "src/device_trezor/trezor/include/randombytes_sysrandom.h"
#include "src/device_trezor/trezor/include/runtime.h"
#include "src/device_trezor/trezor/include/utils.h"

#ifndef SODIUM_LIBRARY_MINIMAL
# include "src/device_trezor/trezor/include/crypto_box_curve25519xchacha20poly1305.h"
# include "src/device_trezor/trezor/include/crypto_core_ed25519.h"
# include "src/device_trezor/trezor/include/crypto_core_ristretto255.h"
# include "src/device_trezor/trezor/include/crypto_scalarmult_ed25519.h"
# include "src/device_trezor/trezor/include/crypto_scalarmult_ristretto255.h"
# include "src/device_trezor/trezor/include/crypto_secretbox_xchacha20poly1305.h"
# include "src/device_trezor/trezor/include/crypto_pwhash_scryptsalsa208sha256.h"
# include "src/device_trezor/trezor/include/crypto_stream_salsa2012.h"
# include "src/device_trezor/trezor/include/crypto_stream_salsa208.h"
# include "src/device_trezor/trezor/include/crypto_stream_xchacha20.h"
#endif

#endif