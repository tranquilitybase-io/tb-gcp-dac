# === git add, commit and push ===
echo "--- hello ---"
git config user.email git.action@gft.com
git config user.name "gitaction gft"

# check if file changed
echo "--- status ---"
git status
if ! git diff --no-ext-diff --quiet --exit-code docs/index.html; then
  git add ../../../docs/index.html
  git commit -m "Add automatically generated openapi static HTML documentation"
fi
