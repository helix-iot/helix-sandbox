## Updating/Reseting

Run the following commands:

```
cd helix-sandbox
git pull
cd compose
sudo docker-compose down
rm -rf ../helix/app/db/helix.sqlite
sudo docker-compose up -d
```

