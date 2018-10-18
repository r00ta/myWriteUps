import itertools
import pyaes
import base64
import binascii

# flag{r3l4t3d_k3y_der1iviNg_fuNct1on5_h4ve_to_be_a_l1mit3d_cla55}
ciphertext = base64.b64decode('/hmP7OXOYv36sP/ESlbkEcHDw3E7ZOVcBGuJB8pLH9x9iOEzedQ63L0s8zt1/2fI6mlv7stvsrfAKcKdLcaKuw==')[48:64]
key = [224, 8, 130, 45, 222, 236, 200, 140, 196, 78, 236, 193, 20, 66, 32, 15, 249, 156, 202, 166, 110, 233, 153, 144, 13, 212, 67, 62, 224, 14] 
for c in range(255):
	candidate = chr(c)
	candidate += binascii.unhexlify(''.join(map(lambda x: x[2:].rjust(2, '0')[1], map(hex, key))))
	print candidate
	aes = pyaes.AESModeOfOperationECB(candidate)	
	decrypted = aes.decrypt(ciphertext)
	print decrypted

