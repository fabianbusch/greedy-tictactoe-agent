#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 19:14:44 2019

@author: fabian
"""

import tensorflow as tf
import numpy as np
import gym

env = gym.make('FrozenLake-v0')

# Network Definition - Part 1
input_s = tf.placeholder(tf.float32, shape=(1, 16))
wl1 = tf.Variable(tf.random_uniform([16, 16], 0, 1))
biasl1 = tf.Variable(tf.ones([1, 16]))
l1_out = tf.nn.relu(tf.add(tf.matmul(input_s, wl1), biasl1))

wl2 = tf.Variable(tf.random_uniform([16, 16], 0, 1))
biasl2 = tf.Variable(tf.ones([1, 16]))
l2_out = tf.nn.relu(tf.add(tf.matmul(l1_out, wl2), biasl2))

wl3 = tf.Variable(tf.random_uniform([16, 4], 0, 1))
biasl3 = tf.Variable(tf.ones([1, 4]))

output_Q = tf.nn.softmax(tf.add(tf.matmul(l2_out, wl3), biasl3))
predicted_action = tf.argmax(output_Q, 1)

# Loss Function - Part 2
next_Q = tf.placeholder(tf.float32, shape=(1, 4))
loss = tf.reduce_sum(tf.square(next_Q - output_Q))

# Optimizer - Part 3
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.003)
train = optimizer.minimize(loss)

# Training
init = tf.global_variables_initializer()

DISCOUNT_FACTOR = .99
EPSILON = 0.2
EPISODES = 20000

with tf.Session() as session:
    session.run(init)
    
    for i in range(EPISODES):
        s = env.reset()
        
        done = False
        
        if i % 100 == 0:
            print('EPISODE', i, 'of', EPISODES)
        
        while not done:
            
            next_input = np.identity(16)[s:s+1]
            a, all_q = session.run([predicted_action, output_Q], feed_dict={input_s:next_input})
            
            if np.random.rand(1) < EPSILON:
                a[0] = env.action_space.sample()
                
            s_next, r, done, _ = env.step(a[0])
            
            next_input = np.identity(16)[s_next:s_next + 1]
            q_next = session.run(output_Q, feed_dict={input_s:next_input})
            
            max_q_next = np.max(q_next)
            target_q = all_q
            target_q[0, a[0]] = r + DISCOUNT_FACTOR * max_q_next
            
            _ = session.run([train], feed_dict={input_s:np.identity(16)[s:s + 1], next_Q:target_q})
            
            s = s_next
    
    # Ergebnis
    for i in range(16):
        next_input = np.identity(16)[i:i + 1]
        all_q = session.run([output_Q], feed_dict={input_s: next_input})
        
        print(i, all_q)