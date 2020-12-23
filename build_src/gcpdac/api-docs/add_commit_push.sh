# === git add, commit and push ===
git config user.email git.action@gft.com
git config user.name "gitaction gft"

# check if file changed
git status
if ! git diff --no-ext-diff --quiet --exit-code ../../../docs/index.html; then
  git add ../../../docs/index.html
  git commit -m "[CICD ignore] Add automatically generated openapi static HTML documentation"
else
  echo "no diff detected, skipping updating doc"
fi
