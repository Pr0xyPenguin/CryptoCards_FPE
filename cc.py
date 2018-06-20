from Crypto.Cipher import AES
import os
from bitstring import BitArray
import array

###############################################################################
#                                  COUNTER                                    #
###############################################################################
class Secret(object):
  def __init__(self, secret=None):
    if secret is None: secret = os.urandom(16)
    self.secret = secret
    self.reset()
  def counter(self):
    for i, c in enumerate(self.current):
      self.current[i] = c + 1
      if self.current: break
    return self.current.tostring()
  def reset(self):
    self.current = array.array('B', self.secret)




###############################################################################
#                                    INPUT                                    #
###############################################################################
CardNum = 0
while True:
    try:
        CardNum = int(input("Please insert your 16-digit Credit Card number: "))
        if(len(str(CardNum))!=16):
            1/0
        break
    except ValueError:
        print("Oops!  That wasn't a valid number.  Try again...")
    except ZeroDivisionError:
        print("Oops!  The number you've enter is not 16 digits. Try again...")
CardNum = format(CardNum,'054b')




###############################################################################
#                                  ENCRYPTION                                 #
###############################################################################
while True:
    L = CardNum[:27]
    R = CardNum[27:]
    key = os.urandom(16)
    secret = Secret()
    cipher = ''
    try:
        for i in range(1,6):
            temp = L
            L = R
            B = str(R + 93 * '0' + format(i,'08b'))
            secret.reset()
            E = AES.new(key,AES.MODE_CTR,counter= secret.counter)
            cipher = E.encrypt(B)
            cipher = BitArray(bytes=cipher,length=128,offset=1)
            cipher = cipher.bin
            R = format(int(temp,2)^int(cipher[:27],2),'027b')

        if(int(L+R,2) <= 9999999999999999 and int(L+R,2) >= 1000000000000000):
            break
        else:
            1/0
    except ZeroDivisionError:
        print("An error occurred. Trying again...")


print("Your encrypted number is: ",int(L+R,2))


###############################################################################
#                                  DECRYPTION                                 #
###############################################################################
LL = L
RR = R
cipher2 = ''

for j in range(1,6):

    BB = str(LL + 93 * '0' + format(6-j,'08b'))
    secret.reset()
    EE = AES.new(key,AES.MODE_CTR,counter= secret.counter)
    cipher2 = EE.decrypt(BB)
    cipher2 = BitArray(bytes=cipher2,length=128,offset=1)
    cipher2 = cipher2.bin
    temp = RR
    RR = LL
    LL = format(int(temp,2) ^int(cipher2[:27],2),'027b')


print("Your decrypted number is: ",int(LL+RR,2))

###############################################################################
#                                  BIBLIOGRAPHY                               #
###############################################################################

#https://blog.cryptographyengineering.com/2011/11/10/format-preserving-encryption-or-how-to/
#https://www.di-mgt.com.au/crypto-ffsem.html
