<launch>

<param name="controller_ready" type="string" value="true" />

  <group ns="homework9">
    <param name="controller_ready" type="string" value="true" />
    <node pkg="homework9" name="PIDnodehw9" type="PIDnodehw9.py"/>
  </group>
  
  <group ns="controls_hw">
    <param name="controller_ready" type="string" value="true" />
    <node pkg="controls_hw" name="vehicle_dynamics" type="vehicle_dynamics.py"/>
  </group>
</launch>
