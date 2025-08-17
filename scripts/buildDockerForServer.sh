docker build --platform linux/amd64 -t dining-web-scraping-amd64 .
docker save -o dining-web-scraping-amd64.tar dining-web-scraping-amd64
scp dining-web-scraping-amd64.tar pphyo@moxie.cs.oswego.edu:/home/pphyo/CSC495/webscraping