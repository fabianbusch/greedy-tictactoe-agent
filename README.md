# greedy-tictactoe-agent
This is an experimental project within the topic of reinforcement learning. It is still in progess. Feel free to reuse my code or give me some new inputs!

# TODOs
The following changes have to be done to make it work properly:

- Starting learning with epsilon = 1 and slowly decreasing it until it is 0.
- Create two dnns with same structure, one as "target dnn", one as "current dnn" and calculate with it target_y.
    -- Example: target_y = r + Qs_of_Target_DNN
    -- learn current DNN with target_y as difference
