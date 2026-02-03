# Publishing to the web

This repository includes a small static site at `docs/` that can host downloads for the two applications in `dist/`.

Options to publish:

- GitHub Pages (recommended): commit & push this branch. A workflow is included to copy `dist/` into `docs/releases` and publish `docs/` to the `gh-pages` branch.
- Netlify / Vercel: drag-and-drop the `docs/` folder or connect the repo and set the publish directory to `docs/`.
- GitHub Releases: create a release and upload the `.exe` files as release assets; link to those files from `docs/index.html` if you prefer not to put large binaries into the Pages branch.

Steps (GitHub Pages via included workflow):

1. Ensure the `dist/` directory contains the built executables: `Genius3DChess.exe` and `AutonomousDiary.exe`.
2. Commit the changes in this branch and push to GitHub:

```powershell
git add docs PUBLISHING.md .github/workflows/deploy-pages.yml
git commit -m "Add docs site and GitHub Pages deploy workflow"
git push origin copilot/update-vscode-documentation
```

3. On GitHub, go to the repository > Actions and watch the `Deploy to GitHub Pages` job. It will copy `dist/` into `docs/releases` and push the `docs/` content to `gh-pages`.

4. When the job finishes, visit `https://<your-username>.github.io/<repo-name>/` to see the page.

Notes & alternatives:
- If you'd rather not store executables inside the Pages site, create a GitHub Release with attached executables and update `docs/index.html` links to point to release URLs.
- Netlify or Vercel may impose file-size limits; for larger binaries use an external file host and link to them.

If you want, I can:
- Push this branch to your GitHub remote for you (I cannot do that without credentials), or
- Create a Release draft and prepare command lines for you to upload the binaries manually.
