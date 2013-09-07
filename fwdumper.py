from bs4 import BeautifulSoup
import os, os.path

"""Throwaway script to parse htm files
very specific to my setup, probably useless"""

if __name__ == "__main__":
	maxm = 0
	sortedfiles = []
	for root, dirs, files in os.walk("book"):
		fwfiles = [(os.path.join(root,f), int(f.split("-")[1].split(".")[0])) for f in files if f.find("fw-") != -1]
		sortedfiles.append(sorted(fwfiles, key =  lambda x: x[1]))
	for f in sortedfiles[0]:
		fn = open(f[0])
		soup = BeautifulSoup(fn)
		cells = soup.select("tr")
		#cells = soup.select("tr td")
		for t in cells:
			#print f[1], t
			if t:
				print f[1], t.get_text().encode('utf-8').rstrip() 

