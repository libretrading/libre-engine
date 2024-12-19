#!/bin/bash

# Define log directory
LOG_DIR="/path/to/logs"
mkdir -p $LOG_DIR

# Send C-c to all active tmux sessions and log the output
echo "Sending C-c to all active tmux sessions..." | tee -a $LOG_DIR/tmux_terminate.log
for session in $(tmux list-sessions -F '#S'); do
  tmux send-keys -t "$session" C-c
done
echo "C-c sent to all active tmux sessions." | tee -a $LOG_DIR/tmux_terminate.log

# Kill all tmux sessions and log the output
echo "Killing all tmux sessions..." | tee -a $LOG_DIR/tmux_terminate.log
tmux kill-server >> $LOG_DIR/tmux_terminate.log 2>&1
echo "All tmux sessions killed." | tee -a $LOG_DIR/tmux_terminate.log

# Autoremove and autoclean with logging
echo "Running autoremove and autoclean..." | tee -a $LOG_DIR/apt_clean.log
sudo apt-get autoremove -y >> $LOG_DIR/apt_clean.log 2>&1
sudo apt-get autoclean -y >> $LOG_DIR/apt_clean.log 2>&1
echo "Autoremove and autoclean completed." | tee -a $LOG_DIR/apt_clean.log

# Update and upgrade with logging
echo "Updating and upgrading the system..." | tee -a $LOG_DIR/apt_update.log
sudo apt-get update -y >> $LOG_DIR/apt_update.log 2>&1
sudo apt-get upgrade -y >> $LOG_DIR/apt_update.log 2>&1
echo "System update and upgrade completed." | tee -a $LOG_DIR/apt_update.log

# Reboot the system with logging
echo "Rebooting the system..." | tee -a $LOG_DIR/reboot.log
sudo /sbin/reboot >> $LOG_DIR/reboot.log 2>&1
echo "System reboot initiated." | tee -a $LOG_DIR/reboot.log
