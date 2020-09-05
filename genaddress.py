from dotscoin.Address import Address
add= Address()
pub_address= add.get_public_address()
keys=add.export()
print(pub_address)
print(keys)