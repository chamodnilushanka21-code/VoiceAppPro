name: Final Build
on:
  workflow_dispatch:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install Buildozer
        run: |
          sudo apt update
          sudo apt install -y git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
          pip install --user --upgrade buildozer cython virtualenv
      - name: Build with Buildozer
        run: buildozer android debug
      - name: Upload Artifact
        uses: actions/upload-artifact@v2
        with:
          name: VoicePro-Final-Release
          path: bin/*.apk
