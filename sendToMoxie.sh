docker save -o dining-web-scraping.tar dining-web-scraping
scp dining-web-scraping.tar pphyo@moxie.cs.oswego.edu:/home/pphyo/CSC495/webscraping
#ssh pphyo@moxie.cs.oswego.edu
#cd /home/pphyo/CSC495/webscraping || exit
#docker load -i dining-web-scraping.tar

#scp main.py requirements.txt Dockerfile pphyo@moxie.cs.oswego.edu:/home/pphyo/CSC495/webscraping