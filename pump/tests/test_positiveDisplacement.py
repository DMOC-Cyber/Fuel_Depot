import pytest
from pump.pump import PositiveDisplacement


class TestSpeed:
    def test_get_speed(self):
        p = PositiveDisplacement()
        p.adjust_speed(0)
        assert p.get_speed_str() == "The pump is stopped."
        p1 = PositiveDisplacement(pump_speed=75, displacement=0.05)
        p1.adjust_speed(75)
        assert p1.get_speed_str() == "The pump is running at 75 rpm."


class TestFlow:
    def test_get_flowrate(self):
        p = PositiveDisplacement(pump_speed=75, displacement=0.05)
        p.adjust_speed(p.speed)
        assert p.get_flow_str() == "The pump outlet flow rate is 3.75 gpm."


class TestPress:
    def test_get_pressure(self):
        p = PositiveDisplacement(press_out=24.5, pump_speed=75, displacement=0.05)
        p.adjust_speed(p.speed)
        assert p.get_press_str() == "The pump pressure is 24.50 psi."


class TestPower:
    def test_get_power(self):
        p = PositiveDisplacement(press_out=24.5, pump_speed=75, displacement=0.05)
        p.adjust_speed(p.speed)
        assert p.get_power_str() == "The power usage for the pump is 0.04 kW."


class TestAdjustSpeed:
    def test_adjust_speed_expected(self):
        p = PositiveDisplacement(press_out=24.5, pump_speed=75, displacement=0.05)
        p.adjust_speed(25)
        assert p.flow_rate == 1.25
        assert p.wattage == 0.013338058432159764
        assert p.speed == 25

    def test_adjust_speed_zero(self):
        p = PositiveDisplacement(press_out=24.5, pump_speed=75, displacement=0.05)
        p.adjust_speed(0)
        assert p.flow_rate == 0.0
        assert p.wattage == 0.0
        assert p.speed == 0

    def test_adjust_speed_neg(self):
        p = PositiveDisplacement(press_out=24.5, pump_speed=75, displacement=0.05)
        with pytest.raises(ValueError) as excinfo:
            p.set_speed(-10)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Speed must be 0 or greater."

    def test_speed_control_non_int(self):
        p = PositiveDisplacement(press_out=24.5, pump_speed=75, displacement=0.05)
        with pytest.raises(TypeError) as excinfo:
            p.set_speed(12.5)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Integer values only."
