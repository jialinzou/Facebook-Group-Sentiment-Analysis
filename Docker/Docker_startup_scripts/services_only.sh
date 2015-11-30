cd ../../ && sudo docker build --file="Docker/Dockerfiles/Dockerfile_services_only" -t mxlei01/facebook-sentiment-analysis-services-only .
sudo docker run --net="host" --name mxlei01/facebook-sentiment-analysis-services-only mxlei01/facebook-sentiment-analysis-services-only
