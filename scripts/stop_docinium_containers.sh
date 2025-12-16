# stop all containers related to docinium
# starting names from docinium_*

# chmod +x stop_docinium_containers.sh  

echo "Stopping all docinium containers..."

docker rm -f $(docker ps -aq --filter "name=docinium_*")

echo "All docinium containers have been stopped."