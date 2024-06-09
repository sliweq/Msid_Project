# Correlation of traffic collision and weather (MSiD project)

Welcome to my project on msid. I wanted to find correlation of traffic collisions and weather data in Poland in a specific year. 

## Installation

### Poetry
#### pip
```bash
pip install poetry
```
#### pipx
```bash
pipx install poetry
```

#### pacman
```bash
sudo pacman -S python-poetry
```
#### project
```bash
git clone https://github.com/sliweq/Msid_Project.git
cd Msid_Project
poetry shell 
poetry install --no-root
```

## Run

```bash
python project/__main__.py
```
### Run with args

- F force downloading data
- S show statistics
- V show visualizations
- 12 3.5 0 0
    - Avg temperature
    - Precipitations
    - Weekend (0-No,1-Yes)
    - Holiday (0-No,1-Yes)

## Sources

Thanks to data from [https://policja.pl/](https://policja.pl) and  [https://danepubliczne.imgw.pl](https://danepubliczne.imgw.pl) , I was able to complete this project
