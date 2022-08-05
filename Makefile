translations.csv: generate-data.py
	GOOGLE_APPLICATION_CREDENTIALS="service-account-file.json" python3 generate-data.py
summary.txt: translations.csv summarise.py
	python3 summarise.py > summary.txt

