from flask_bcrypt import generate_password_hash, check_password_hash

password = "admin1234"

# Test 1 : Hachage standard
h1 = generate_password_hash(password).decode('utf-8')
check1 = check_password_hash(h1, password)

# Test 2 : Hachage avec forçage de bytes (souvent nécessaire sur Mac)
h2 = generate_password_hash(password.encode('utf-8')).decode('utf-8')
check2 = check_password_hash(h2, password)

print(f"--- RÉSULTATS DIAGNOSTIC ---")
print(f"Hash 1 : {h1}")
print(f"Match 1 (Standard) : {'✅' if check1 else '❌'}")
print(f"Match 2 (Bytes force) : {'✅' if check2 else '❌'}")

if not check1 and not check2:
    print("\n🚨 ALERTE : Bcrypt ne fonctionne pas correctement sur ton système.")