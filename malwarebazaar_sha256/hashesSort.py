import os
from urllib import response
from malwarebazaar.api import Bazaar
import tqdm

bazaar = Bazaar("user's api key here ")

hashesFile = open("full_sha256.txt")
count = 0
for i, line in enumerate(hashesFile):
        count += 1
        
        try:
            response = bazaar.query_hash(line.strip())
            if 'Ransomware' in response['data'][0]['tags'] or 'ransomware' in response['data'][0]['tags']:
                    extension = response['data'][0]['file_type']
                    print(extension)
                    f = open(f"E:\\Ransomware 2023\\collection\\hashes_{extension}.txt", "a")
                    f.write('\n' + line.strip())
                    f.close()
            else:
                # print('else')
                pass
        except:
            f = open(f"E:\\Ransomware 2023\\collection\\retry.txt", "a")
            f.write('\n' + line.strip())
            f.close()
            
        print(count)

hashesFile.close()
