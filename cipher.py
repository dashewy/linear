from supplemental_functions import blocker, hill_scramber_key
from supplemental_functions import stream_scambeler,  alpha_bin_dict, bin_alpha_dict

class cipher():
    # may be used in later versions
    def __init__(self):
        pass
    
    def ceaser_encode(self, my_message, my_offset, show=True):
 
        encoded = []
        for letter in my_message:
    
            if letter.isalpha():
      
                if letter.isupper():
        
                    first_index = ord('A')
                 
                    encoder = chr(first_index + (ord(letter) - first_index - my_offset) % 26 )

                    encoded.append(encoder)
                else:
                    first_index = ord('a')

                    encoder = chr(first_index + (ord(letter) - first_index - my_offset) % 26)

                    encoded.append(encoder)
     
            else:
                remain = chr(ord(letter))

                encoded.append(remain)

        new_string = ''.join(encoded)
 
        if show is True:
            print(new_string)
        return new_string
    
    def ceaser_decode(self, message, offset, show=True):
  
        decoded = []
 
        for letter in message:

            if letter.isalpha():
      
                if letter.isupper():
                    first_index = ord('A')

                    decoder = chr(first_index + ((ord(letter) - first_index + offset)) % 26)

                    decoded.append(decoder)
                else:
                    first_index = ord('a')

                    decoder = chr(first_index + ((ord(letter) - first_index + offset)) % 26)

                    decoded.append(decoder)
    
            else:
                remain = chr(ord(letter))

                decoded.append(remain)

  
        new_string = ''.join(decoded)

        if show is True:
            print(new_string)
  
        return(new_string)
    
    def affine_encode(self, my_message, my_offset, a, show=True):
  
        encoded = []
        for letter in my_message:
    
            if letter.isalpha():
      
                if letter.isupper():
        
                    first_index = ord('A')

                    encoder = chr(first_index + (a * (ord(letter) - first_index) + my_offset) % 26)

                    encoded.append(encoder)
                else:
                    first_index = ord('a')

                    encoder = chr(first_index + (a * (ord(letter) - first_index) + my_offset) % 26)

                    encoded.append(encoder)
      
            else:
                remain = chr(ord(letter))

                encoded.append(remain)

        new_string = ''.join(encoded)

        if show is True:
            print(new_string)
  
        return new_string

    def affine_decode(self, message, offset, a, show=True):
        try:
            a_inverse = pow(a, -1, 26)
        except ValueError:
            print('a does not have inverse, try using a different value')
            # this stops code below from running
            return
        decoded = []
        
        for letter in message:
 
            if letter.isalpha():
    
                if letter.isupper():
                    first_index = ord('A')

                    decoder = chr(first_index + ((a_inverse * ((ord(letter) - first_index) - offset))) % 26)

                    decoded.append(decoder)
                else:
                    first_index = ord('a')

                    decoder = chr(first_index + ((a_inverse  * ((ord(letter) - first_index) - offset))) % 26)
                
                    decoded.append(decoder)
  
            else:
                remain = chr(ord(letter))
        
                decoded.append(remain)


        new_string = ''.join(decoded)

        if show is True:
            print(new_string)


        return(new_string)
    
    

    def vigenre_encode(self, new_message, keyword_phrase, show=True):
        new_encoder = []
        keyword_updater = []


        count = 0

        for i in keyword_phrase:
            if i.isalpha():
                if i.isupper():

                    first_index = ord('A')

                    keyword_updater.append(ord(i) - first_index)
                else:
                    first_index = ord('a')

                    keyword_updater.append(ord(i) - first_index)

            else:
                remain = chr(ord(i))

                keyword_updater.append(remain)

        for letter in new_message:

            if letter.isalpha():
                if letter.isupper():
                    first_index = ord('A')

                    machine = chr(first_index + (ord(letter) - first_index + (keyword_updater[count % len(keyword_updater)])) % 26)

                    new_encoder.append(machine)

                    count += 1

                else:
                    first_index = ord('a')
     
                    machine = chr(first_index + (ord(letter) - first_index + (keyword_updater[count % len(keyword_updater)])) % 26)

                    new_encoder.append(machine)

                    count += 1

            else:
                remain = chr(ord(letter))

                new_encoder.append(remain)

        updated_string = ''.join(new_encoder)

        if show is True:
            print(updated_string)
        return(updated_string)
    
    def vigenre_decode(self, new_message, keyword_phrase, show=True):
        new_decoder = []
        keyword_updater = []

        count = 0

        for i in keyword_phrase:
            if i.isalpha():
                if i.isupper():

                    first_index = ord('A')

                    keyword_updater.append(ord(i) - first_index)
                else:
                    first_index = ord('a')

                    keyword_updater.append(ord(i) - first_index)

            else:
                remain = chr(ord(i))

                keyword_updater.append(remain)

        for letter in new_message:

            if letter.isalpha():
                if letter.isupper():
                    first_index = ord('A')

                    machine = chr(first_index + (ord(letter) - first_index - (keyword_updater[count % len(keyword_updater)])) % 26)

                    new_decoder.append(machine)

                    count += 1

                else:
                    first_index = ord('a')

                    machine = chr(first_index + (ord(letter) - first_index - (keyword_updater[count % len(keyword_updater)])) % 26)

                    new_decoder.append(machine)

                    count += 1

            else:
                remain = chr(ord(letter))

                new_decoder.append(remain)

        updated_string = ''.join(new_decoder)

        if show is True:
            print(updated_string)
        
        return(updated_string)
    
    
    def hill(self, message, key, size):
        
        message = blocker(message, size, show=False)    
        key = hill_scramber_key(size, show=False)
        
        
    def streamer(self, message, encrypt=True, show=True):
        bin_dict = alpha_bin_dict()
        if encrypt is True:
            tokenize = message.split()
            letters = []
            
            for word in tokenize:
                for letter in word:
                    letters.append(letter)
                    
            binary_rep = []
            for letter in letters:
                pass
                
            
            
        if show is True:
            print(tokenize)
            print(letters)
            # print(bin_dict)
            # print(binary_rep)

    
    def brutus_breaker(self, message):
        
        for number in range(26):
            method_1 = self.ceaser_decode(message, offset=number, show=False)
            print(f'the message is {method_1} and offset is {number}')
                
    def affine_breaker(self, message):
        
        for a in range(26):
            for n in range(26):
                method_2 = self.affine_decode(message, offset=n, a=a, show=False)
                if method_2 is not None:
                    print(f'the message is {method_2} and the offset is {n} and the multiplier is {a}')





cipher_test = cipher()
# cipher_test.affine_decode('TTGFTMGTTJMTTR.MCTMTRAOTGTJMJ.TOQTGJMTJMJMTAJ.', 15, 9)
# cipher_test.affine_decode('wben', 4, 9)

# cipher_test.affine_breaker('IXCEHRI AQ VEIP')
cipher_test.streamer('hello world')