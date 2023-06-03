# MD-Notifications

A dockerized Python application to notify you when new chapters become available on Mangadex

## How to Deploy

### Docker
MD-Notifications can be deployed with a simple docker command

```
docker run -d -e MANGADEX_USERNAME=<mangadex_username> \
              -e MANGADEX_PASSWORD=<mangadex_password> \
              -e DISCORD_WEBHOOK_URL=<discord_webhook_url> \
              docker.io/du0ng4/md-notifications:master
```

### Kubernetes
Provided in the directory `k8s/` is a `.yaml` file to easily deploy MD-Notifications.  Simply fill in the secrets and from the project's root directory, run the command:
```
kubectl create -f k8s/md-notifications.yaml
```
