<launch>

<param name="controller_ready" type="string" value="true" />

  <group ns="homework5">
    <param name="controller_ready" type="string" value="true" />
    <node pkg="homework5" name="PIDnodehw5" type="PIDnodehw5.py"/>
  </group>
  
  <group ns="controls_hw">
    <param name="controller_ready" type="string" value="true" />
    <node pkg="controls_hw" name="vehicle_dynamics" type="vehicle_dynamics.py"/>
  </group>
</launch>
