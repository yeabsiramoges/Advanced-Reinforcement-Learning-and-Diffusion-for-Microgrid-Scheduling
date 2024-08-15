---
tags: compsci
dg-publish: true
---
Research Topics: [[notes/Microgrids]], [[notes/Adaptive Scheduling]]
Research Areas: [[notes/Adaptive Controls]], [Reinforcement Learning](notes/Reinforcement%20Learning.md), [Diffusion](notes/Diffusion.md)
___
Proposal Title: [[notes/Advanced Reinforcement Learning for Microgrid Scheduling]]

Project Overview: Most buildings in the united states get their power from a nation wide power grid. Throughout the year, this central grid serves to power offices, schools, and residential homes with little issue. Problems are in non standard environmental conditions that result in breaks across the grid, some small like a tree falling on a line while others can cause several states to be out of power for an extended period of time.

Microgrids are decentralized energy grids that service specific facilities. Microgrids are great because you get to have a high level of control over power availability and use; microgrids thrive due to being independent, intelligent, local power stores and generators. This project deals with the intelligent aspect of the grid, the controller, with a focus on maintaining energy equilibrium to reduce climate impact from the facility. Controller manages the system balance with respect to stores power, actively generated power, and the price of both and the opportunity cost of keeping the energy versus selling to the central grid.

Personal Statement: 
Climate is an interesting use case for diffusion modeling. I say this having done two previous research projects that lend themselves well to this one.

My first experience related to diffusion modeling applications in the virtual try on space. This research began with a survey of the industry, looking at specific provides of diffusion model based try-on services. The research dealt with using 3D scans of clothes and people and using cross-attention to perform implicit wrapping and blending around the contours of a subject. The diffusion process was the bridging step, while cross attention worked to maintain the key identifiers of the clothing.

My second experience dealt with energy companies and climate work directly. This project looked into using hourly energy time series data to predict future loads on the grid and use those predictions to control the output from the grid. The key finding from this research project that makes me feel confident in this one is finding improved performance from using randomized methods instead of autoregressive and non-seasonal methods.

I think that there is a lot of potential in using the predictive and generative power of reinforcement learning to improve the output of diffusion models.

Personal Responsibilities & Tentative Work Plan: My task in this project is performing the training mentioned above, using reinforcement learning to aid in the training of our diffusion model where we will be using the diffusion model as an adaptive scheduler for the microgrid. The main goal I have in mind is making a focus of exploring low density sections of the solution space when training our model. Here, two papers that I find interesting are [[notes/Novelty Detection in Reinforcement Learning with World Models]] and [[notes/Curiosity-driven Exploration by Self-supervised Prediction]]. Both look into two new approaches for exploring new avenues through the state space of our agent, resulting in new and often times better executions.

Time Commitment: 27 hours weekly
