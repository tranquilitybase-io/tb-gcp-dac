# === git add, commit and push ===
git config user.email git.action@gft.com
git config user.name "gitaction gft"
chmod 777 redoc-static.html
mv redoc-static.html docs/index.html

# check if file changed
if ! git diff --no-ext-diff --quiet --exit-code docs/index.html; then
  git add docs/index.html
  git commit -m "Add automatically generated openapi static HTML documentation"
fi
