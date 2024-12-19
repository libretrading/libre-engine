#!/bin/bash

# Define the directory where your schedulers are located
SCHEDULERS_DIR="/path/to/your/schedulers"
LOGS_DIR="/path/to/logs/schedulers"
ENGINE_DIR="/path/to/your/ENGINE"

# Ensure the logs directory exists
mkdir -p $LOGS_DIR

# List all the Python scheduler scripts
SCHEDULERS=(
    "data_scheduler.py"
    "trader1_scheduler.py"
    "trader2_scheduler.py"
    "trader3_scheduler.py"
    "liquidator_scheduler.py"
    # add the schedulers you want to run here
    # so as you can see, you can trade as many systems on as many accounts as you want
)

# Loop through each scheduler and start a separate tmux session
for scheduler in "${SCHEDULERS[@]}"; do
    session_name=$(basename "$scheduler" .py)
    log_file="$LOGS_DIR/$session_name.log"

    echo "$(date): Starting tmux session '$session_name'" >> $log_file

    # Create a new tmux session for each scheduler
    tmux new-session -d -s "$session_name"
    if [ $? -eq 0 ]; then
        echo "$(date): tmux session '$session_name' created successfully" >> $log_file
    else
        echo "$(date): Failed to create tmux session '$session_name'" >> $log_file
        continue  # Skip this session if tmux session creation fails
    fi

    # Sleep for 1 second
    sleep 1

    # Send the environment activation command and log if successful
    tmux send-keys -t "$session_name" "source /path/to/your/pythonenv/bin/activate" C-m
    if [ $? -eq 0 ]; then
        echo "$(date): Environment activated in session '$session_name'" >> $log_file
    else
        echo "$(date): Failed to activate environment in session '$session_name'" >> $log_file
    fi

    # Sleep for 1 second
    sleep 1

    # Send the PYTHONPATH export command and log if successful
    tmux send-keys -t "$session_name" "export PYTHONPATH=$ENGINE_DIR:\$PYTHONPATH" C-m
    if [ $? -eq 0 ]; then
        echo "$(date): PYTHONPATH set in session '$session_name'" >> $log_file
    else
        echo "$(date): Failed to set PYTHONPATH in session '$session_name'" >> $log_file
    fi

    # Sleep for 1 second
    sleep 1

    # Send the Python script execution command and log if successful
    tmux send-keys -t "$session_name" "python3 $SCHEDULERS_DIR/$scheduler >> $log_file 2>&1" C-m
    if [ $? -eq 0 ]; then
        echo "$(date): Python script '$scheduler' started successfully in session '$session_name'" >> $log_file
    else
        echo "$(date): Failed to start Python script '$scheduler' in session '$session_name'" >> $log_file
    fi
done
