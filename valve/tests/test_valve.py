from valve import valve


class TestValve:
    def test_calc_coeff(self):
        v = valve.Valve()
        v.calc_coeff(2)
        assert v.Cv == 60.0

    def test_press_drop(self):
        v = valve.Valve()
        v.press_drop(100)
        assert v.deltaP == 11.111111111111112

    def test_sys_flow_rate(self):
        v = valve.Valve()
        v.sys_flow_rate(v.Cv, v.deltaP)
        assert v.flow_out == 116.18950038622252

    def test_cls_get_position(self):
        v = valve.Valve()
        assert v.cls_get_position() == 0

    def test_cls_change_position(self):
        v = valve.Valve()
        v.cls_change_position(100)
        assert v.cls_get_position() == 100

    def test_open(self):
        v = valve.Valve()
        v.open()
        assert v.cls_get_position() == 100

    def test_close(self):
        v = valve.Valve(position=100)
        v.close()
        assert v.cls_get_position() == 0