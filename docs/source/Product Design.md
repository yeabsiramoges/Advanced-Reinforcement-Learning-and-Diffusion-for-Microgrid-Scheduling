# Background
> "[[notes/Microgrids|Microgrids]], also called “mini-grids,” are self-sufficient energy systems that can operate independently from a centralized grid system while supplying a distinct geographic area with energy. Their ability to run independently from the centralized grid, in island mode, increases their resilience to outages caused by natural disasters because it shields communities from power outages rooted in the centralized grid." [^1]

> "Microgrids primarily consist of various components, including Renewable Energy Sources (RES), Distributed Generation (DG), [reciprocating engines](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/piston-engine "Learn more about reciprocating engines from ScienceDirect's AI-generated Topic Pages"), [energy storage systems](https://www.sciencedirect.com/topics/engineering/energy-storage-system "Learn more about energy storage systems from ScienceDirect's AI-generated Topic Pages"), and different types of loads, all operating in a controlled and coordinated manner." [^2]

> "Microgrids can help in increasing the resilience of the power system with efficient energy management and real-time solution in case of extreme weather conditions and in an emergency situation when a [power outage](https://www.sciencedirect.com/topics/engineering/power-outage "Learn more about power outage from ScienceDirect's AI-generated Topic Pages") in the main utility grid occurs. Hence, microgrids can provide a sustainable power alternative in case of frequent outages to keep the critical infrastructure continuously powered without contributing to climate change. This in turn can increase system reliability, adaptability and enhances the system’s overall efficiency." [^2]

> "Microgrids can be regarded as a local electricity network that can deliver power to the consumer using an intelligent control operation for flexible and easy communication among the different interconnected system sources so, that the supply and demand ratio remains balanced." [^2]

> "Despite the challenges in the development of the microgrid, there are still numerous opportunities and solutions to tackle the challenges that microgrids face and pave a road map for the future sustainable microgrids.

...

> An efficient and advanced [energy management system](https://www.sciencedirect.com/topics/engineering/energy-management-system "Learn more about energy management system from ScienceDirect's AI-generated Topic Pages") can also play a leading role in the microgrid's operation and planning by managing the microgrid's load modelling and power sources integration issues. Energy management system can be helpful in achieving the balance between generation and demand. It can also help in reducing GHG emissions by the utilization of more RES and less fossil fuel-based sources for power generation

...

> Forecasting techniques can be used in the microgrid to predict demand and generation in various [climatic conditions](https://www.sciencedirect.com/topics/engineering/climatic-condition "Learn more about climatic conditions from ScienceDirect's AI-generated Topic Pages"). Due to the challenge of climate change forecasting techniques in the microgrid are of valuable importance and without it the proper design, operation and planning of the microgrid will not be successful." [^2]

> "For further enhancing the features of the microgrid to provide more improved services, microgrids need to be upgraded on certain advanced levels. According to researchers report of Sandia National Laboratories as cited in [[20]](https://www.sciencedirect.com/science/article/pii/S1755008424000024#b0100), advanced microgrids must comprise large scale grid features such as:

- Capability of balancing demand and generation on a real-time basis.
- Scheduling dispatch of resources.
- Optimization of energy profile and efficiencies.
- Compatibility with the protection system and coordination.
- Preservation of grid reliability.
- Ensuring secure communication." [^2]
![image](https://onlinelibrary.wiley.com/cms/asset/3a766f61-99d0-4670-b2c7-c8cc253cf9b4/etep12683-gra-0001.png)
TABLE 1. Different control methods for the respective MG operation [^3]
# Value Proposition
[[coding/microgrids/wiki/RLDIFF|RLDIFF]] will serve as a smart controller capable of efficiently allocating energy through out the grid, managing both energy consumption but also energy transmission if connected to a larger grid to cause beneficial downstream effects from causing more of the grid using renewable energy sources.

Microgrids contain a complex resource allocation problem that is well served with the advanced predictve ability of [[notes/Diffusion|Diffusion]] with the reliable agent training through [[notes/Reinforcement Learning|Reinforcement Learning]].

The efficiency gains from optimizing microgrids helps in island mode with energy and cost saving, as well as providing power for the larger grid when interconnected from energy runoff.
# Objectives
- [ ] Adaptive planner that incorporates [[notes/Reinforcement Learning|Reinforcement Learning]] and [[notes/Diffusion|Diffusion]] to generate efficient microgrid execution trajectories.
# Solution
## Papers
- [[notes/Planning with Diffusion for Flexible Behavior Synthesis|Planning with Diffusion for Flexible Behavior Synthesis]]: [Diffuser](https://github.com/jannerm/diffuser)
- [[notes/AdaptDiffuser|Diffusion Models as Adaptive Self-evolving Planners]]: [AdaptDiffuser](https://github.com/Liang-ZX/adaptdiffuser)
- [[notes/Adaptive Online Replanning with Diffusion Models]]: [ReplanDiffsuer](https://github.com/rainbow979/replandiffuser)
- [[Goal-Conditioned HRL]]: [Code](https://github.com/AboudyKreidieh/h-baselines?tab=readme-ov-file#2-supported-modelsalgorithms)
## Supplimental Works
- [[notes/Novelty Detection in Reinforcement Learning with World Models|Novelty Detection in Reinforcement Learning with World Models]]
- [[notes/Curiosity-driven Exploration by Self-supervised Prediction|Curiosity-driven Exploration by Self-supervised Prediction]]
## Implementation
Using the [[notes/Diffusion|Diffusion]]-boosted [[notes/Reinforcement Learning|Reinforcement Learning]] models, every step of the evolutionary model chooses the best performing agent, as well as the agents that would provide the greatest "Novelty" when exploring the solution space. This would be done as Goal Conditioned HRL, where the goal would be maximizing exploration and latent-based detection. The [[Online Reinforcement Learing]] model will be able to replan using the best aspects of constantly fed data.
### Core Features
### Integration
### Alternatives
### Constraints
### Out-of-Scope

# Feasibility
The proposed solution is almost a maximum viable product for the time remaining. Required resources below are fulfilled, so the remaining work is combining the hierarchal model with the adaptive evolutionary models in an effective manner.
## Required Resources
- [x] Compute: [[Satori]], [[Engaging]]
 ___
[^1]: [Microgrids for Climate Resilience](https://www.newamerica.org/the-thread/climate-change-microgrids/)
[^2]: [Microgrid Literature Overview](https://www.sciencedirect.com/science/article/pii/S1755008424000024)
[^3]: [AC, DC, and hybrid control strategies](https://onlinelibrary.wiley.com/doi/full/10.1002/2050-7038.12683)
