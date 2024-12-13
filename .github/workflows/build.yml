name: Build JSON

on:
  push:
    branches:
      - main
  schedule:
    # * is a special character in YAML so you have to quote this string
    - cron:  '0 * * * *'

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python 3.12
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install PyGithub
    - name: Run script and commit changes
      run: |
        python release.py
        echo "Setting up git credentials..."
        git remote set-url origin https://x-access-token:"$GITHUB_TOKEN"@github.com/"$GITHUB_REPOSITORY".git
        git config --global user.email "actions@github.com"
        git config --global user.name "actions"
        echo "Git credentials configured."

        git checkout main
        git add .
        git commit -m "Automatic update of data" && git push --set-upstream origin main || true
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
