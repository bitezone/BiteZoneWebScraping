# The program should be run from the directory of menu-scraping folder
mkdir temp
cp ./docker-compose.server.yml ./temp
mv ./temp/docker-compose.server.yml ./temp/docker-compose.yml
docker commit $(docker ps --filter "name=web_scraping_service" --format "{{.ID}}") bitezone/web-scraping
docker commit $(docker ps --filter "name=postgres_bitezone" --format "{{.ID}}") bitezone/database
docker save bitezone/web-scraping > ./temp/bitezone-web-scraping.tar
docker save bitezone/database > ./temp/bitezone-database.tar

scp -r ./temp ./helper_scripts/server_scripts/unpack_docker_images.sh pphyo@cs.oswego.edu:/home/pphyo/CSC495/docker-images

rm -rf temp