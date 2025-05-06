set -e

echo "Hi, stopping the container..."
# Stop the container

containerid=`docker ps | awk -F " " '{print $1}'`
docker rm -f $containerid
echo "Container stopped successfully."

