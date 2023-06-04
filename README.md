# MD-Notifications

A dockerized Python application to notify you when new chapters become available on MangaDex

## Manga list source

MD-Notifications can either read your public MDLists or your private library.  Reading from your private library is more responsive when adding and removing manga but requires you to provide your MangaDex credentials and will only work on "older" MangaDex accounts.  In addition to this, the MangaDex API will be eventually changing its authentication method in the future which break this feature.

For this reason, it is suggested that you use public MDLists.  You will need your MDList's ID which can be found in its URL.

## How to Deploy

### Docker
MD-Notifications can be deployed with a simple docker command

Public MDLists
```
docker run -d -e PUBLIC_MANGA_LIST=<public_manga_list> \
              -e DISCORD_WEBHOOK_URL=<discord_webhook_url> \
               docker.io/du0ng4/md-notifications:master
```

Private Library
```
docker run -d -e MANGADEX_USERNAME=<mangadex_username> \
              -e MANGADEX_PASSWORD=<mangadex_password> \
              -e DISCORD_WEBHOOK_URL=<discord_webhook_url> \
              docker.io/du0ng4/md-notifications:master
```

### Kubernetes
Provided in the directory `k8s/` are `.yaml` files to easily deploy MD-Notifications.  Simply fill in the secrets and from the project's root directory, run the command:

Public MD-Lists
```
kubectl create -f k8s/md-notifications-public.yaml
```

Private Library
```
kubectl create -f k8s/md-notifications-private.yaml
```