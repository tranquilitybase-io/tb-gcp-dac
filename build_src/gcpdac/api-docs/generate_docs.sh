# === Install redoc-cli and generate API documentation ===
cd ../../../
ls
echo "?????"



npm install redoc-cli
npx redoc-cli bundle src/main/python/tranquilitybase/gcpdac/openapi.yml \
 --title "GCP DAC service REST API" \
 --output docs/index.html
rm -fr node_modules
rm -fr package-lock.json
