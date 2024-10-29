#!/bin/bash

### Variables
tx_session='sesh'
win1=0

### Browser
firefox -new-window 'https://www.youtube.com'
firefox -new-tab 'https://www.google.com'
firefox -new-window 'https://en.wikipedia.org/wiki/Plus-Tech_Squeeze_Box'

### Tmux
tmux attach -t $tx_session || {
	tmux new-session -d -s $tx_session -c `realpath ~/pictures/`
	tmux rename-window -t $tx_session:$win1 'win1'
	tmux select-window -t $win1
	tmux select-layout even-horizontal

	sleep 0.3
	tmux send-keys -t $win1.0 'cmatrix' C-m

	tmux select-window -t $win1
	tmux select-pane -t 0
	tmux attach -t $tx_session
}