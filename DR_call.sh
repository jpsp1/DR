D=$HOME/agents/DR

cd $D

date > DR.log 2>&1

source .venv/bin/activate

export PATH=$PATH:$HOME/.local/bin:$HOME/.nvm/versions/node/v26.13.1/bin:$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games

export NVM_BIN=$HOME/.nvm/versions/node/v26.13.1/bin

uv  run DR.py >> DR.log 2>&1

