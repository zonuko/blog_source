# zonuko.github.io Source
blog source

# Requirement

## pelican plugin

- git clone https://github.com/getpelican/pelican-plugins.git ../
- rm -rf path/to/pelican-plugins/pelican_youtube
  - 後でカレントディレクトに変えたい

## pelican themes

- git clone --recursive https://github.com/getpelican/pelican-themes ../themes
  - こっちも変えたい

## Python modules

- python -m pip install pelican
- python -m pip install webassets
- python -m pip install BeautifulSoup4
- python -m pip install pelican-youtube
