# Predictions of traffic collision based on weather data (MSiD project)

Welcome to my project on MSID. The main goal of this project is to analyze traffic collisions, focusing on data from weekends, holidays, and various weather conditions. Additionally, the project aims to develop a predictive model to forecast traffic collisions, as well as the number of injuries and fatalities.

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

### Project
```bash
git clone https://github.com/sliweq/Msid_Project.git
cd Msid_Project
poetry shell 
poetry install --no-root
```

## Run

```bash
python -m project
```
### Run with args

- S - show statistics
- V - show visualizations

### Data to predict

Data to predict can be found in project/setup.py file

## Sources

Thanks to data from [https://policja.pl/](https://policja.pl),   [https://danepubliczne.imgw.pl](https://danepubliczne.imgw.pl) and [https://www.timeanddate.com](https://www.timeanddate.com), I was able to complete this project
