##Intro

This projects automates process of scraping data from 
Otomoto.pl with Selenium WebDriver and Behave framework.
Project perform action of searching for a BMW M3 that wasn't a part of any car crash, 
sorting by the cheapest price. Data like link, name and price is being scraped out of the website
and send to Neon database


##Getting Started
In Bash
git clone https://github.com/krawczukm11/pageObjectBehave/issues


##Prepare env
For Ubuntu
sudo apt-get update
sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
sudo apt-get install unixodbc unixodbc-dev

##Python setup
curl https://pyenv.run | bash
python -m venv /path/to/your/venv
source /path/to/your/venv/bin/activate
pyenv install 3.12.4
pyenv global 3.12.4
pip install -r requirements.txt

##Startomg a test
write "behave"