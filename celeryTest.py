from tasks import add, gen_prime

add.delay()
prime=gen_prime.delay(5000)
print(prime.ready())
# print(prime.get(timeout=2))