# Malmo-3x3Runner
A 3x3 grid view solution to cliff walking. Uses discrete movement commands.

The runner agent takes in the walkable block types and the goal block type and then searches for the goal. 

This is highly based on depth first search with back tracing and queue list. 

Be sure to add the following to your mission XML: 

```
         <DiscreteMovementCommands/>
                    <ObservationFromFullStats/>
                  <ObservationFromGrid>
                      <Grid name="floor3x3">
                        <min x="-1" y="-1" z="-1"/>
                        <max x="1" y="-1" z="1"/>
                      </Grid>
                  </ObservationFromGrid>
```

Example usage within tutorial 7:

```
    #make decision making agent
    runner_agent = GridViewRunnerAgent(["diamond_block","emerald_block","redstone_block"],"redstone_block")

    # Loop until mission ends:
    while world_state.is_mission_running:
        sys.stdout.write(".")
        time.sleep(0.2)
        world_state = agent_host.getWorldState()

        runner_agent.TakeNextAction(world_state,agent_host)

        for error in world_state.errors:
            print "Error:",error.text

```


Project Malmo:
https://github.com/Microsoft/malmo#getting-started

