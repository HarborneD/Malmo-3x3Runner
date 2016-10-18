# Malmo-3x3Runner
A 3x3 grid view solution to cliff walking. Uses discrete movement commands.

The runner agent takes in the walkable block types and the goal block type and then searches for the goal. 

This is highly based on depth first search with back tracing and queue list. 

Be sure to add: 

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

Project Malmo:
https://github.com/Microsoft/malmo#getting-started

