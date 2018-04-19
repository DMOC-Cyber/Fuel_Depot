#!/bin/python

"""
VirtualPLC-pump.py

Purpose: Creates a generic Pump class for PLC-controlled SCADA systems. Subclassed into variable and positive
displacement pumps.

Author: Cody Jackson

Date: 4/12/18
#################################
Version 0.1
    Initial build
"""
import math

# from pymodbus.client.sync import ModbusTcpClient


class Pump:
    """Generic class for pumps.

    Default parameters: Volumetric flow rate, required head pressure, outlet pressure, pump speed, power required

    Provides base methods to change pump speed control, calculate changes to pump parameters based on speed changes,
    read the pump speed, outlet pressure, and flow rate.
    """
    def __init__(self, flow_rate=0.0, pump_head_in=0.0, press_out=0.0, pump_speed=0, power=0.0):
        """Set initial parameters.

        :param flow_rate: Flow rate from the pump (gpm)
        :param pump_head_in: Necessary pump head into the pump (feet)
        :param press_out: Pressure created by the pump (psi)
        :param pump_speed: Rotational speed of the pump (rpm)
        :param power: Power required to drive the pump at the current speed (kw)
        """
        self.flow_rate = flow_rate
        self.head = pump_head_in
        self.outlet_pressure = press_out
        self.speed = pump_speed
        self.power = power

    def speed_control(self, new_speed):
        """Change the pump speed.

        :param new_speed: Requested speed for the pump
        :except TypeError Exception if non-integer argument used
        """
        try:
            if type(self.speed) != int:
                raise TypeError
        except TypeError:
            return "Integer values only."
        else:
            self.speed = new_speed
            return "Pump speed changed to {speed}%".format(speed=self.speed)

    def pump_laws(self, old_speed, new_speed, old_flow_rate, old_press_out, old_pump_power):
        """Defines pump characteristics that are based on pump speed.

        Only applies to variable displacement (centrifugal) pumps. Variable names match pump law equations.

        :param old_speed: Current (old) speed of the pump
        :param new_speed: Requested (new) speed of the pump
        :param old_flow_rate: Current (old) flow rate from the pump
        :param old_press_out: Current (old) pressure from the pump
        :param old_pump_power: Current (old) power requirement of the pump
        :return: Volumetric flow rate, pump head, and pressure
        """
        self.n1 = old_speed
        self.n2 = new_speed
        self.V1 = old_flow_rate
        self.Hp1 = old_press_out
        self.P1 = old_pump_power

        self.V2 = self.V1 * (self.n2 / self.n1)  # New flow rate
        self.Hp2 = self.Hp1 * math.pow((self.n2 / self.n1), 2)  # New outlet pressure
        self.P2 = self.P1 * math.pow((self.n2 / self.n1), 3)  # New pump power

        return self.V2, self.Hp2, self.P2

    def cls_read_speed(self):
        """Get the current speed of the pump.

        :return: Pump speed
        """
        return self.speed

    def cls_read_press(self):
        """Get the current outlet pressure of the pump.

        :return: Pressure from the pump
        """
        return self.outlet_pressure

    def cls_read_flow(self):
        """Get the current outlet flow rate of the pump.

        :return: Outlet flow rate
        """
        return self.flow_rate

    def cls_read_power(self):
        """Get the current power draw of the pump.

        :return: Current pump power requirement
        """
        return self.power


class CentrifPump(Pump):
    """Defines a variable-displacement, centrifugal-style pump."""
    def __init__(self):
        """Set default pump parameters."""
        super().__init__(flow_rate=1000.0, pump_head_in=25.0, press_out=45.0, pump_speed=5000, power=1.5)

    def get_speed(self):
        """Get the current speed of the pump

        :return: Current rotational speed, in rpm
        """
        return "The pump is running at {speed} rpm.".format(speed=self.cls_read_speed())

    def get_flowrate(self):
        """Get the current flow rate of the pump

        :return: Current flow rate, in gpm
        """
        return "The pump is pushing {flow} gpm.".format(flow=self.cls_read_flow())

    def get_pressure(self):
        """Get the current output pressure for the pump.

        :return: Current outlet pressure, in psi
        """
        return "The pump pressure is {press} psi.".format(press=self.cls_read_press())

    def get_power(self):
        """Get the current power draw for the pump.

        :return: Current power requirement, in kW
        """
        return "The power usage for the pump is {pow} kW.".format(pow=self.cls_read_power())

    def change_speed(self, new_speed):
        """Modify the speed of the pump.

        Affects the outlet flow rate, outlet pressure, and power requirements for the pump.

        :param new_speed: New pump speed
        :return: Changes, in-place, the flow rate, output pressure, and pump power requirement
        """
        self.new_speed = new_speed
        self.n1 = self.speed
        self.V1 = self.flow_rate
        self.Hp1 = self.outlet_pressure
        self.P1 = self.power

        self.speed_control(self.new_speed)
        self.flow_rate, self.outlet_pressure, self.power = self.pump_laws(self.n1, self.new_speed, self.V1, self.Hp1,
                                                                          self.P1)

        # print("Old parameters: {speed}, {flow}, {press}, {power}".format(speed=self.n1, flow=self.V1, press=self.Hp1,
        #                                                                  power=self.P1))
        # print("New parameters: {speed}, {flow}, {press}, {power}".format(speed=self.new_speed, flow=self.flow_rate,
        #                                                                  press=self.outlet_pressure, power=self.power))


class PositiveDisplacement(Pump):
    """Defines a positive-displacement pump."""
    def __init__(self):
        """Set default pump parameters."""
        super().__init__(flow_rate=1000.0, press_out=45.0, pump_speed=5000, power=1.5)

    def get_speed(self):
        """Get the current speed of the pump

        :return: Current rotational speed, in rpm
        """
        return "The pump is running at {speed} rpm.".format(speed=self.cls_read_speed())

    def get_flowrate(self):
        """Get the current flow rate of the pump

        :return: Current flow rate, in gpm
        """
        return "The pump is pushing {flow} gpm.".format(flow=self.cls_read_flow())

    def get_pressure(self):
        """Get the current output pressure for the pump.

        :return: Current outlet pressure, in psi
        """
        return "The pump pressure is {press} psi.".format(press=self.cls_read_press())

    def get_power(self):
        """Get the current power draw for the pump.

        :return: Current power requirement, in kW
        """
        return "The power usage for the pump is {pow} kW.".format(pow=self.cls_read_power())

    def change_speed(self, new_speed):
        """Modify the speed of the pump.

        Affects the outlet flow rate and power requirements for the pump.

        :param new_speed: New pump speed
        :return: Changes, in-place, the flow rate, and pump power requirement
        """
        self.speed_diff = new_speed / self.speed
        self.flow_rate = self.flow_rate * self.speed_diff
        self.power = self.power * self.speed_diff
        self.speed = new_speed

        # print("The new speed is {speed} rpm, the new flow rate is {flow:.0f} gpm, " \
        #        "and the new power usage is {pow:.1f} kW.".format(speed=self.speed, flow=self.flow_rate,
        #                                                          pow=self.power))